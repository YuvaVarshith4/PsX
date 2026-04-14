import copy
class Symbol:
    def __init__(self, name, type_, scope, line=None):
        self.name = name
        self.type = type_
        self.scope = scope
        self.line = line
        self.is_used = False
class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.current_scope = "global"
        self.errors = []
        self.warnings = []
        self.function_stack = []
        self.loop_stack = []
        
      
        self.builtin_functions = {
            'print', 'len', 'typeOf', 'int', 'float', 'str',
            'math.abs', 'math.min', 'math.max', 'math.round', 'math.rand',
            'str.trim', 'str.upper', 'str.lower', 'str.split', 'str.replace',
            'arr.push', 'arr.pop', 'arr.join', 'arr.length'
        }
        
    def analyze(self, nodes):
        """Main entry point for semantic analysis"""
        for node in nodes:
            self.analyze_node(node)
        
      
        self.check_unused_variables()
        
        return {
            'errors': self.errors,
            'warnings': self.warnings,
            'symbol_table': self.symbol_table
        }
    
    def analyze_node(self, node):
        """Analyze individual AST node"""
        if node.type == 'VarDecl':
            self.analyze_var_declaration(node)
        elif node.type == 'Assign':
            self.analyze_assignment(node)
        elif node.type == 'FunctionDecl':
            self.analyze_function_declaration(node)
        elif node.type == 'Call':
            self.analyze_function_call(node)
        elif node.type == 'Return':
            self.analyze_return_statement(node)
        elif node.type == 'If':
            self.analyze_if_statement(node)
        elif node.type == 'While':
            self.analyze_while_statement(node)
        elif node.type == 'For':
            self.analyze_for_statement(node)
        elif node.type == 'Print':
            self.analyze_print_statement(node)
        
      
        for child in node.children:
            if hasattr(child, 'type'):
                self.analyze_node(child)
    
    def analyze_var_declaration(self, node):
        """Analyze variable declaration"""
        var_name = node.value
        var_type = self.infer_type(node.children[0])
        
      
        if var_name in self.symbol_table:
            existing = self.symbol_table[var_name]
            if existing.scope == self.current_scope:
                self.errors.append(f"Line {node.line}: Variable '{var_name}' already declared in current scope")
                return
        
      
        symbol = Symbol(var_name, var_type, self.current_scope, node.line)
        self.symbol_table[var_name] = symbol
    
    def analyze_assignment(self, node):
        """Analyze assignment statement"""
        var_name = node.value
        
      
        if var_name not in self.symbol_table:
            self.errors.append(f"Line {node.line}: Undefined variable '{var_name}'")
            return
        
      
        self.symbol_table[var_name].is_used = True
        
      
        expr_type = self.infer_type(node.children[0])
        var_type = self.symbol_table[var_name].type
        
        if not self.is_compatible_types(expr_type, var_type):
            self.warnings.append(f"Line {node.line}: Type mismatch - assigning {expr_type} to {var_type}")
    
    def analyze_function_declaration(self, node):
        """Analyze function declaration"""
        func_name = node.value
        
      
        if func_name in self.symbol_table:
            existing = self.symbol_table[func_name]
            if existing.scope == self.current_scope:
                self.errors.append(f"Line {node.line}: Function '{func_name}' already declared")
                return
        
      
        symbol = Symbol(func_name, 'function', self.current_scope, node.line)
        self.symbol_table[func_name] = symbol
        
      
        old_scope = self.current_scope
        self.current_scope = f"{func_name}_scope"
        self.function_stack.append(func_name)
        
      
        params = node.children[0].value if node.children[0] else []
        for param in params:
            param_symbol = Symbol(param, 'parameter', self.current_scope)
            self.symbol_table[param] = param_symbol
        
      
        if len(node.children) > 1:
            body = node.children[1].value if hasattr(node.children[1], 'value') else [node.children[1]]
            for stmt in body:
                self.analyze_node(stmt)
        
      
        self.current_scope = old_scope
        self.function_stack.pop()
    
    def analyze_function_call(self, node):
        """Analyze function call"""
        func_name = node.value
        
      
        if func_name in self.builtin_functions:
            return
        
      
        if func_name not in self.symbol_table:
            self.errors.append(f"Line {node.line}: Undefined function '{func_name}'")
            return
        
        symbol = self.symbol_table[func_name]
        if symbol.type != 'function':
            self.errors.append(f"Line {node.line}: '{func_name}' is not a function")
        
      
        symbol.is_used = True
        
      
        for arg in node.children:
            self.analyze_node(arg)
    
    def analyze_return_statement(self, node):
        """Analyze return statement"""
        if not self.function_stack:
            self.errors.append(f"Line {node.line}: Return statement outside function")
            return
        
      
        if node.children:
            self.analyze_node(node.children[0])
    
    def analyze_if_statement(self, node):
        """Analyze if statement"""
      
        if node.children:
            self.analyze_node(node.children[0])
        
      
        if len(node.children) > 1:
            if_body = node.children[1].value if hasattr(node.children[1], 'value') else [node.children[1]]
            for stmt in if_body:
                self.analyze_node(stmt)
        
      
        if len(node.children) > 2:
            else_body = node.children[2].value if hasattr(node.children[2], 'value') else [node.children[2]]
            for stmt in else_body:
                self.analyze_node(stmt)
    
    def analyze_while_statement(self, node):
        """Analyze while statement"""
      
        self.loop_stack.append('while')
        
      
        if node.children:
            self.analyze_node(node.children[0])
        if len(node.children) > 1:
            body = node.children[1].value if hasattr(node.children[1], 'value') else [node.children[1]]
            for stmt in body:
                self.analyze_node(stmt)
        
      
        self.loop_stack.pop()
    
    def analyze_for_statement(self, node):
        """Analyze for statement"""
      
        self.loop_stack.append('for')
        
      
        var_name = node.children[0].value
        loop_var = Symbol(var_name, 'integer', self.current_scope)
        self.symbol_table[var_name] = loop_var
        
      
        for child in node.children[1:]:
            self.analyze_node(child)
        
      
        self.loop_stack.pop()
    
    def analyze_print_statement(self, node):
        """Analyze print statement"""
        if node.children:
            self.analyze_node(node.children[0])
    
    def infer_type(self, node):
        """Infer type of expression node"""
        if node.type == 'Value':
            value = node.value
            if value.isdigit() or (value.replace('-', '').isdigit() and value.count('-') == 1):
                return 'integer'
            elif '.' in value and value.replace('.', '').replace('-', '').isdigit():
                return 'float'
            elif value.startswith('"') and value.endswith('"'):
                return 'string'
            elif value in self.symbol_table:
                return self.symbol_table[value].type
            return 'unknown'
        
        elif node.type == 'BinOp':
            left_type = self.infer_type(node.children[0])
            right_type = self.infer_type(node.children[1])
            
            if node.value in ['+', '-', '*', '/', '%']:
                if 'string' in [left_type, right_type]:
                    return 'string'
                return 'number'
            elif node.value in ['==', '!=', '>', '<', '>=', '<=']:
                return 'boolean'
        
        elif node.type == 'Call':
            return 'unknown'
        
        return 'unknown'
    
    def is_compatible_types(self, from_type, to_type):
        """Check if types are compatible for assignment"""
        if from_type == to_type:
            return True
        
      
        if from_type in ['integer', 'float'] and to_type in ['integer', 'float']:
            return True
        
      
        if from_type == 'string' and to_type == 'string':
            return True
        
        return False
    
    def check_unused_variables(self):
        """Check for unused variables and functions"""
        for name, symbol in self.symbol_table.items():
            if not symbol.is_used and symbol.scope != "global":
                self.warnings.append(f"Line {symbol.line}: Unused variable/function '{name}'")
# Integration function for all main files
def analyze_semantics(ast, file_type="mix"):
    """Universal semantic analysis interface"""
    analyzer = SemanticAnalyzer()
    
  
    if file_type == "variables_print":
        return analyzer.analyze(ast)
    elif file_type == "expressions_if":
        return analyzer.analyze(ast)
    elif file_type == "ifelse":
        return analyzer.analyze(ast)
    elif file_type == "for_loops":
        return analyzer.analyze(ast)
    elif file_type == "while_dowhile":
        return analyzer.analyze(ast)
    elif file_type == "func":
        return analyzer.analyze(ast)
    elif file_type == "meth_short":
        return analyzer.analyze(ast)
    elif file_type == "mix":
        return analyzer.analyze(ast)
    else:
        return analyzer.analyze(ast)
