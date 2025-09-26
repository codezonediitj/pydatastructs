import llvmlite.binding as llvm
import llvmlite.ir as ir
from llvmlite import ir
import ctypes
from ctypes import Structure, POINTER, c_void_p, c_int, c_char_p, c_double

llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

class LLVMAdjacencyListGraph:
    def __init__(self):
        self.module = ir.Module(name="adjacency_list_graph")
        self.builder = None

        self.void_type = ir.VoidType()
        self.int_type = ir.IntType(32)
        self.int64_type = ir.IntType(64)
        self.int8_type = ir.IntType(8)
        self.double_type = ir.DoubleType()
        self.bool_type = ir.IntType(1)

        self.int_ptr = self.int_type.as_pointer()
        self.char_ptr = self.int8_type.as_pointer()
        self.void_ptr = self.int8_type.as_pointer()

        triple = self._get_target_triple()
        target = llvm.Target.from_default_triple()
        self.target_machine = target.create_target_machine()
        self.target_data = self.target_machine.target_data
        self.module.triple = triple
        self.module.data_layout = str(self.target_data)

        self._create_structures()

        self._create_function_declarations()

        self._create_graph_functions()

    def _get_target_triple(self):
        import platform
        system = platform.system().lower()
        machine = platform.machine().lower()

        if system == "darwin":  # macOS
            if machine in ["arm64", "aarch64"]:
                return "arm64-apple-darwin"
            else:  # x86_64
                return "x86_64-apple-darwin"
        elif system == "linux":
            if machine in ["arm64", "aarch64"]:
                return "aarch64-unknown-linux-gnu"
            else:  # x86_64
                return "x86_64-unknown-linux-gnu"
        elif system == "windows":
            if machine in ["arm64", "aarch64"]:
                return "aarch64-pc-windows-msvc"
            else:
                return "x86_64-pc-windows-msvc"
        else:
            return llvm.get_default_triple()

    def _create_structures(self):

        self.node_type = ir.LiteralStructType([
            self.int_type,
            self.char_ptr,
            self.int_type,
            self.void_ptr,
            self.int_type,
            self.int_type
        ])

        self.edge_type = ir.LiteralStructType([
            self.node_type.as_pointer(),
            self.node_type.as_pointer(),
            self.double_type
        ])

        self.hash_entry_type = ir.LiteralStructType([
            self.char_ptr,
            self.int_type,
            self.void_ptr,
            self.void_ptr
        ])

        self.graph_type = ir.LiteralStructType([
            self.node_type.as_pointer().as_pointer(),
            self.int_type,
            self.int_type,
            self.void_ptr,
            self.void_ptr,
            self.int_type
        ])

    def _get_target_data(self):
        return self.target_machine.target_data

    def _get_struct_size(self, struct_type):
        return struct_type.get_abi_size(self._get_target_data())

    def _get_pointer_size(self):
        import struct
        return struct.calcsize("P")

    def _create_function_declarations(self):

        malloc_type = ir.FunctionType(self.void_ptr, [self.int64_type])
        self.malloc_func = ir.Function(self.module, malloc_type, name="malloc")

        free_type = ir.FunctionType(self.void_type, [self.void_ptr])
        self.free_func = ir.Function(self.module, free_type, name="free")

        memcpy_type = ir.FunctionType(self.void_ptr, [self.void_ptr, self.void_ptr, self.int64_type])
        self.memcpy_func = ir.Function(self.module, memcpy_type, name="memcpy")

        strlen_type = ir.FunctionType(self.int64_type, [self.char_ptr])
        self.strlen_func = ir.Function(self.module, strlen_type, name="strlen")

    def _create_graph_functions(self):
        self._create_hash_functions()
        self._create_hash_insert()
        self._create_node_functions()
        self._create_graph_init()
        self._create_add_vertex()
        self._create_add_edge()
        self._create_is_adjacent()
        self._create_hash_remove()
        self._create_remove_vertex()
        self._create_remove_edge()
        self._create_graph_cleanup()

    def _compare_strings(self, str1, str2, length):
        entry_block = self.builder.block
        loop_block = self.builder.block.parent.append_basic_block(name="str_cmp_loop")
        check_block = self.builder.block.parent.append_basic_block(name="str_cmp_check")
        true_block = self.builder.block.parent.append_basic_block(name="strings_equal")
        false_block = self.builder.block.parent.append_basic_block(name="strings_not_equal")
        merge_block = self.builder.block.parent.append_basic_block(name="string_cmp_merge")

        i = self.builder.alloca(self.int_type, name="str_cmp_i")
        self.builder.store(ir.Constant(self.int_type, 0), i)
        self.builder.branch(loop_block)

        self.builder.position_at_end(loop_block)
        i_val = self.builder.load(i)
        loop_cond = self.builder.icmp_signed('<', i_val, length)
        self.builder.cbranch(loop_cond, check_block, true_block)

        self.builder.position_at_end(check_block)
        char1_ptr = self.builder.gep(str1, [i_val])
        char2_ptr = self.builder.gep(str2, [i_val])
        char1 = self.builder.load(char1_ptr)
        char2 = self.builder.load(char2_ptr)
        chars_equal = self.builder.icmp_signed('==', char1, char2)

        next_char_block = self.builder.block.parent.append_basic_block(name="next_char")
        self.builder.cbranch(chars_equal, next_char_block, false_block)

        self.builder.position_at_end(next_char_block)
        next_i = self.builder.add(i_val, ir.Constant(self.int_type, 1))
        self.builder.store(next_i, i)
        self.builder.branch(loop_block)

        self.builder.position_at_end(true_block)
        self.builder.branch(merge_block)

        self.builder.position_at_end(false_block)
        self.builder.branch(merge_block)

        self.builder.position_at_end(merge_block)
        phi = self.builder.phi(self.bool_type, name="string_cmp_result")
        phi.add_incoming(ir.Constant(self.bool_type, 1), true_block)
        phi.add_incoming(ir.Constant(self.bool_type, 0), false_block)

        return phi

    def _create_hash_functions(self):
        hash_func_type = ir.FunctionType(self.int_type, [self.char_ptr, self.int_type])
        self.hash_func = ir.Function(self.module, hash_func_type, name="hash_string")

        block = self.hash_func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        str_ptr, str_len = self.hash_func.args
        hash_val = self.builder.alloca(self.int_type, name="hash")
        self.builder.store(ir.Constant(self.int_type, 5381), hash_val)

        i = self.builder.alloca(self.int_type, name="i")
        self.builder.store(ir.Constant(self.int_type, 0), i)

        loop_block = self.hash_func.append_basic_block(name="loop")
        end_block = self.hash_func.append_basic_block(name="end")

        self.builder.branch(loop_block)
        self.builder.position_at_end(loop_block)

        i_val = self.builder.load(i)
        cond = self.builder.icmp_signed('<', i_val, str_len)

        loop_body = self.hash_func.append_basic_block(name="loop_body")
        self.builder.cbranch(cond, loop_body, end_block)

        self.builder.position_at_end(loop_body)
        char_ptr = self.builder.gep(str_ptr, [i_val])
        char_val = self.builder.load(char_ptr)
        char_ext = self.builder.zext(char_val, self.int_type)

        hash_current = self.builder.load(hash_val)
        hash_shifted = self.builder.shl(hash_current, ir.Constant(self.int_type, 5))
        hash_new = self.builder.add(hash_shifted, hash_current)
        hash_final = self.builder.add(hash_new, char_ext)
        self.builder.store(hash_final, hash_val)

        i_next = self.builder.add(i_val, ir.Constant(self.int_type, 1))
        self.builder.store(i_next, i)
        self.builder.branch(loop_block)

        self.builder.position_at_end(end_block)
        result = self.builder.load(hash_val)
        self.builder.ret(result)

        lookup_func_type = ir.FunctionType(self.void_ptr, [self.void_ptr, self.char_ptr, self.int_type])
        self.hash_lookup = ir.Function(self.module, lookup_func_type, name="hash_lookup")

        block = self.hash_lookup.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        table, key, key_len = self.hash_lookup.args

        current = self.builder.alloca(self.void_ptr)
        self.builder.store(table, current)

        loop_block = self.hash_lookup.append_basic_block(name="loop")
        check_block = self.hash_lookup.append_basic_block(name="check")
        found_block = self.hash_lookup.append_basic_block(name="found")
        not_found_block = self.hash_lookup.append_basic_block(name="not_found")

        self.builder.branch(loop_block)
        self.builder.position_at_end(loop_block)

        current_val = self.builder.load(current)
        is_null = self.builder.icmp_unsigned('==', current_val, ir.Constant(self.void_ptr, None))
        self.builder.cbranch(is_null, not_found_block, check_block)

        self.builder.position_at_end(check_block)
        entry_ptr = self.builder.bitcast(current_val, self.hash_entry_type.as_pointer())
        entry_key_ptr = self.builder.gep(entry_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 0)])
        entry_key = self.builder.load(entry_key_ptr)
        entry_key_len_ptr = self.builder.gep(entry_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 1)])
        entry_key_len = self.builder.load(entry_key_len_ptr)

        len_match = self.builder.icmp_unsigned('==', entry_key_len, key_len)

        content_check_block = self.hash_lookup.append_basic_block(name="content_check")
        next_block = self.hash_lookup.append_basic_block(name="next_entry")

        self.builder.cbranch(len_match, content_check_block, next_block)

        self.builder.position_at_end(content_check_block)
        strings_match = self._compare_strings(entry_key, key, key_len)
        self.builder.cbranch(strings_match, found_block, next_block)

        self.builder.position_at_end(next_block)
        next_entry_ptr = self.builder.gep(entry_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 3)])
        next_entry = self.builder.load(next_entry_ptr)
        self.builder.store(next_entry, current)
        self.builder.branch(loop_block)

        self.builder.position_at_end(found_block)
        value_ptr = self.builder.gep(entry_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 2)])
        value = self.builder.load(value_ptr)
        self.builder.ret(value)

        self.builder.position_at_end(not_found_block)
        self.builder.ret(ir.Constant(self.void_ptr, None))

    def _create_node_functions(self):
        create_node_type = ir.FunctionType(self.node_type.as_pointer(), [self.char_ptr, self.int_type, self.int_type])
        self.create_node = ir.Function(self.module, create_node_type, name="create_node")

        block = self.create_node.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        name_ptr, name_len, node_id = self.create_node.args

        node_size = ir.Constant(self.int64_type, self._get_struct_size(self.node_type))
        node_mem = self.builder.call(self.malloc_func, [node_size])
        node_ptr = self.builder.bitcast(node_mem, self.node_type.as_pointer())

        id_ptr = self.builder.gep(node_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 0)])
        self.builder.store(node_id, id_ptr)

        name_buf_size = self.builder.zext(name_len, self.int64_type)
        name_buf = self.builder.call(self.malloc_func, [name_buf_size])
        name_dest = self.builder.bitcast(name_buf, self.char_ptr)
        name_len_64 = self.builder.zext(name_len, self.int64_type)
        self.builder.call(self.memcpy_func, [name_dest, name_ptr, name_len_64])

        name_field_ptr = self.builder.gep(node_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 1)])
        self.builder.store(name_dest, name_field_ptr)

        name_len_ptr = self.builder.gep(node_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 2)])
        self.builder.store(name_len, name_len_ptr)

        adj_ptr = self.builder.gep(node_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 3)])
        self.builder.store(ir.Constant(self.void_ptr, None), adj_ptr)

        adj_count_ptr = self.builder.gep(node_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 4)])
        self.builder.store(ir.Constant(self.int_type, 0), adj_count_ptr)
        adj_cap_ptr = self.builder.gep(node_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 5)])
        self.builder.store(ir.Constant(self.int_type, 0), adj_cap_ptr)

        self.builder.ret(node_ptr)

    def _create_graph_init(self):
        init_type = ir.FunctionType(self.graph_type.as_pointer(), [])
        self.graph_init = ir.Function(self.module, init_type, name="graph_init")

        block = self.graph_init.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        graph_size = ir.Constant(self.int64_type, self._get_struct_size(self.graph_type))
        graph_mem = self.builder.call(self.malloc_func, [graph_size])
        graph_ptr = self.builder.bitcast(graph_mem, self.graph_type.as_pointer())

        nodes_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 0)])
        self.builder.store(ir.Constant(self.node_type.as_pointer().as_pointer(), None), nodes_ptr)

        count_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 1)])
        self.builder.store(ir.Constant(self.int_type, 0), count_ptr)

        cap_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 2)])
        self.builder.store(ir.Constant(self.int_type, 0), cap_ptr)

        node_map_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 3)])
        self.builder.store(ir.Constant(self.void_ptr, None), node_map_ptr)

        edge_map_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 4)])
        self.builder.store(ir.Constant(self.void_ptr, None), edge_map_ptr)

        next_id_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 5)])
        self.builder.store(ir.Constant(self.int_type, 0), next_id_ptr)

        self.builder.ret(graph_ptr)

    def _create_add_vertex(self):
        add_vertex_type = ir.FunctionType(self.int_type, [self.graph_type.as_pointer(), self.char_ptr, self.int_type])
        self.add_vertex = ir.Function(self.module, add_vertex_type, name="add_vertex")

        block = self.add_vertex.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        graph_ptr, name_ptr, name_len = self.add_vertex.args

        node_map_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 3)])
        node_map = self.builder.load(node_map_ptr)
        existing_node = self.builder.call(self.hash_lookup, [node_map, name_ptr, name_len])

        exists_block = self.add_vertex.append_basic_block(name="node_exists")
        create_block = self.add_vertex.append_basic_block(name="create_node")

        is_null = self.builder.icmp_signed('==', existing_node, ir.Constant(self.void_ptr, None))
        self.builder.cbranch(is_null, create_block, exists_block)

        self.builder.position_at_end(exists_block)
        self.builder.ret(ir.Constant(self.int_type, -1))

        self.builder.position_at_end(create_block)

        next_id_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 5)])
        current_id = self.builder.load(next_id_ptr)
        new_id = self.builder.add(current_id, ir.Constant(self.int_type, 1))
        self.builder.store(new_id, next_id_ptr)

        name_size = self.builder.add(name_len, ir.Constant(self.int_type, 1))
        name_size_64 = self.builder.zext(name_size, self.int64_type)
        name_copy = self.builder.call(self.malloc_func, [name_size_64])
        name_copy_typed = self.builder.bitcast(name_copy, self.char_ptr)

        name_len_64 = self.builder.zext(name_len, self.int64_type)
        self.builder.call(self.memcpy_func, [name_copy, name_ptr, name_len_64])

        null_term_ptr = self.builder.gep(name_copy_typed, [name_len])
        self.builder.store(ir.Constant(self.int8_type, 0), null_term_ptr)

        node_ptr = self.builder.call(self.create_node, [name_copy_typed, name_len, current_id])

        nodes_array_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 0)])
        count_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 1)])
        capacity_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 2)])

        current_count = self.builder.load(count_ptr)
        current_capacity = self.builder.load(capacity_ptr)

        resize_block = self.add_vertex.append_basic_block(name="resize_array")
        add_node_block = self.add_vertex.append_basic_block(name="add_node")

        needs_resize = self.builder.icmp_signed('>=', current_count, current_capacity)
        self.builder.cbranch(needs_resize, resize_block, add_node_block)

        self.builder.position_at_end(resize_block)
        new_capacity = self.builder.select(
            self.builder.icmp_signed('==', current_capacity, ir.Constant(self.int_type, 0)),
            ir.Constant(self.int_type, 4),
            self.builder.mul(current_capacity, ir.Constant(self.int_type, 2))
        )

        target_data = self._get_target_data()
        ptr_type = self.node_type.as_pointer()
        ptr_size = ir.Constant(self.int64_type, self._get_pointer_size())

        new_size_64 = self.builder.mul(self.builder.zext(new_capacity, self.int64_type), ptr_size)
        new_array_mem = self.builder.call(self.malloc_func, [new_size_64])
        new_array = self.builder.bitcast(new_array_mem, self.node_type.as_pointer().as_pointer())

        copy_block = self.add_vertex.append_basic_block(name="copy_nodes")
        no_copy_block = self.add_vertex.append_basic_block(name="no_copy")

        has_existing = self.builder.icmp_signed('>', current_count, ir.Constant(self.int_type, 0))
        self.builder.cbranch(has_existing, copy_block, no_copy_block)

        self.builder.position_at_end(copy_block)
        old_array = self.builder.load(nodes_array_ptr)
        old_size_64 = self.builder.mul(self.builder.zext(current_count, self.int64_type), ptr_size)
        old_array_void = self.builder.bitcast(old_array, self.void_ptr)
        new_array_void = self.builder.bitcast(new_array, self.void_ptr)
        self.builder.call(self.memcpy_func, [new_array_void, old_array_void, old_size_64])

        self.builder.call(self.free_func, [old_array_void])
        self.builder.branch(no_copy_block)

        self.builder.position_at_end(no_copy_block)
        self.builder.store(new_array, nodes_array_ptr)
        self.builder.store(new_capacity, capacity_ptr)
        self.builder.branch(add_node_block)

        self.builder.position_at_end(add_node_block)
        nodes_array = self.builder.load(nodes_array_ptr)
        current_count_final = self.builder.load(count_ptr)
        node_slot = self.builder.gep(nodes_array, [current_count_final])
        self.builder.store(node_ptr, node_slot)

        new_count = self.builder.add(current_count_final, ir.Constant(self.int_type, 1))
        self.builder.store(new_count, count_ptr)

        self.builder.call(self.hash_insert, [node_map_ptr, name_copy_typed, name_len,
                                            self.builder.bitcast(node_ptr, self.void_ptr)])

        self.builder.ret(ir.Constant(self.int_type, 0))

    def _create_add_edge(self):
        add_edge_type = ir.FunctionType(self.int_type,
            [self.graph_type.as_pointer(), self.char_ptr, self.int_type,
            self.char_ptr, self.int_type, self.double_type])
        self.add_edge = ir.Function(self.module, add_edge_type, name="add_edge")

        block = self.add_edge.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        graph_ptr, src_name, src_len, tgt_name, tgt_len, weight = self.add_edge.args

        node_map_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 3)])
        node_map = self.builder.load(node_map_ptr)

        src_node_void = self.builder.call(self.hash_lookup, [node_map, src_name, src_len])
        src_exists = self.builder.icmp_signed('!=', src_node_void, ir.Constant(self.void_ptr, None))

        src_found_block = self.add_edge.append_basic_block(name="src_found")
        error_block = self.add_edge.append_basic_block(name="error")

        self.builder.cbranch(src_exists, src_found_block, error_block)

        self.builder.position_at_end(error_block)
        self.builder.ret(ir.Constant(self.int_type, -1))

        self.builder.position_at_end(src_found_block)
        tgt_node_void = self.builder.call(self.hash_lookup, [node_map, tgt_name, tgt_len])
        tgt_exists = self.builder.icmp_signed('!=', tgt_node_void, ir.Constant(self.void_ptr, None))

        tgt_found_block = self.add_edge.append_basic_block(name="tgt_found")
        error2_block = self.add_edge.append_basic_block(name="error2")

        self.builder.cbranch(tgt_exists, tgt_found_block, error2_block)

        self.builder.position_at_end(error2_block)
        self.builder.ret(ir.Constant(self.int_type, -2))

        self.builder.position_at_end(tgt_found_block)
        src_node_ptr = self.builder.bitcast(src_node_void, self.node_type.as_pointer())
        tgt_node_ptr = self.builder.bitcast(tgt_node_void, self.node_type.as_pointer())

        edge_key_len = self.builder.add(self.builder.add(src_len, tgt_len), ir.Constant(self.int_type, 2))
        edge_key_len_64 = self.builder.zext(edge_key_len, self.int64_type)
        edge_key_mem = self.builder.call(self.malloc_func, [edge_key_len_64])
        edge_key = self.builder.bitcast(edge_key_mem, self.char_ptr)

        src_len_64 = self.builder.zext(src_len, self.int64_type)
        self.builder.call(self.memcpy_func, [edge_key, src_name, src_len_64])

        underscore_ptr = self.builder.gep(edge_key, [src_len])
        self.builder.store(ir.Constant(self.int8_type, ord('_')), underscore_ptr)

        tgt_start_ptr = self.builder.gep(edge_key, [self.builder.add(src_len, ir.Constant(self.int_type, 1))])
        tgt_len_64 = self.builder.zext(tgt_len, self.int64_type)
        self.builder.call(self.memcpy_func, [tgt_start_ptr, tgt_name, tgt_len_64])

        final_key_len = self.builder.sub(edge_key_len, ir.Constant(self.int_type, 1))
        null_ptr = self.builder.gep(edge_key, [final_key_len])
        self.builder.store(ir.Constant(self.int8_type, 0), null_ptr)

        edge_map_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 4)])
        edge_map = self.builder.load(edge_map_ptr)
        existing_edge = self.builder.call(self.hash_lookup, [edge_map, edge_key, final_key_len])

        edge_exists_block = self.add_edge.append_basic_block(name="edge_exists")
        create_edge_block = self.add_edge.append_basic_block(name="create_edge")

        edge_exists = self.builder.icmp_signed('!=', existing_edge, ir.Constant(self.void_ptr, None))
        self.builder.cbranch(edge_exists, edge_exists_block, create_edge_block)

        self.builder.position_at_end(edge_exists_block)
        existing_edge_ptr = self.builder.bitcast(existing_edge, self.edge_type.as_pointer())
        weight_ptr = self.builder.gep(existing_edge_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 2)])
        self.builder.store(weight, weight_ptr)

        self.builder.call(self.free_func, [edge_key_mem])
        self.builder.ret(ir.Constant(self.int_type, 0))

        self.builder.position_at_end(create_edge_block)

        edge_size = ir.Constant(self.int64_type, self._get_struct_size(self.edge_type))
        edge_mem = self.builder.call(self.malloc_func, [edge_size])
        edge_ptr = self.builder.bitcast(edge_mem, self.edge_type.as_pointer())

        src_field_ptr = self.builder.gep(edge_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 0)])
        self.builder.store(src_node_ptr, src_field_ptr)

        tgt_field_ptr = self.builder.gep(edge_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 1)])
        self.builder.store(tgt_node_ptr, tgt_field_ptr)

        weight_field_ptr = self.builder.gep(edge_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 2)])
        self.builder.store(weight, weight_field_ptr)

        self.builder.call(self.hash_insert, [edge_map_ptr, edge_key, final_key_len,
                                            self.builder.bitcast(edge_ptr, self.void_ptr)])

        self._add_to_adjacency_list(src_node_ptr, tgt_node_ptr)

        self.builder.ret(ir.Constant(self.int_type, 0))

    def _add_to_adjacency_list(self, src_node_ptr, tgt_node_ptr):
        adj_list_ptr = self.builder.gep(src_node_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 3)])
        adj_count_ptr = self.builder.gep(src_node_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 4)])
        adj_cap_ptr = self.builder.gep(src_node_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 5)])

        current_count = self.builder.load(adj_count_ptr)
        tgt_node_name_ptr = self.builder.gep(tgt_node_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 1)])
        tgt_node_name = self.builder.load(tgt_node_name_ptr)
        tgt_node_name_len_ptr = self.builder.gep(tgt_node_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 2)])
        tgt_node_name_len = self.builder.load(tgt_node_name_len_ptr)

        adj_list_void = self.builder.load(adj_list_ptr)
        adj_list_exists = self.builder.icmp_signed('!=', adj_list_void, ir.Constant(self.void_ptr, None))

        check_duplicates_block = self.builder.block.parent.append_basic_block(name="check_duplicates")
        proceed_add_block = self.builder.block.parent.append_basic_block(name="proceed_add")
        self.builder.cbranch(adj_list_exists, check_duplicates_block, proceed_add_block)

        self.builder.position_at_end(check_duplicates_block)
        adj_list_typed = self.builder.bitcast(adj_list_void, self.node_type.as_pointer().as_pointer())
        dup_i = self.builder.alloca(self.int_type, name="dup_check_i")
        self.builder.store(ir.Constant(self.int_type, 0), dup_i)

        dup_loop_block = self.builder.block.parent.append_basic_block(name="dup_check_loop")
        dup_check_block = self.builder.block.parent.append_basic_block(name="dup_check_node")
        dup_next_block = self.builder.block.parent.append_basic_block(name="dup_next")
        self.builder.branch(dup_loop_block)

        self.builder.position_at_end(dup_loop_block)
        dup_i_val = self.builder.load(dup_i)
        current_count_loop = self.builder.load(adj_count_ptr)
        dup_loop_condition = self.builder.icmp_signed('<', dup_i_val, current_count_loop)
        self.builder.cbranch(dup_loop_condition, dup_check_block, proceed_add_block)

        self.builder.position_at_end(dup_check_block)
        existing_node_ptr = self.builder.gep(adj_list_typed, [dup_i_val])
        existing_node = self.builder.load(existing_node_ptr)
        existing_name_ptr = self.builder.gep(existing_node, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 1)])
        existing_name = self.builder.load(existing_name_ptr)
        existing_name_len_ptr = self.builder.gep(existing_node, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 2)])
        existing_name_len = self.builder.load(existing_name_len_ptr)

        len_match = self.builder.icmp_signed('==', existing_name_len, tgt_node_name_len)
        dup_content_check_block = self.builder.block.parent.append_basic_block(name="dup_content_check")
        self.builder.cbranch(len_match, dup_content_check_block, dup_next_block)

        self.builder.position_at_end(dup_content_check_block)
        names_match = self._compare_strings(existing_name, tgt_node_name, tgt_node_name_len)
        self.builder.cbranch(names_match, proceed_add_block, dup_next_block)

        self.builder.position_at_end(dup_next_block)
        next_dup_i = self.builder.add(dup_i_val, ir.Constant(self.int_type, 1))
        self.builder.store(next_dup_i, dup_i)
        self.builder.branch(dup_loop_block)

        self.builder.position_at_end(proceed_add_block)
        current_capacity = self.builder.load(adj_cap_ptr)
        current_count_final = self.builder.load(adj_count_ptr)
        needs_resize = self.builder.icmp_signed('>=', current_count_final, current_capacity)

        resize_adj_block = self.builder.block.parent.append_basic_block(name="resize_adj")
        add_adj_block = self.builder.block.parent.append_basic_block(name="add_adj")
        self.builder.cbranch(needs_resize, resize_adj_block, add_adj_block)

        self.builder.position_at_end(resize_adj_block)
        new_capacity = self.builder.select(
            self.builder.icmp_signed('==', current_capacity, ir.Constant(self.int_type, 0)),
            ir.Constant(self.int_type, 1),
            self.builder.mul(current_capacity, ir.Constant(self.int_type, 2))
        )
        ptr_size = ir.Constant(self.int64_type, self._get_pointer_size())
        new_size_bytes = self.builder.mul(self.builder.zext(new_capacity, self.int64_type), ptr_size)
        new_array_mem = self.builder.call(self.malloc_func, [new_size_bytes])

        old_adj_list = self.builder.load(adj_list_ptr)
        copy_needed = self.builder.icmp_signed('>', current_count_final, ir.Constant(self.int_type, 0))
        copy_block = self.builder.block.parent.append_basic_block(name="copy_existing")
        store_block = self.builder.block.parent.append_basic_block(name="store_new_array")
        self.builder.cbranch(copy_needed, copy_block, store_block)

        self.builder.position_at_end(copy_block)
        old_size_bytes = self.builder.mul(self.builder.zext(current_count_final, self.int64_type), ptr_size)
        self.builder.call(self.memcpy_func, [new_array_mem, old_adj_list, old_size_bytes])
        self.builder.call(self.free_func, [old_adj_list])
        self.builder.branch(store_block)

        self.builder.position_at_end(store_block)
        self.builder.store(new_array_mem, adj_list_ptr)
        self.builder.store(new_capacity, adj_cap_ptr)
        self.builder.branch(add_adj_block)

        self.builder.position_at_end(add_adj_block)
        adj_array = self.builder.load(adj_list_ptr)
        adj_array_typed = self.builder.bitcast(adj_array, self.node_type.as_pointer().as_pointer())
        target_addr = self.builder.gep(adj_array_typed, [current_count_final])
        self.builder.store(tgt_node_ptr, target_addr)
        new_count = self.builder.add(current_count_final, ir.Constant(self.int_type, 1))
        self.builder.store(new_count, adj_count_ptr)

    def _create_hash_insert(self):
        insert_func_type = ir.FunctionType(self.int_type,
            [self.void_ptr.as_pointer(), self.char_ptr, self.int_type, self.void_ptr])
        self.hash_insert = ir.Function(self.module, insert_func_type, name="hash_insert")

        block = self.hash_insert.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        table_ptr, key, key_len, value = self.hash_insert.args

        entry_size = ir.Constant(self.int64_type, self._get_struct_size(self.hash_entry_type))
        entry_mem = self.builder.call(self.malloc_func, [entry_size])
        entry_ptr = self.builder.bitcast(entry_mem, self.hash_entry_type.as_pointer())

        key_field_ptr = self.builder.gep(entry_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 0)])
        self.builder.store(key, key_field_ptr)

        key_len_field_ptr = self.builder.gep(entry_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 1)])
        self.builder.store(key_len, key_len_field_ptr)

        value_field_ptr = self.builder.gep(entry_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 2)])
        self.builder.store(value, value_field_ptr)

        old_head = self.builder.load(table_ptr)
        next_field_ptr = self.builder.gep(entry_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 3)])
        self.builder.store(old_head, next_field_ptr)

        entry_void = self.builder.bitcast(entry_ptr, self.void_ptr)
        self.builder.store(entry_void, table_ptr)

        self.builder.ret(ir.Constant(self.int_type, 0))

    def _create_is_adjacent(self):
        is_adj_type = ir.FunctionType(
            self.bool_type,
            [self.graph_type.as_pointer(), self.char_ptr, self.int_type,
            self.char_ptr, self.int_type]
        )
        self.is_adjacent = ir.Function(self.module, is_adj_type, name="is_adjacent")

        entry_block = self.is_adjacent.append_basic_block("entry")
        node1_found_block = self.is_adjacent.append_basic_block("node1_found")
        check_adjacency_block = self.is_adjacent.append_basic_block("check_adjacency")
        search_adj_block = self.is_adjacent.append_basic_block("search_adj")
        adj_loop_block = self.is_adjacent.append_basic_block("adj_loop")
        adj_check_block = self.is_adjacent.append_basic_block("adj_check")
        adj_next_block = self.is_adjacent.append_basic_block("adj_next")
        content_check_block = self.is_adjacent.append_basic_block("content_check")
        adj_loop_end_block = self.is_adjacent.append_basic_block("adj_loop_end")
        true_block = self.is_adjacent.append_basic_block("return_true")
        false_block = self.is_adjacent.append_basic_block("return_false")

        self.builder.position_at_end(entry_block)
        graph_ptr, node1_name, node1_name_len, node2_name, node2_name_len = self.is_adjacent.args

        node_map_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 3)])
        node_map = self.builder.load(node_map_ptr)

        node1_void = self.builder.call(self.hash_lookup, [node_map, node1_name, node1_name_len])
        node1_exists = self.builder.icmp_signed('!=', node1_void, ir.Constant(self.void_ptr, None))
        self.builder.cbranch(node1_exists, node1_found_block, false_block)

        self.builder.position_at_end(node1_found_block)
        node2_void = self.builder.call(self.hash_lookup, [node_map, node2_name, node2_name_len])
        node2_exists = self.builder.icmp_signed('!=', node2_void, ir.Constant(self.void_ptr, None))
        self.builder.cbranch(node2_exists, check_adjacency_block, false_block)

        self.builder.position_at_end(check_adjacency_block)
        node1_ptr = self.builder.bitcast(node1_void, self.node_type.as_pointer())
        node2_ptr = self.builder.bitcast(node2_void, self.node_type.as_pointer())

        adj_list_ptr = self.builder.gep(node1_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 3)])
        adj_count_ptr = self.builder.gep(node1_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 4)])

        adj_list_void = self.builder.load(adj_list_ptr)
        adj_count = self.builder.load(adj_count_ptr)

        adj_exists = self.builder.icmp_signed('!=', adj_list_void, ir.Constant(self.void_ptr, None))
        count_positive = self.builder.icmp_signed('>', adj_count, ir.Constant(self.int_type, 0))
        should_search = self.builder.and_(adj_exists, count_positive)
        self.builder.cbranch(should_search, search_adj_block, false_block)

        self.builder.position_at_end(search_adj_block)
        adj_array_typed = self.builder.bitcast(adj_list_void, self.node_type.as_pointer().as_pointer())
        i = self.builder.alloca(self.int_type, name="i")
        self.builder.store(ir.Constant(self.int_type, 0), i)
        self.builder.branch(adj_loop_block)

        self.builder.position_at_end(adj_loop_block)
        i_val = self.builder.load(i)
        loop_cond = self.builder.icmp_signed('<', i_val, adj_count)
        self.builder.cbranch(loop_cond, adj_check_block, adj_loop_end_block)

        self.builder.position_at_end(adj_check_block)
        entry_ptr = self.builder.gep(adj_array_typed, [i_val])
        adj_node = self.builder.load(entry_ptr)

        adj_node_name_ptr = self.builder.gep(adj_node, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 1)])
        adj_node_name = self.builder.load(adj_node_name_ptr)
        adj_node_name_len_ptr = self.builder.gep(adj_node, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 2)])
        adj_node_name_len = self.builder.load(adj_node_name_len_ptr)

        len_match = self.builder.icmp_signed('==', adj_node_name_len, node2_name_len)
        self.builder.cbranch(len_match, content_check_block, adj_next_block)

        self.builder.position_at_end(content_check_block)
        names_match = self._compare_strings(adj_node_name, node2_name, node2_name_len)
        self.builder.cbranch(names_match, true_block, adj_next_block)

        self.builder.position_at_end(adj_next_block)
        next_i = self.builder.add(i_val, ir.Constant(self.int_type, 1))
        self.builder.store(next_i, i)
        self.builder.branch(adj_loop_block)

        self.builder.position_at_end(adj_loop_end_block)
        self.builder.ret(ir.Constant(self.bool_type, 0))

        self.builder.position_at_end(true_block)
        self.builder.ret(ir.Constant(self.bool_type, 1))

        self.builder.position_at_end(false_block)
        self.builder.ret(ir.Constant(self.bool_type, 0))


    def _create_remove_vertex(self):

        remove_vertex_type = ir.FunctionType(self.int_type,
            [self.graph_type.as_pointer(), self.char_ptr, self.int_type])
        self.remove_vertex = ir.Function(self.module, remove_vertex_type, name="remove_vertex")

        block = self.remove_vertex.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        graph_ptr, name_ptr, name_len = self.remove_vertex.args

        node_map_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 3)])
        node_map = self.builder.load(node_map_ptr)
        node_void = self.builder.call(self.hash_lookup, [node_map, name_ptr, name_len])

        node_found_block = self.remove_vertex.append_basic_block(name="node_found")
        error_block = self.remove_vertex.append_basic_block(name="error")

        node_exists = self.builder.icmp_signed('!=', node_void, ir.Constant(self.void_ptr, None))
        self.builder.cbranch(node_exists, node_found_block, error_block)

        self.builder.position_at_end(error_block)
        self.builder.ret(ir.Constant(self.int_type, -1))

        self.builder.position_at_end(node_found_block)
        node_to_remove = self.builder.bitcast(node_void, self.node_type.as_pointer())

        node_id_ptr = self.builder.gep(node_to_remove, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 0)])
        node_id = self.builder.load(node_id_ptr)

        self._remove_from_nodes_array(graph_ptr, node_to_remove)

        self.builder.call(self.hash_remove, [node_map_ptr, name_ptr, name_len])

        self._remove_all_edges_for_vertex(graph_ptr, name_ptr, name_len)

        self._remove_from_all_adjacency_lists(graph_ptr, name_ptr, name_len)

        adj_list_ptr = self.builder.gep(node_to_remove, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 3)])
        adj_list = self.builder.load(adj_list_ptr)
        adj_list_not_null = self.builder.icmp_signed('!=', adj_list, ir.Constant(self.void_ptr, None))

        free_adj_block = self.remove_vertex.append_basic_block(name="free_adj")
        free_node_block = self.remove_vertex.append_basic_block(name="free_node")

        self.builder.cbranch(adj_list_not_null, free_adj_block, free_node_block)

        self.builder.position_at_end(free_adj_block)
        self.builder.call(self.free_func, [adj_list])
        self.builder.branch(free_node_block)

        self.builder.position_at_end(free_node_block)
        node_name_ptr = self.builder.gep(node_to_remove, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 1)])
        node_name = self.builder.load(node_name_ptr)
        node_name_void = self.builder.bitcast(node_name, self.void_ptr)
        self.builder.call(self.free_func, [node_name_void])

        node_void_for_free = self.builder.bitcast(node_to_remove, self.void_ptr)
        self.builder.call(self.free_func, [node_void_for_free])

        self.builder.ret(ir.Constant(self.int_type, 0))

    def _create_remove_edge(self):
        remove_edge_type = ir.FunctionType(self.int_type,
            [self.graph_type.as_pointer(), self.char_ptr, self.int_type, self.char_ptr, self.int_type])
        self.remove_edge = ir.Function(self.module, remove_edge_type, name="remove_edge")

        block = self.remove_edge.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        graph_ptr, src_name, src_len, tgt_name, tgt_len = self.remove_edge.args
        node_map_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 3)])
        node_map = self.builder.load(node_map_ptr)

        src_node_void = self.builder.call(self.hash_lookup, [node_map, src_name, src_len])
        src_exists = self.builder.icmp_signed('!=', src_node_void, ir.Constant(self.void_ptr, None))

        src_found_block = self.remove_edge.append_basic_block(name="src_found")
        error_block = self.remove_edge.append_basic_block(name="error")

        self.builder.cbranch(src_exists, src_found_block, error_block)
        self.builder.position_at_end(error_block)
        self.builder.ret(ir.Constant(self.int_type, -1))
        self.builder.position_at_end(src_found_block)
        tgt_node_void = self.builder.call(self.hash_lookup, [node_map, tgt_name, tgt_len])
        tgt_exists = self.builder.icmp_signed('!=', tgt_node_void, ir.Constant(self.void_ptr, None))

        both_found_block = self.remove_edge.append_basic_block(name="both_found")
        error2_block = self.remove_edge.append_basic_block(name="error2")

        self.builder.cbranch(tgt_exists, both_found_block, error2_block)
        self.builder.position_at_end(error2_block)
        self.builder.ret(ir.Constant(self.int_type, -2))

        self.builder.position_at_end(both_found_block)
        src_node_ptr = self.builder.bitcast(src_node_void, self.node_type.as_pointer())
        tgt_node_ptr = self.builder.bitcast(tgt_node_void, self.node_type.as_pointer())

        edge_key_len = self.builder.add(self.builder.add(src_len, tgt_len), ir.Constant(self.int_type, 2))
        edge_key_len_64 = self.builder.zext(edge_key_len, self.int64_type)
        edge_key_mem = self.builder.call(self.malloc_func, [edge_key_len_64])
        edge_key = self.builder.bitcast(edge_key_mem, self.char_ptr)

        src_len_64 = self.builder.zext(src_len, self.int64_type)
        self.builder.call(self.memcpy_func, [edge_key, src_name, src_len_64])

        underscore_ptr = self.builder.gep(edge_key, [src_len])
        self.builder.store(ir.Constant(self.int8_type, ord('_')), underscore_ptr)

        tgt_start_ptr = self.builder.gep(edge_key, [self.builder.add(src_len, ir.Constant(self.int_type, 1))])
        tgt_len_64 = self.builder.zext(tgt_len, self.int64_type)
        self.builder.call(self.memcpy_func, [tgt_start_ptr, tgt_name, tgt_len_64])

        final_key_len = self.builder.sub(edge_key_len, ir.Constant(self.int_type, 1))
        null_ptr = self.builder.gep(edge_key, [final_key_len])
        self.builder.store(ir.Constant(self.int8_type, 0), null_ptr)

        edge_map_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 4)])
        edge_map = self.builder.load(edge_map_ptr)

        edge_to_remove = self.builder.call(self.hash_lookup, [edge_map, edge_key, final_key_len])
        edge_exists = self.builder.icmp_signed('!=', edge_to_remove, ir.Constant(self.void_ptr, None))

        remove_edge_block = self.remove_edge.append_basic_block(name="remove_edge_data")
        cleanup_block = self.remove_edge.append_basic_block(name="cleanup")

        self.builder.cbranch(edge_exists, remove_edge_block, cleanup_block)

        self.builder.position_at_end(remove_edge_block)
        self.builder.call(self.free_func, [edge_to_remove])
        self.builder.branch(cleanup_block)

        self.builder.position_at_end(cleanup_block)
        self.builder.call(self.hash_remove, [edge_map_ptr, edge_key, final_key_len])

        self._remove_from_adjacency_list(src_node_ptr, tgt_node_ptr)

        self.builder.call(self.free_func, [edge_key_mem])

        self.builder.ret(ir.Constant(self.int_type, 0))

    def _remove_from_nodes_array(self, graph_ptr, node_to_remove):
        nodes_array_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 0)])
        count_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 1)])

        nodes_array = self.builder.load(nodes_array_ptr)
        current_count = self.builder.load(count_ptr)

        i = self.builder.alloca(self.int_type, name="i")
        self.builder.store(ir.Constant(self.int_type, 0), i)

        loop_block = self.builder.block.parent.append_basic_block(name="find_loop")
        check_block = self.builder.block.parent.append_basic_block(name="check_node")
        found_block = self.builder.block.parent.append_basic_block(name="found_node")
        shift_block = self.builder.block.parent.append_basic_block(name="shift_elements")
        done_block = self.builder.block.parent.append_basic_block(name="done_remove")

        self.builder.branch(loop_block)

        self.builder.position_at_end(loop_block)
        i_val = self.builder.load(i)
        loop_condition = self.builder.icmp_signed('<', i_val, current_count)
        self.builder.cbranch(loop_condition, check_block, done_block)

        self.builder.position_at_end(check_block)
        current_node_ptr = self.builder.gep(nodes_array, [i_val])
        current_node = self.builder.load(current_node_ptr)
        is_match = self.builder.icmp_signed('==', current_node, node_to_remove)

        next_iter_block = self.builder.block.parent.append_basic_block(name="next_iter")
        self.builder.cbranch(is_match, found_block, next_iter_block)

        self.builder.position_at_end(next_iter_block)
        next_i = self.builder.add(i_val, ir.Constant(self.int_type, 1))
        self.builder.store(next_i, i)
        self.builder.branch(loop_block)

        self.builder.position_at_end(found_block)
        shift_i = self.builder.alloca(self.int_type, name="shift_i")
        self.builder.store(i_val, shift_i)
        self.builder.branch(shift_block)

        self.builder.position_at_end(shift_block)
        shift_i_val = self.builder.load(shift_i)
        next_idx = self.builder.add(shift_i_val, ir.Constant(self.int_type, 1))
        shift_condition = self.builder.icmp_signed('<', next_idx, current_count)

        do_shift_block = self.builder.block.parent.append_basic_block(name="do_shift")
        finish_shift_block = self.builder.block.parent.append_basic_block(name="finish_shift")

        self.builder.cbranch(shift_condition, do_shift_block, finish_shift_block)

        self.builder.position_at_end(do_shift_block)
        src_ptr = self.builder.gep(nodes_array, [next_idx])
        dst_ptr = self.builder.gep(nodes_array, [shift_i_val])
        node_to_shift = self.builder.load(src_ptr)
        self.builder.store(node_to_shift, dst_ptr)

        self.builder.store(next_idx, shift_i)
        self.builder.branch(shift_block)

        self.builder.position_at_end(finish_shift_block)
        new_count = self.builder.sub(current_count, ir.Constant(self.int_type, 1))
        self.builder.store(new_count, count_ptr)
        self.builder.branch(done_block)

        self.builder.position_at_end(done_block)

    def _remove_from_all_adjacency_lists(self, graph_ptr, vertex_name, vertex_name_len):
        nodes_array_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 0)])
        count_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 1)])

        nodes_array = self.builder.load(nodes_array_ptr)
        current_count = self.builder.load(count_ptr)

        i = self.builder.alloca(self.int_type, name="node_i")
        self.builder.store(ir.Constant(self.int_type, 0), i)

        node_loop_block = self.builder.block.parent.append_basic_block(name="node_loop")
        process_node_block = self.builder.block.parent.append_basic_block(name="process_node")
        next_node_block = self.builder.block.parent.append_basic_block(name="next_node")
        done_adj_cleanup = self.builder.block.parent.append_basic_block(name="done_adj_cleanup")

        self.builder.branch(node_loop_block)

        self.builder.position_at_end(node_loop_block)
        i_val = self.builder.load(i)
        loop_condition = self.builder.icmp_signed('<', i_val, current_count)
        self.builder.cbranch(loop_condition, process_node_block, done_adj_cleanup)

        self.builder.position_at_end(process_node_block)
        current_node_ptr = self.builder.gep(nodes_array, [i_val])
        current_node = self.builder.load(current_node_ptr)

        self._remove_vertex_from_node_adjacency(current_node, vertex_name, vertex_name_len)

        self.builder.branch(next_node_block)

        self.builder.position_at_end(next_node_block)
        next_i = self.builder.add(i_val, ir.Constant(self.int_type, 1))
        self.builder.store(next_i, i)
        self.builder.branch(node_loop_block)

        self.builder.position_at_end(done_adj_cleanup)

    def _remove_from_adjacency_list(self, src_node_ptr, tgt_node_ptr):
        tgt_node_name_ptr = self.builder.gep(tgt_node_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 1)])
        tgt_node_name = self.builder.load(tgt_node_name_ptr)
        tgt_node_name_len_ptr = self.builder.gep(tgt_node_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 2)])
        tgt_node_name_len = self.builder.load(tgt_node_name_len_ptr)

        adj_list_ptr = self.builder.gep(src_node_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 3)])
        adj_count_ptr = self.builder.gep(src_node_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 4)])

        adj_list_void = self.builder.load(adj_list_ptr)
        adj_count = self.builder.load(adj_count_ptr)

        adj_list_typed = self.builder.bitcast(adj_list_void, self.node_type.as_pointer().as_pointer())

        i = self.builder.alloca(self.int_type, name="adj_i")
        self.builder.store(ir.Constant(self.int_type, 0), i)

        adj_loop_block = self.builder.block.parent.append_basic_block(name="adj_find_loop")
        adj_check_block = self.builder.block.parent.append_basic_block(name="adj_check")
        adj_found_block = self.builder.block.parent.append_basic_block(name="adj_found")
        adj_shift_block = self.builder.block.parent.append_basic_block(name="adj_shift")
        adj_next_block = self.builder.block.parent.append_basic_block(name="adj_next")
        adj_done_block = self.builder.block.parent.append_basic_block(name="adj_done")

        self.builder.branch(adj_loop_block)

        self.builder.position_at_end(adj_loop_block)
        i_val = self.builder.load(i)
        loop_condition = self.builder.icmp_signed('<', i_val, adj_count)
        self.builder.cbranch(loop_condition, adj_check_block, adj_done_block)

        self.builder.position_at_end(adj_check_block)
        adj_entry_ptr = self.builder.gep(adj_list_typed, [i_val])
        adj_node = self.builder.load(adj_entry_ptr)

        adj_node_name_ptr = self.builder.gep(adj_node, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 1)])
        adj_node_name = self.builder.load(adj_node_name_ptr)
        adj_node_name_len_ptr = self.builder.gep(adj_node, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 2)])
        adj_node_name_len = self.builder.load(adj_node_name_len_ptr)

        len_match = self.builder.icmp_signed('==', adj_node_name_len, tgt_node_name_len)

        content_check_block = self.builder.block.parent.append_basic_block(name="adj_content_check")

        self.builder.cbranch(len_match, content_check_block, adj_next_block)

        self.builder.position_at_end(content_check_block)
        names_match = self._compare_strings(adj_node_name, tgt_node_name, tgt_node_name_len)
        self.builder.cbranch(names_match, adj_found_block, adj_next_block)

        self.builder.position_at_end(adj_found_block)
        shift_i = self.builder.alloca(self.int_type, name="adj_shift_i")
        self.builder.store(i_val, shift_i)
        self.builder.branch(adj_shift_block)

        self.builder.position_at_end(adj_shift_block)
        shift_i_val = self.builder.load(shift_i)
        next_shift_idx = self.builder.add(shift_i_val, ir.Constant(self.int_type, 1))
        shift_condition = self.builder.icmp_signed('<', next_shift_idx, adj_count)

        do_adj_shift_block = self.builder.block.parent.append_basic_block(name="do_adj_shift")
        finish_adj_shift_block = self.builder.block.parent.append_basic_block(name="finish_adj_shift")

        self.builder.cbranch(shift_condition, do_adj_shift_block, finish_adj_shift_block)

        self.builder.position_at_end(do_adj_shift_block)
        src_adj_ptr = self.builder.gep(adj_list_typed, [next_shift_idx])
        dst_adj_ptr = self.builder.gep(adj_list_typed, [shift_i_val])

        node_to_shift = self.builder.load(src_adj_ptr)
        self.builder.store(node_to_shift, dst_adj_ptr)

        self.builder.store(next_shift_idx, shift_i)
        self.builder.branch(adj_shift_block)

        self.builder.position_at_end(finish_adj_shift_block)
        new_adj_count = self.builder.sub(adj_count, ir.Constant(self.int_type, 1))
        self.builder.store(new_adj_count, adj_count_ptr)
        self.builder.branch(adj_done_block)

        self.builder.position_at_end(adj_next_block)
        next_i = self.builder.add(i_val, ir.Constant(self.int_type, 1))
        self.builder.store(next_i, i)
        self.builder.branch(adj_loop_block)

        self.builder.position_at_end(adj_done_block)

    def _create_hash_remove(self):
        remove_func_type = ir.FunctionType(self.int_type,
            [self.void_ptr.as_pointer(), self.char_ptr, self.int_type])
        self.hash_remove = ir.Function(self.module, remove_func_type, name="hash_remove")

        block = self.hash_remove.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        table_ptr, key, key_len = self.hash_remove.args

        table_head = self.builder.load(table_ptr)
        is_empty = self.builder.icmp_signed('==', table_head, ir.Constant(self.void_ptr, None))

        empty_block = self.hash_remove.append_basic_block(name="empty_table")
        search_block = self.hash_remove.append_basic_block(name="search_table")

        self.builder.cbranch(is_empty, empty_block, search_block)

        self.builder.position_at_end(empty_block)
        self.builder.ret(ir.Constant(self.int_type, -1))

        self.builder.position_at_end(search_block)
        current = self.builder.alloca(self.void_ptr, name="current")
        prev = self.builder.alloca(self.void_ptr.as_pointer(), name="prev")

        self.builder.store(table_head, current)
        self.builder.store(table_ptr, prev)

        loop_block = self.hash_remove.append_basic_block(name="search_loop")
        check_block = self.hash_remove.append_basic_block(name="check_key")
        found_block = self.hash_remove.append_basic_block(name="found_entry")
        not_found_block = self.hash_remove.append_basic_block(name="not_found")
        next_block = self.hash_remove.append_basic_block(name="next_entry")

        self.builder.branch(loop_block)

        self.builder.position_at_end(loop_block)
        current_val = self.builder.load(current)
        is_null = self.builder.icmp_signed('==', current_val, ir.Constant(self.void_ptr, None))
        self.builder.cbranch(is_null, not_found_block, check_block)

        self.builder.position_at_end(check_block)
        entry_ptr = self.builder.bitcast(current_val, self.hash_entry_type.as_pointer())

        entry_key_ptr = self.builder.gep(entry_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 0)])
        entry_key = self.builder.load(entry_key_ptr)
        entry_key_len_ptr = self.builder.gep(entry_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 1)])
        entry_key_len = self.builder.load(entry_key_len_ptr)

        len_match = self.builder.icmp_signed('==', entry_key_len, key_len)
        content_check_block = self.hash_remove.append_basic_block(name="content_check")

        self.builder.cbranch(len_match, content_check_block, next_block)

        self.builder.position_at_end(content_check_block)
        strings_match = self._compare_strings(entry_key, key, key_len)
        self.builder.cbranch(strings_match, found_block, next_block)

        self.builder.position_at_end(found_block)
        next_entry_ptr = self.builder.gep(entry_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 3)])
        next_entry = self.builder.load(next_entry_ptr)

        prev_val = self.builder.load(prev)
        self.builder.store(next_entry, prev_val)

        self.builder.call(self.free_func, [current_val])

        self.builder.ret(ir.Constant(self.int_type, 0))
        self.builder.position_at_end(next_block)
        next_entry_ptr2 = self.builder.gep(entry_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 3)])
        next_entry2 = self.builder.load(next_entry_ptr2)

        entry_next_field_ptr = self.builder.gep(entry_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 3)])
        self.builder.store(entry_next_field_ptr, prev)
        self.builder.store(next_entry2, current)
        self.builder.branch(loop_block)

        self.builder.position_at_end(not_found_block)
        self.builder.ret(ir.Constant(self.int_type, -1))

    def _remove_all_edges_for_vertex(self, graph_ptr, vertex_name, vertex_name_len):

        edge_map_ptr = self.builder.gep(graph_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 4)])

        edges_to_remove = self.builder.alloca(self.void_ptr, name="edges_to_remove_list")
        self.builder.store(ir.Constant(self.void_ptr, None), edges_to_remove)

        edge_map = self.builder.load(edge_map_ptr)
        current_entry = self.builder.alloca(self.void_ptr, name="current_entry")
        self.builder.store(edge_map, current_entry)

        collect_loop_block = self.builder.block.parent.append_basic_block(name="collect_edge_loop")
        check_collect_block = self.builder.block.parent.append_basic_block(name="check_collect_edge")
        add_to_remove_list_block = self.builder.block.parent.append_basic_block(name="add_to_remove_list")
        next_collect_block = self.builder.block.parent.append_basic_block(name="next_collect_edge")
        removal_phase_block = self.builder.block.parent.append_basic_block(name="removal_phase")

        self.builder.branch(collect_loop_block)

        self.builder.position_at_end(collect_loop_block)
        current_entry_val = self.builder.load(current_entry)
        is_null = self.builder.icmp_signed('==', current_entry_val, ir.Constant(self.void_ptr, None))
        self.builder.cbranch(is_null, removal_phase_block, check_collect_block)

        self.builder.position_at_end(check_collect_block)
        entry_ptr = self.builder.bitcast(current_entry_val, self.hash_entry_type.as_pointer())

        edge_key_ptr = self.builder.gep(entry_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 0)])
        edge_key = self.builder.load(edge_key_ptr)
        edge_key_len_ptr = self.builder.gep(entry_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 1)])
        edge_key_len = self.builder.load(edge_key_len_ptr)

        contains_vertex = self._string_contains_substring(edge_key, edge_key_len, vertex_name, vertex_name_len)
        self.builder.cbranch(contains_vertex, add_to_remove_list_block, next_collect_block)

        self.builder.position_at_end(add_to_remove_list_block)

        list_node_size = ir.Constant(self.int64_type, 24)
        list_node_mem = self.builder.call(self.malloc_func, [list_node_size])

        key_ptr_field = self.builder.bitcast(list_node_mem, self.char_ptr.as_pointer())
        self.builder.store(edge_key, key_ptr_field)

        key_len_offset = self.builder.gep(list_node_mem, [ir.Constant(self.int64_type, 8)])
        key_len_field = self.builder.bitcast(key_len_offset, self.int_type.as_pointer())
        self.builder.store(edge_key_len, key_len_field)

        next_offset = self.builder.gep(list_node_mem, [ir.Constant(self.int64_type, 16)])
        next_field = self.builder.bitcast(next_offset, self.void_ptr.as_pointer())
        old_head = self.builder.load(edges_to_remove)
        self.builder.store(old_head, next_field)

        self.builder.store(list_node_mem, edges_to_remove)
        self.builder.branch(next_collect_block)

        self.builder.position_at_end(next_collect_block)
        next_ptr = self.builder.gep(entry_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 3)])
        next_entry = self.builder.load(next_ptr)
        self.builder.store(next_entry, current_entry)
        self.builder.branch(collect_loop_block)

        self.builder.position_at_end(removal_phase_block)

        removal_loop_block = self.builder.block.parent.append_basic_block(name="removal_loop")
        process_removal_block = self.builder.block.parent.append_basic_block(name="process_removal")
        done_edge_cleanup = self.builder.block.parent.append_basic_block(name="done_edge_cleanup")

        self.builder.branch(removal_loop_block)

        self.builder.position_at_end(removal_loop_block)
        current_remove_node = self.builder.load(edges_to_remove)
        is_done = self.builder.icmp_signed('==', current_remove_node, ir.Constant(self.void_ptr, None))
        self.builder.cbranch(is_done, done_edge_cleanup, process_removal_block)

        self.builder.position_at_end(process_removal_block)

        key_from_node_ptr = self.builder.bitcast(current_remove_node, self.char_ptr.as_pointer())
        key_from_node = self.builder.load(key_from_node_ptr)

        key_len_offset = self.builder.gep(current_remove_node, [ir.Constant(self.int64_type, 8)])
        key_len_from_node_ptr = self.builder.bitcast(key_len_offset, self.int_type.as_pointer())
        key_len_from_node = self.builder.load(key_len_from_node_ptr)

        next_offset = self.builder.gep(current_remove_node, [ir.Constant(self.int64_type, 16)])
        next_remove_node_ptr = self.builder.bitcast(next_offset, self.void_ptr.as_pointer())
        next_remove_node = self.builder.load(next_remove_node_ptr)
        self.builder.store(next_remove_node, edges_to_remove)

        edge_to_free = self.builder.call(self.hash_lookup, [edge_map, key_from_node, key_len_from_node])
        edge_exists = self.builder.icmp_signed('!=', edge_to_free, ir.Constant(self.void_ptr, None))

        free_edge_block = self.builder.block.parent.append_basic_block(name="free_edge_obj")
        remove_from_hash_block = self.builder.block.parent.append_basic_block(name="remove_from_hash")

        self.builder.cbranch(edge_exists, free_edge_block, remove_from_hash_block)

        self.builder.position_at_end(free_edge_block)
        self.builder.call(self.free_func, [edge_to_free])
        self.builder.branch(remove_from_hash_block)

        self.builder.position_at_end(remove_from_hash_block)
        self.builder.call(self.hash_remove, [edge_map_ptr, key_from_node, key_len_from_node])

        self.builder.call(self.free_func, [current_remove_node])

        self.builder.branch(removal_loop_block)

        self.builder.position_at_end(done_edge_cleanup)

    def _remove_vertex_from_node_adjacency(self, node_ptr, vertex_name, vertex_name_len):

        adj_list_ptr = self.builder.gep(node_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 3)])
        adj_count_ptr = self.builder.gep(node_ptr, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 4)])

        adj_list = self.builder.load(adj_list_ptr)
        adj_count = self.builder.load(adj_count_ptr)

        adj_exists = self.builder.icmp_signed('!=', adj_list, ir.Constant(self.void_ptr, None))

        process_adj_block = self.builder.block.parent.append_basic_block(name="process_adj_list")
        skip_adj_block = self.builder.block.parent.append_basic_block(name="skip_adj_list")

        self.builder.cbranch(adj_exists, process_adj_block, skip_adj_block)

        self.builder.position_at_end(process_adj_block)
        adj_list_typed = self.builder.bitcast(adj_list, self.node_type.as_pointer().as_pointer())

        write_index = self.builder.alloca(self.int_type, name="write_idx")
        self.builder.store(ir.Constant(self.int_type, 0), write_index)

        i = self.builder.alloca(self.int_type, name="read_idx")
        self.builder.store(ir.Constant(self.int_type, 0), i)

        compact_loop_block = self.builder.block.parent.append_basic_block(name="compact_loop")
        check_vertex_block = self.builder.block.parent.append_basic_block(name="check_vertex")
        keep_vertex_block = self.builder.block.parent.append_basic_block(name="keep_vertex")
        skip_vertex_block = self.builder.block.parent.append_basic_block(name="skip_vertex")
        update_count_block = self.builder.block.parent.append_basic_block(name="update_count")

        self.builder.branch(compact_loop_block)

        self.builder.position_at_end(compact_loop_block)
        i_val = self.builder.load(i)
        loop_condition = self.builder.icmp_signed('<', i_val, adj_count)
        self.builder.cbranch(loop_condition, check_vertex_block, update_count_block)

        self.builder.position_at_end(check_vertex_block)
        read_entry_ptr = self.builder.gep(adj_list_typed, [i_val])
        adj_node = self.builder.load(read_entry_ptr)

        adj_node_name_ptr = self.builder.gep(adj_node, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 1)])
        adj_node_name = self.builder.load(adj_node_name_ptr)
        adj_node_name_len_ptr = self.builder.gep(adj_node, [ir.Constant(self.int_type, 0), ir.Constant(self.int_type, 2)])
        adj_node_name_len = self.builder.load(adj_node_name_len_ptr)

        len_match = self.builder.icmp_signed('==', adj_node_name_len, vertex_name_len)

        content_cmp_block = self.builder.block.parent.append_basic_block(name="content_cmp")
        next_read_block = self.builder.block.parent.append_basic_block(name="next_read")

        self.builder.cbranch(len_match, content_cmp_block, keep_vertex_block)

        self.builder.position_at_end(content_cmp_block)
        names_match = self._compare_strings(adj_node_name, vertex_name, vertex_name_len)
        self.builder.cbranch(names_match, skip_vertex_block, keep_vertex_block)

        self.builder.position_at_end(keep_vertex_block)
        write_idx_val = self.builder.load(write_index)

        indices_different = self.builder.icmp_signed('!=', i_val, write_idx_val)

        do_copy_block = self.builder.block.parent.append_basic_block(name="do_copy")
        advance_write_block = self.builder.block.parent.append_basic_block(name="advance_write")

        self.builder.cbranch(indices_different, do_copy_block, advance_write_block)

        self.builder.position_at_end(do_copy_block)
        write_entry_ptr = self.builder.gep(adj_list_typed, [write_idx_val])
        self.builder.store(adj_node, write_entry_ptr)
        self.builder.branch(advance_write_block)

        self.builder.position_at_end(advance_write_block)
        next_write_idx = self.builder.add(write_idx_val, ir.Constant(self.int_type, 1))
        self.builder.store(next_write_idx, write_index)
        self.builder.branch(next_read_block)

        self.builder.position_at_end(skip_vertex_block)
        self.builder.branch(next_read_block)

        self.builder.position_at_end(next_read_block)
        next_i = self.builder.add(i_val, ir.Constant(self.int_type, 1))
        self.builder.store(next_i, i)
        self.builder.branch(compact_loop_block)

        self.builder.position_at_end(update_count_block)
        final_write_idx = self.builder.load(write_index)
        self.builder.store(final_write_idx, adj_count_ptr)
        self.builder.branch(skip_adj_block)

        self.builder.position_at_end(skip_adj_block)

    def _string_contains_substring(self, haystack, haystack_len, needle, needle_len):

        entry_block = self.builder.block
        false_block = self.builder.block.parent.append_basic_block(name="substr_false")
        search_block = self.builder.block.parent.append_basic_block(name="substr_search")
        outer_loop_block = self.builder.block.parent.append_basic_block(name="outer_search_loop")
        inner_loop_start = self.builder.block.parent.append_basic_block(name="inner_loop_start")
        check_char_block = self.builder.block.parent.append_basic_block(name="check_char")
        char_match_block = self.builder.block.parent.append_basic_block(name="char_match")
        continue_outer_block = self.builder.block.parent.append_basic_block(name="continue_outer")
        true_block = self.builder.block.parent.append_basic_block(name="substr_true")
        merge_block = self.builder.block.parent.append_basic_block(name="merge")

        self.builder.position_at_end(entry_block)
        too_long = self.builder.icmp_signed('>', needle_len, haystack_len)
        self.builder.cbranch(too_long, false_block, search_block)

        self.builder.position_at_end(search_block)
        max_start = self.builder.sub(haystack_len, needle_len)
        max_start = self.builder.add(max_start, ir.Constant(self.int_type, 1))

        i = self.builder.alloca(self.int_type, name="search_i")
        self.builder.store(ir.Constant(self.int_type, 0), i)
        self.builder.branch(outer_loop_block)

        self.builder.position_at_end(outer_loop_block)
        i_val = self.builder.load(i)
        outer_condition = self.builder.icmp_signed('<', i_val, max_start)
        self.builder.cbranch(outer_condition, inner_loop_start, false_block)

        self.builder.position_at_end(inner_loop_start)
        j = self.builder.alloca(self.int_type, name="search_j")
        self.builder.store(ir.Constant(self.int_type, 0), j)
        self.builder.branch(check_char_block)

        self.builder.position_at_end(check_char_block)
        j_val = self.builder.load(j)
        inner_condition = self.builder.icmp_signed('<', j_val, needle_len)

        match_or_mismatch = self.builder.block.parent.append_basic_block(name="match_or_mismatch")
        self.builder.cbranch(inner_condition, match_or_mismatch, true_block)

        self.builder.position_at_end(match_or_mismatch)
        haystack_idx = self.builder.add(i_val, j_val)
        haystack_char_ptr = self.builder.gep(haystack, [haystack_idx])
        needle_char_ptr = self.builder.gep(needle, [j_val])
        haystack_char = self.builder.load(haystack_char_ptr)
        needle_char = self.builder.load(needle_char_ptr)
        chars_match = self.builder.icmp_signed('==', haystack_char, needle_char)

        self.builder.cbranch(chars_match, char_match_block, continue_outer_block)

        self.builder.position_at_end(char_match_block)
        next_j = self.builder.add(j_val, ir.Constant(self.int_type, 1))
        self.builder.store(next_j, j)
        self.builder.branch(check_char_block)

        self.builder.position_at_end(continue_outer_block)
        next_i = self.builder.add(i_val, ir.Constant(self.int_type, 1))
        self.builder.store(next_i, i)
        self.builder.branch(outer_loop_block)

        self.builder.position_at_end(true_block)
        self.builder.branch(merge_block)

        self.builder.position_at_end(false_block)
        self.builder.branch(merge_block)

        self.builder.position_at_end(merge_block)
        phi = self.builder.phi(self.bool_type, name="substr_result")
        phi.add_incoming(ir.Constant(self.bool_type, 1), true_block)
        phi.add_incoming(ir.Constant(self.bool_type, 0), false_block)

        return phi

    def _create_graph_cleanup(self):

        cleanup_type = ir.FunctionType(self.void_type, [self.graph_type.as_pointer()])
        self.graph_cleanup = ir.Function(self.module, cleanup_type, name="graph_cleanup")

        block = self.graph_cleanup.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        graph_ptr = self.graph_cleanup.args[0]

        graph_void = self.builder.bitcast(graph_ptr, self.void_ptr)
        self.builder.call(self.free_func, [graph_void])

        self.builder.ret_void()

    def compile_to_machine_code(self):

        mod = llvm.parse_assembly(str(self.module))
        mod.verify()

        ee = llvm.create_mcjit_compiler(mod, self.target_machine)
        ee.finalize_object()

        functions = {}
        function_names = [
            'graph_init', 'add_vertex', 'add_edge', 'is_adjacent',
            'remove_vertex', 'remove_edge', 'graph_cleanup'
        ]

        for name in function_names:
            func_ptr = ee.get_function_address(name)
            functions[name] = func_ptr

        return functions, ee
