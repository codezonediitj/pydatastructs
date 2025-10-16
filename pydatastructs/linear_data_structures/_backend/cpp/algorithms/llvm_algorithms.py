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


def get_quick_sort_ptr(dtype: str) -> int:
    dtype = dtype.lower().strip()
    if dtype not in _SUPPORTED:
        raise ValueError(f"Unsupported dtype '{dtype}'. Supported: {list(_SUPPORTED)}")

    return _materialize_quick(dtype)

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


def _build_quick_sort_ir(dtype: str) -> str:
    if dtype not in _SUPPORTED:
        raise ValueError(f"Unsupported dtype '{dtype}'. Supported: {list(_SUPPORTED)}")

    T, _ = _SUPPORTED[dtype]
    i32 = ir.IntType(32)
    i64 = ir.IntType(64)

    mod = ir.Module(name=f"quick_sort_{dtype}_module")
    fn_name = f"quick_sort_{dtype}"

    # void quick_sort(T* arr, int32 low, int32 high)
    fn_ty = ir.FunctionType(ir.VoidType(), [T.as_pointer(), i32, i32])
    fn = ir.Function(mod, fn_ty, name=fn_name)
    arr, low, high = fn.args
    arr.name, low.name, high.name = "arr", "low", "high"

    entry = fn.append_basic_block("entry")
    part = fn.append_basic_block("partition")
    exit = fn.append_basic_block("exit")

    b = ir.IRBuilder(entry)

    # if (low < high)
    cond = b.icmp_signed("<", low, high)
    b.cbranch(cond, part, exit)

    # --- Partition block
    b.position_at_end(part)

    # pivot = arr[high]
    high_64 = b.sext(high, i64)
    pivot_ptr = b.gep(arr, [high_64])
    pivot = b.load(pivot_ptr, name="pivot")

    # i = low - 1
    i = b.alloca(i32, name="i")
    i_init = b.sub(low, ir.Constant(i32, 1))
    b.store(i_init, i)

    # j = low
    j = b.alloca(i32, name="j")
    b.store(low, j)

    loop = fn.append_basic_block("loop")
    after_loop = fn.append_basic_block("after_loop")
    body = fn.append_basic_block("body")
    swap = fn.append_basic_block("swap")
    skip_swap = fn.append_basic_block("skip_swap")

    b.branch(loop)

    # --- Loop: while (j < high)
    b.position_at_end(loop)
    j_val = b.load(j)
    cond = b.icmp_signed("<", j_val, high)
    b.cbranch(cond, body, after_loop)

    # --- Body
    b.position_at_end(body)
    j64 = b.sext(j_val, i64)
    elem_ptr = b.gep(arr, [j64])
    elem = b.load(elem_ptr, name="elem")

    if isinstance(T, ir.IntType):
        cmp = b.icmp_signed("<=", elem, pivot)
    else:
        cmp = b.fcmp_ordered("<=", elem, pivot, fastmath=True)

    b.cbranch(cmp, swap, skip_swap)

    # --- Swap block
    b.position_at_end(swap)
    i_val = b.load(i)
    i_next = b.add(i_val, ir.Constant(i32, 1))
    b.store(i_next, i)

    i64v = b.sext(i_next, i64)
    iptr = b.gep(arr, [i64v])
    ival = b.load(iptr)
    # swap arr[i] and arr[j]
    b.store(elem, iptr)
    b.store(ival, elem_ptr)

    b.branch(skip_swap)

    # --- Skip swap
    b.position_at_end(skip_swap)
    j_next = b.add(j_val, ir.Constant(i32, 1))
    b.store(j_next, j)
    b.branch(loop)

    # --- After loop
    b.position_at_end(after_loop)
    i_val = b.load(i)
    i_plus1 = b.add(i_val, ir.Constant(i32, 1))

    i64v = b.sext(i_plus1, i64)
    iptr = b.gep(arr, [i64v])
    ival = b.load(iptr)

    # swap arr[i+1] and arr[high]
    b.store(pivot, iptr)
    b.store(ival, pivot_ptr)

    # Now i+1 is the partition index
    pi = i_plus1

    # Recursive calls:
    # quick_sort(arr, low, pi - 1)
    low_call = low
    high_call1 = b.sub(pi, ir.Constant(i32, 1))
    b.call(fn, [arr, low_call, high_call1])

    # quick_sort(arr, pi + 1, high)
    low_call2 = b.add(pi, ir.Constant(i32, 1))
    high_call2 = high
    b.call(fn, [arr, low_call2, high_call2])

    b.branch(exit)

    # --- Exit
    b.position_at_end(exit)
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


def _materialize_quick(dtype: str) -> int:
    _ensure_target_machine()

    key = f"quick_{dtype}"
    if key in _fn_ptr_cache:
        return _fn_ptr_cache[key]

    try:
        llvm_ir = _build_quick_sort_ir(dtype)
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

        addr = engine.get_function_address(f"quick_sort_{dtype}")
        if not addr:
            raise RuntimeError(f"Failed to get address for quick_sort_{dtype}")

        _fn_ptr_cache[key] = addr
        _engines[key] = engine

        return addr

    except Exception as e:
        raise RuntimeError(f"Failed to materialize quick sort function for dtype {dtype}: {e}")
