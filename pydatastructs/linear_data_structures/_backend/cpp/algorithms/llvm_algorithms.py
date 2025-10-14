from llvmlite import ir, binding
import atexit

_SUPPORTED = {
    "int32": (ir.IntType(32), 4),
    "int64": (ir.IntType(64), 8),
    "float32": (ir.FloatType(), 4),
    "float64": (ir.DoubleType(), 8),
}

_engines = {}
_target_machine = None
_fn_ptr_cache = {}

def _cleanup():
    global _engines, _target_machine, _fn_ptr_cache
    _engines.clear()
    _target_machine = None
    _fn_ptr_cache.clear()

atexit.register(_cleanup)

def _ensure_target_machine():
    global _target_machine
    if _target_machine is not None:
        return

    try:
        binding.initialize_all_targets()
        binding.initialize_all_asmprinters()

        target = binding.Target.from_default_triple()
        _target_machine = target.create_target_machine(opt=3)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize LLVM target machine: {e}")

def get_bubble_sort_ptr(dtype: str) -> int:
    dtype = dtype.lower().strip()
    if dtype not in _SUPPORTED:
        raise ValueError(f"Unsupported dtype '{dtype}'. Supported: {list(_SUPPORTED)}")

    return _materialize(dtype)


def get_is_ordered_ptr(dtype: str) -> int:
    dtype = dtype.lower().strip()
    if dtype not in _SUPPORTED:
        raise ValueError(f"Unsupported dtype '{dtype}'. Supported: {list(_SUPPORTED)}")

    return _materialize_is_ordered(dtype)


def _build_is_ordered_ir(dtype: str) -> str:
    if dtype not in _SUPPORTED:
        raise ValueError(f"Unsupported dtype '{dtype}'. Supported: {list(_SUPPORTED)}")

    T, _ = _SUPPORTED[dtype]
    i32 = ir.IntType(32)
    i64 = ir.IntType(64)

    mod = ir.Module(name=f"is_ordered_{dtype}_module")
    fn_name = f"is_ordered_{dtype}"

    fn_ty = ir.FunctionType(i32, [T.as_pointer(), i32])
    fn = ir.Function(mod, fn_ty, name=fn_name)

    arr, n = fn.args
    arr.name, n.name = "arr", "n"

    b_entry = fn.append_basic_block("entry")
    b_loop = fn.append_basic_block("loop")
    b_check = fn.append_basic_block("check")
    b_ret_true = fn.append_basic_block("ret_true")
    b_ret_false = fn.append_basic_block("ret_false")
    b_exit = fn.append_basic_block("exit")

    b = ir.IRBuilder(b_entry)
    cond_trivial = b.icmp_signed("<=", n, ir.Constant(i32, 1))
    b.cbranch(cond_trivial, b_ret_true, b_loop)

    b.position_at_end(b_loop)
    i = b.phi(i32, name="i")
    i.add_incoming(ir.Constant(i32, 1), b_entry)

    cond_loop = b.icmp_signed("<", i, n)
    b.cbranch(cond_loop, b_check, b_ret_true)

    b.position_at_end(b_check)
    i64_idx = b.sext(i, i64)
    iprev = b.sub(i, ir.Constant(i32, 1))
    iprev64 = b.sext(iprev, i64)

    ptr_i = b.gep(arr, [i64_idx], inbounds=True)
    ptr_iprev = b.gep(arr, [iprev64], inbounds=True)

    val_i = b.load(ptr_i)
    val_iprev = b.load(ptr_iprev)

    if isinstance(T, ir.IntType):
        cond = b.icmp_signed("<=", val_iprev, val_i)
    else:
        cond = b.fcmp_ordered("<=", val_iprev, val_i, fastmath=True)

    b.cbranch(cond, b.loop, b_ret_false)

    b.position_at_end(b_ret_false)
    b.ret(ir.Constant(i32, 0))

    b.position_at_end(b.loop)
    i_next = b.add(i, ir.Constant(i32, 1))
    i.add_incoming(i_next, b.loop)
    b.branch(b_loop)

    b.position_at_end(b_ret_true)
    b.ret(ir.Constant(i32, 1))

    return str(mod)


def _materialize_is_ordered(dtype: str) -> int:
    _ensure_target_machine()

    if dtype in _fn_ptr_cache:
        return _fn_ptr_cache[dtype]

    try:
        llvm_ir = _build_is_ordered_ir(dtype)
        mod = binding.parse_assembly(llvm_ir)
        mod.verify()

        try:
            pm = binding.ModulePassManager()
            pm.add_instruction_combining_pass()
            pm.add_reassociate_pass()
            pm.add_gvn_pass()
            pm.add_cfg_simplification_pass()
            pm.run(mod)
        except AttributeError:
            pass

        engine = binding.create_mcjit_compiler(mod, _target_machine)
        engine.finalize_object()
        engine.run_static_constructors()

        addr = engine.get_function_address(f"is_ordered_{dtype}")
        if not addr:
            raise RuntimeError(f"Failed to get address for is_ordered_{dtype}")

        _fn_ptr_cache[dtype] = addr
        _engines[dtype] = engine

        return addr

    except Exception as e:
        raise RuntimeError(f"Failed to materialize function for dtype {dtype}: {e}")

def _build_bubble_sort_ir(dtype: str) -> str:
    if dtype not in _SUPPORTED:
        raise ValueError(f"Unsupported dtype '{dtype}'. Supported: {list(_SUPPORTED)}")

    T, _ = _SUPPORTED[dtype]
    i32 = ir.IntType(32)
    i64 = ir.IntType(64)

    mod = ir.Module(name=f"bubble_sort_{dtype}_module")
    fn_name = f"bubble_sort_{dtype}"

    fn_ty = ir.FunctionType(ir.VoidType(), [T.as_pointer(), i32])
    fn = ir.Function(mod, fn_ty, name=fn_name)

    arr, n = fn.args
    arr.name, n.name = "arr", "n"

    b_entry = fn.append_basic_block("entry")
    b_outer = fn.append_basic_block("outer")
    b_inner_init = fn.append_basic_block("inner.init")
    b_inner = fn.append_basic_block("inner")
    b_body = fn.append_basic_block("body")
    b_swap = fn.append_basic_block("swap")
    b_inner_latch = fn.append_basic_block("inner.latch")
    b_outer_latch = fn.append_basic_block("outer.latch")
    b_exit = fn.append_basic_block("exit")

    b = ir.IRBuilder(b_entry)

    cond_trivial = b.icmp_signed("<=", n, ir.Constant(i32, 1))
    b.cbranch(cond_trivial, b_exit, b_outer)

    b.position_at_end(b_outer)
    i_phi = b.phi(i32, name="i")
    i_phi.add_incoming(ir.Constant(i32, 0), b_entry)

    n1 = b.sub(n, ir.Constant(i32, 1), name="n_minus_1")
    cond_outer = b.icmp_signed("<", i_phi, n1)
    b.cbranch(cond_outer, b_inner_init, b_exit)

    b.position_at_end(b_inner_init)

    inner_limit = b.sub(n1, i_phi, name="inner_limit")
    b.branch(b_inner)

    b.position_at_end(b_inner)
    j_phi = b.phi(i32, name="j")
    j_phi.add_incoming(ir.Constant(i32, 0), b_inner_init)

    cond_inner = b.icmp_signed("<", j_phi, inner_limit)
    b.cbranch(cond_inner, b_body, b_outer_latch)

    b.position_at_end(b_body)
    j64 = b.sext(j_phi, i64)
    jp1 = b.add(j_phi, ir.Constant(i32, 1))
    jp1_64 = b.sext(jp1, i64)

    ptr_j = b.gep(arr, [j64], inbounds=True)
    ptr_jp1 = b.gep(arr, [jp1_64], inbounds=True)

    val_j = b.load(ptr_j)
    val_jp1 = b.load(ptr_jp1)

    if isinstance(T, ir.IntType):
        should_swap = b.icmp_signed(">", val_j, val_jp1)
    else:
        should_swap = b.fcmp_ordered(">", val_j, val_jp1, fastmath=True)

    b.cbranch(should_swap, b_swap, b_inner_latch)

    b.position_at_end(b_swap)
    b.store(val_jp1, ptr_j)
    b.store(val_j, ptr_jp1)
    b.branch(b_inner_latch)

    b.position_at_end(b_inner_latch)
    j_next = b.add(j_phi, ir.Constant(i32, 1))
    j_phi.add_incoming(j_next, b_inner_latch)
    b.branch(b_inner)

    b.position_at_end(b_outer_latch)
    i_next = b.add(i_phi, ir.Constant(i32, 1))
    i_phi.add_incoming(i_next, b_outer_latch)
    b.branch(b_outer)

    b.position_at_end(b_exit)
    b.ret_void()

    return str(mod)

def _materialize(dtype: str) -> int:
    _ensure_target_machine()

    if dtype in _fn_ptr_cache:
        return _fn_ptr_cache[dtype]

    try:
        llvm_ir = _build_bubble_sort_ir(dtype)
        mod = binding.parse_assembly(llvm_ir)
        mod.verify()

        try:
            pm = binding.ModulePassManager()
            pm.add_instruction_combining_pass()
            pm.add_reassociate_pass()
            pm.add_gvn_pass()
            pm.add_cfg_simplification_pass()
            pm.run(mod)
        except AttributeError:
            pass

        engine = binding.create_mcjit_compiler(mod, _target_machine)
        engine.finalize_object()
        engine.run_static_constructors()

        addr = engine.get_function_address(f"bubble_sort_{dtype}")
        if not addr:
            raise RuntimeError(f"Failed to get address for bubble_sort_{dtype}")

        _fn_ptr_cache[dtype] = addr
        _engines[dtype] = engine

        return addr

    except Exception as e:
        raise RuntimeError(f"Failed to materialize function for dtype {dtype}: {e}")
