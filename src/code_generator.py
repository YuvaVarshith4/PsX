import sys
class MemoryManager:
    def __init__(self, size=65536):
        self.memory = [None] * size
        self.heap_ptr = size // 2
        self.stack_ptr = size - 1
        self.symbol_to_address = {}
        self.next_address = 1000
    
    def allocate_address(self, var_name, size=1):
        """Allocate memory address for variable"""
        address = self.next_address
        self.next_address += size
        self.symbol_to_address[var_name] = address
        return address
    
    def get_address(self, var_name):
        """Get address of variable"""
        return self.symbol_to_address.get(var_name, -1)
    
    def store(self, address, value):
        """Store value at address"""
        if 0 <= address < len(self.memory):
            self.memory[address] = value
    
    def load(self, address):
        """Load value from address"""
        if 0 <= address < len(self.memory):
            return self.memory[address]
        return None
    
    def push_stack(self, value):
        """Push value onto stack"""
        self.memory[self.stack_ptr] = value
        self.stack_ptr -= 1
    
    def pop_stack(self):
        """Pop value from stack"""
        self.stack_ptr += 1
        return self.memory[self.stack_ptr]
class RegisterManager:
    def __init__(self):
        self.registers = {
            'R0': 0, 'R1': 0, 'R2': 0, 'R3': 0,
            'R4': 0, 'R5': 0, 'R6': 0, 'R7': 0,
            'SP': 65535,
            'FP': 65535,
            'PC': 0      
        }
    
    def set_register(self, reg, value):
        """Set register value"""
        if reg in self.registers:
            self.registers[reg] = value
    
    def get_register(self, reg):
        """Get register value"""
        return self.registers.get(reg, 0)
    
    def copy_register(self, src, dest):
        """Copy value between registers"""
        if src in self.registers and dest in self.registers:
            self.registers[dest] = self.registers[src]
class CodeGenerator:
    def __init__(self):
        self.memory = MemoryManager()
        self.registers = RegisterManager()
        self.instructions = []
        self.label_counter = 0
        self.current_function = None
    
    def generate(self, ast):
        """Main entry point for code generation"""
        self.instructions = []
        
      
        self.add_instruction("HEADER", "PsX Three Address Code Generation")
        self.add_instruction("ALLOC", f"Memory size: {self.memory.memory}")
        
      
        for node in ast:
            self.generate_node(node)
        
      
        self.add_instruction("FOOTER", "End of generated code")
        
        return {
            'instructions': self.instructions,
            'memory_map': self.memory.symbol_to_address,
            'register_state': self.registers.registers
        }
    
    def generate_node(self, node):
        """Generate code for individual AST node"""
        if node.type == 'VarDecl':
            return self.generate_var_declaration(node)
        elif node.type == 'Assign':
            return self.generate_assignment(node)
        elif node.type == 'FunctionDecl':
            return self.generate_function_declaration(node)
        elif node.type == 'Call':
            return self.generate_function_call(node)
        elif node.type == 'Return':
            return self.generate_return_statement(node)
        elif node.type == 'If':
            return self.generate_if_statement(node)
        elif node.type == 'While':
            return self.generate_while_statement(node)
        elif node.type == 'For':
            return self.generate_for_statement(node)
        elif node.type == 'Print':
            return self.generate_print_statement(node)
        elif node.type == 'BinOp':
            return self.generate_binary_operation(node)
        elif node.type == 'Value':
            return self.generate_value(node)
        elif node.type == 'Start' or node.type == 'End':
            return self.generate_value(node)
        else:
            return None
    
    def generate_var_declaration(self, node):
        """Generate code for variable declaration"""
        var_name = node.value
        address = self.memory.allocate_address(var_name)
        
      
        expr_result = self.generate_node(node.children[0])
        self.memory.store(address, expr_result)
        
        self.add_instruction("VARDECL", f"ALLOC {var_name} -> [{address}] = {expr_result}")
        
        return expr_result
    
    def generate_assignment(self, node):
        """Generate code for assignment"""
        var_name = node.value
        address = self.memory.get_address(var_name)
        
        if address == -1:
          
            address = self.memory.allocate_address(var_name)
        
        expr_result = self.generate_node(node.children[0])
        self.memory.store(address, expr_result)
        
        self.add_instruction("ASSIGN", f"[{address}] = {expr_result} ({var_name})")
        
        return expr_result
    
    def generate_function_declaration(self, node):
        """Generate code for function declaration"""
        func_name = node.value
        self.current_function = func_name
        
      
        self.add_instruction("FUNC_START", f"--- Function: {func_name} ---")
        self.registers.set_register('FP', self.registers.get_register('SP'))
        
      
        if node.children:
            params = node.children[0].value if hasattr(node.children[0], 'value') else []
            for param in params:
                param_addr = self.memory.allocate_address(f"{func_name}_{param}")
                self.add_instruction("PARAM", f"PARAM {param} -> [{param_addr}]")
        
      
        if len(node.children) > 1:
            body = node.children[1].value if hasattr(node.children[1], 'value') else [node.children[1]]
            for stmt in body:
                self.generate_node(stmt)
        
      
        self.add_instruction("FUNC_END", f"--- End Function: {func_name} ---")
        self.current_function = None
    
    def generate_function_call(self, node):
        """Generate code for function call"""
        func_name = node.value
        
      
        args = []
        for arg in node.children:
            arg_result = self.generate_node(arg)
            args.append(arg_result)
        
      
        for i, arg in enumerate(args):
            self.memory.push_stack(arg)
            self.add_instruction("PUSH_ARG", f"Push arg{i}: {arg} -> [SP]")
        
      
        self.add_instruction("CALL", f"CALL {func_name} with {len(args)} arguments")
        
      
        for i in range(len(args)):
            self.memory.pop_stack()
            self.add_instruction("POP_ARG", f"Pop arg{i} from stack")
    
    def generate_return_statement(self, node):
        """Generate code for return statement"""
        if node.children:
            result = self.generate_node(node.children[0])
            self.registers.set_register('R0', result)
            self.add_instruction("RETURN", f"RETURN {result} -> R0")
        else:
            self.add_instruction("RETURN", "RETURN (void)")
    
    def generate_if_statement(self, node):
        """Generate code for if statement"""
        label_else = f"else_{self.label_counter}"
        label_end = f"end_if_{self.label_counter}"
        self.label_counter += 1
        
      
        if node.children:
            condition_result = self.generate_node(node.children[0])
            self.add_instruction("IF", f"IF {condition_result} == false GOTO {label_else}")
        
      
        if len(node.children) > 1:
            if_body = node.children[1].value if hasattr(node.children[1], 'value') else [node.children[1]]
            for stmt in if_body:
                self.generate_node(stmt)
        
        self.add_instruction("GOTO", f"GOTO {label_end}")
        self.add_instruction("LABEL", f"{label_else}:")
        
      
        if len(node.children) > 2:
            else_body = node.children[2].value if hasattr(node.children[2], 'value') else [node.children[2]]
            for stmt in else_body:
                self.generate_node(stmt)
        
        self.add_instruction("LABEL", f"{label_end}:")
    
    def generate_while_statement(self, node):
        """Generate code for while statement"""
        label_start = f"while_start_{self.label_counter}"
        label_end = f"while_end_{self.label_counter}"
        self.label_counter += 1
        
        self.add_instruction("LABEL", f"{label_start}:")
        
      
        if node.children:
            condition_result = self.generate_node(node.children[0])
            self.add_instruction("WHILE", f"IF {condition_result} == false GOTO {label_end}")
        
      
        if len(node.children) > 1:
            body = node.children[1].value if hasattr(node.children[1], 'value') else [node.children[1]]
            for stmt in body:
                self.generate_node(stmt)
        
        self.add_instruction("GOTO", f"GOTO {label_start}")
        self.add_instruction("LABEL", f"{label_end}:")
    
    def generate_for_statement(self, node):
        """Generate code for for statement"""
        label_start = f"for_start_{self.label_counter}"
        label_end = f"for_end_{self.label_counter}"
        self.label_counter += 1
        
      
        var_name = node.children[0].value
        var_addr = self.memory.allocate_address(var_name)
        
      
        start_result = self.generate_node(node.children[1])
        self.memory.store(var_addr, start_result)
        
        self.add_instruction("LABEL", f"{label_start}:")
        
      
        end_result = self.generate_node(node.children[2])
        self.add_instruction("FOR_CHECK", f"IF [{var_addr}] >= {end_result} GOTO {label_end}")
        
      
        if len(node.children) > 4:
            body_node = node.children[4]
            if hasattr(body_node, 'value') and isinstance(body_node.value, list):
                for stmt in body_node.value:
                    self.generate_node(stmt)
            else:
                self.generate_node(body_node)
        
      
        step_result = self.generate_node(node.children[3]) if len(node.children) > 3 else 1
        current_val = self.memory.load(var_addr)
        new_val = current_val + step_result
        self.memory.store(var_addr, new_val)
        
        self.add_instruction("FOR_STEP", f"[{var_addr}] = [{var_addr}] + {step_result}")
        self.add_instruction("GOTO", f"GOTO {label_start}")
        self.add_instruction("LABEL", f"{label_end}:")
    
    def generate_print_statement(self, node):
        """Generate code for print statement"""
        if node.children:
            result = self.generate_node(node.children[0])
            self.add_instruction("PRINT", f"PRINT {result}")
            return result
        return None
    
    def generate_binary_operation(self, node):
        """Generate code for binary operations"""
        left_result = self.generate_node(node.children[0])
        right_result = self.generate_node(node.children[1])
        op = node.value
        
      
        self.registers.set_register('R1', left_result)
        self.registers.set_register('R2', right_result)
        
        if op == '+':
            result = left_result + right_result
            self.registers.set_register('R3', result)
            self.add_instruction("ADD", f"R3 = R1 + R2 = {result}")
        elif op == '-':
            result = left_result - right_result
            self.registers.set_register('R3', result)
            self.add_instruction("SUB", f"R3 = R1 - R2 = {result}")
        elif op == '*':
            result = left_result * right_result
            self.registers.set_register('R3', result)
            self.add_instruction("MUL", f"R3 = R1 * R2 = {result}")
        elif op == '/':
            result = left_result / right_result
            self.registers.set_register('R3', result)
            self.add_instruction("DIV", f"R3 = R1 / R2 = {result}")
        elif op == '%':
            result = left_result % right_result
            self.registers.set_register('R3', result)
            self.add_instruction("MOD", f"R3 = R1 % R2 = {result}")
        else:
            result = 0
            self.add_instruction("UNKNOWN_OP", f"Unknown operation: {op}")
        
        return result
    
    def generate_value(self, node):
        """Generate code for value node"""
        value = node.value
        
      
        if isinstance(value, str) and not value.startswith('"'):
            address = self.memory.get_address(value)
            if address != -1:
                loaded_value = self.memory.load(address)
                self.registers.set_register('R1', loaded_value)
                self.add_instruction("LOAD", f"R1 = [{address}] = {loaded_value} ({value})")
                return loaded_value
            else:
              
                try:
                    if '.' in value:
                        return float(value)
                    else:
                        return int(value)
                except:
                    return value
        
        return value
    
    def add_instruction(self, instr_type, description):
        """Add instruction to output"""
        instruction = {
            'type': instr_type,
            'description': description,
            'registers': self.registers.registers.copy(),
            'memory': self.memory.memory[:100]
        }
        self.instructions.append(instruction)
    
    def output_code(self, result):
        """Output generated three-address code"""
        print("=" * 60)
        print("🔧 PSX THREE-ADDRESS CODE GENERATION")
        print("=" * 60)
        
        print(f"\nGenerated {len(result['instructions'])} instructions")
        print(f"Memory allocations: {len(result['memory_map'])} variables")
        
        print("\n📋 INSTRUCTIONS:")
        for i, instr in enumerate(result['instructions']):
            print(f"{i+1:3d}. {instr['type']:12s} - {instr['description']}")
        
        print("\n📍 MEMORY MAP:")
        for var, addr in result['memory_map'].items():
            print(f"    {var:15s} -> [{addr:4d}]")
        
        print("\n🏪 FINAL REGISTER STATE:")
        for reg, value in result['register_state'].items():
            print(f"    {reg:3s}: {value:6d}")
        
        print("\n" + "=" * 60)
        print("✅ CODE GENERATION COMPLETE")
        print("=" * 60)
# Integration function for all main files
def generate_three_address_code(ast, file_type="mix"):
    """Universal three-address code generation interface"""
    generator = CodeGenerator()
    
  
    if file_type == "variables_print":
        return generator.generate(ast)
    elif file_type == "expressions_if":
        return generator.generate(ast)
    elif file_type == "ifelse":
        return generator.generate(ast)
    elif file_type == "for_loops":
        return generator.generate(ast)
    elif file_type == "while_dowhile":
        return generator.generate(ast)
    elif file_type == "func":
        return generator.generate(ast)
    elif file_type == "meth_short":
        return generator.generate(ast)
    elif file_type == "mix":
        return generator.generate(ast)
    else:
        return generator.generate(ast)
