import copy
import random
import math
class Function:
    def __init__(self, name, params, body, is_arrow=False, closure_env=None, is_expr=False):
        self.name = name
        self.params = params
        self.body = body
        self.is_arrow = is_arrow
        self.closure_env = closure_env or {}
        self.is_expr = is_expr
class NativeFunction:
    def __init__(self, name, func):
        self.name = name
        self.func = func
class ReturnException(Exception):
    pass
class ASTNode:
    def __init__(self, type_, value=None, line=None):
        self.type = type_
        self.value = value
        self.line = line
        self.children = []
class Runtime:
    def __init__(self):
      
        self.env = {
          
            'len': NativeFunction('len', lambda args: len(args[0])),
            'typeOf': NativeFunction('typeOf', lambda args: type(args[0]).__name__),
            'int': NativeFunction('int', lambda args: int(args[0])),
            'float': NativeFunction('float', lambda args: float(args[0])),
            'str': NativeFunction('str', lambda args: str(args[0])),
            
          
            'str.toUpper': NativeFunction('str.toUpper', lambda args: str(args[0]).upper() if args else ""),
            'str.toLower': NativeFunction('str.toLower', lambda args: str(args[0]).lower() if args else ""),
            'str.split': NativeFunction('str.split', lambda args: str(args[0]).split(args[1]) if len(args) > 1 else str(args[0]).split()),
            'str.replace': NativeFunction('str.replace', lambda args: str(args[0]).replace(str(args[1]), str(args[2])) if len(args) > 2 else args[0]),
            'str.trim': NativeFunction('str.trim', lambda args: str(args[0]).strip() if args else ""),
            
          
            'math.rand': NativeFunction('math.rand', self._math_rand),
            'math.round': NativeFunction('math.round', lambda args: round(float(args[0])) if args else 0),
            'math.floor': NativeFunction('math.floor', lambda args: math.floor(float(args[0])) if args else 0),
            'math.ceil': NativeFunction('math.ceil', lambda args: math.ceil(float(args[0])) if args else 0),
            'math.abs': NativeFunction('math.abs', lambda args: abs(float(args[0])) if args else 0),
            'math.max': NativeFunction('math.max', lambda args: max(args) if args else 0),
            'math.min': NativeFunction('math.min', lambda args: min(args) if args else 0),
            
          
            'arr.push': NativeFunction('arr.push', self._arr_push),
            'arr.pop': NativeFunction('arr.pop', self._arr_pop),
            'arr.join': NativeFunction('arr.join', lambda args: str(args[1]).join(map(str, args[0])) if len(args) > 1 else "".join(map(str, args[0]))),
        }
        self.call_stack = []
        self.return_value = None
    def _math_rand(self, args):
        if len(args) == 2:
            return random.randint(int(args[0]), int(args[1]))
        return random.random()
    def _arr_push(self, args):
        if len(args) == 2 and isinstance(args[0], list):
            args[0].append(args[1])
            return args[0]
        return None
    def _arr_pop(self, args):
        if len(args) == 1 and isinstance(args[0], list) and len(args[0]) > 0:
            return args[0].pop()
        return None
    def eval(self, nodes):
        for node in nodes:
            self.execute(node)
    def execute(self, node):
        if node.type == 'VarDecl':
            value = self.eval_expr(node.children[0])
            self.env[node.value] = value
        
        elif node.type == 'Assign':
            value = self.eval_expr(node.children[0])
            self.env[node.value] = value
            
        elif node.type == 'AssignOp':
            var_name, op = node.value
            val = self.eval_expr(node.children[0])
            if var_name in self.env:
                if op == '+=':
                    left = self.env[var_name]
                    if isinstance(left, str) or isinstance(val, str):
                        self.env[var_name] = str(left) + str(val)
                    else:
                        self.env[var_name] += val
                elif op == '-=': self.env[var_name] -= val
                elif op == '*=': self.env[var_name] *= val
                elif op == '/=': self.env[var_name] /= val
                elif op == '%=': self.env[var_name] %= val
                    
        elif node.type == 'Update':
            var_name, op = node.value
            if var_name in self.env:
                if op == '++':
                    self.env[var_name] += 1
                elif op == '--':
                    self.env[var_name] -= 1
            
        elif node.type == 'ArrayAssign':
            arr_name = node.value
            idx = int(self.eval_expr(node.children[0]))
            val = self.eval_expr(node.children[1])
            if arr_name in self.env:
                arr = self.env[arr_name]
                if isinstance(arr, list):
                    if idx >= len(arr):
                        arr.extend([None] * (idx - len(arr) + 1))
                    arr[idx] = val
        
        elif node.type == 'FunctionDecl':
            func = Function(node.value, node.children[0].value, node.children[1].value)
            func.closure_env = copy.deepcopy(self.env)
            self.env[node.value] = func
        
        elif node.type == 'Call':
            return self.call_function(node.value, node.children)
        
        elif node.type == 'Return':
            if node.children:
                self.return_value = self.eval_expr(node.children[0])
            else:
                self.return_value = None
            raise ReturnException()
        
        elif node.type == 'Print':
            print(self.eval_expr(node.children[0]))
        
        elif node.type == 'If':
            if self.eval_expr(node.children[0]):
                for stmt in node.children[1].value:
                    self.execute(stmt)
            elif len(node.children) > 2 and node.children[2].value:
                for stmt in node.children[2].value:
                    self.execute(stmt)
        
        elif node.type == 'While':
            while self.eval_expr(node.children[0]):
                for stmt in node.children[1].value:
                    self.execute(stmt)
        
        elif node.type == 'DoWhile':
            body = node.children[0].value
            while True:
                for stmt in body:
                    self.execute(stmt)
                if not self.eval_expr(node.children[1]):
                    break
        
        elif node.type == 'For':
            var_name = node.children[0].value
            start = int(self.eval_expr(node.children[1]))
            end = int(self.eval_expr(node.children[2]))
            step = int(self.eval_expr(node.children[3]))
            
            if step > 0:
                end_range = end + 1
            elif step < 0:
                end_range = end - 1
            else:
                end_range = end
            
            for i in range(start, end_range, step):
                self.env[var_name] = i
                for stmt in node.children[4].value:
                    self.execute(stmt)
    def call_function(self, func_name, args):
        func = self.eval_expr(ASTNode('Value', func_name))
        evaluated_args = [self.eval_expr(arg) for arg in args]
        
        if isinstance(func, NativeFunction):
            return func.func(evaluated_args)
            
        if not isinstance(func, Function):
            raise RuntimeError(f"'{func_name}' is not a function")
        
        old_env = self.env
        self.env = copy.deepcopy(func.closure_env)
        
        for i, param in enumerate(func.params):
            if i < len(evaluated_args):
                self.env[param] = evaluated_args[i]
            else:
                self.env[param] = None
        
        try:
            self.return_value = None
            if func.is_arrow and getattr(func, 'is_expr', False):
                result = self.eval_expr(func.body[0])
                self.env = old_env
                return result
            else:
                for stmt in func.body:
                    self.execute(stmt)
                result = self.return_value
                self.env = old_env
                return result
        except ReturnException:
            result = self.return_value
            self.env = old_env
            return result
    def eval_expr(self, node):
        if isinstance(node, str):
            return self.eval_value(node)
        
        if node.type == 'Value':
            return self.eval_value(node.value)
            
        elif node.type == 'ArrayLiteral':
            return [self.eval_expr(child) for child in node.children]
            
        elif node.type == 'ArrayIndex':
            arr = self.env.get(node.value)
            idx = int(self.eval_expr(node.children[0]))
            return arr[idx]
            
        elif node.type == 'Call':
            return self.call_function(node.value, node.children)
        
        elif node.type == 'BinOp':
            left = self.eval_expr(node.children[0])
            right = self.eval_expr(node.children[1])
            op = node.value
            
            if op == '+':
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right
            elif op == '-': return left - right
            elif op == '*': return left * right
            elif op == '/': return left / right
            elif op == '%': return left % right
            elif op == '**': return left ** right
            elif op in ('==', '!=', '>', '<', '>=', '<='):
                return self.compare(left, op, right)
        
        elif node.type == 'ArrowFunc':
            params = node.children[0].value
            is_expr = node.children[1].type != 'Body'
            if is_expr:
                body = [node.children[1]]
            else:
                body = node.children[1].value
                
            return Function(None, params, body, is_arrow=True, closure_env=copy.deepcopy(self.env), is_expr=is_expr)
        
        return self.eval_value(node.value) if hasattr(node, 'value') else node
    def eval_value(self, val):
        if isinstance(val, str) and val in self.env:
            return self.env[val]
        
        try:
            return int(val)
        except:
            pass
        
        try:
            return float(val)
        except:
            pass
        
        if isinstance(val, str) and val.startswith('"') and val.endswith('"'):
            return val[1:-1].replace('\\n', '\n')
        
        return val
    def compare(self, left, op, right):
        try:
            left = float(left)
            right = float(right)
        except:
            pass
        
        if op == '>': return left > right
        elif op == '<': return left < right
        elif op == '==': return left == right
        elif op == '>=': return left >= right
        elif op == '<=': return left <= right
        elif op == '!=': return left != right
        
        return False