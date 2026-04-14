class ASTNode:
    def __init__(self, type_, value=None, line=None):
        self.type = type_
        self.value = value
        self.line = line
        self.children = []
class Runtime:
    def __init__(self):
        self.env = {}
    def eval(self, nodes):
        for node in nodes:
            self.execute(node)
    def execute(self, node):
        if node.type == 'VarDecl':
            self.env[node.value] = self.eval_expression(node.children[0])
        elif node.type == 'Print':
            print(self.eval_expression(node.children[0]))
        elif node.type == 'If':
            cond_node = node.children[0]
            left_val = self.eval_expression(cond_node.value[0])
            right_val = self.eval_expression(cond_node.value[2])
            if self.compare(left_val, cond_node.value[1], right_val):
                for stmt in node.children[1].value:
                    self.execute(stmt)
            elif len(node.children) > 2:
                for stmt in node.children[2].value:
                    self.execute(stmt)
  
    def eval_expression(self, node):
        if node.type == 'Value':
            return self.eval_value(node)
        elif node.type == 'BinOp':
            left = self.eval_expression(node.children[0])
            right = self.eval_expression(node.children[1])
            op = node.value
            if op == '+': return left + right
            elif op == '-': return left - right
            elif op == '*': return left * right
            elif op == '/': return left / right
        else:
            raise ValueError(f"Unknown node type {node.type}")
    def eval_value(self, node):
        val = node.value
        if val in self.env:
            return self.env[val]
        try: return int(val)
        except: pass
        try: return float(val)
        except: pass
        if val.startswith('"') and val.endswith('"'):
            return val[1:-1]
        return val
    def compare(self, left, op, right):
        try:
            left = float(left)
            right = float(right)
        except: pass
        if op == '>': return left > right
        elif op == '<': return left < right
        elif op == '==': return left == right
        elif op == '>=': return left >= right
        elif op == '<=': return left <= right
        elif op == '!=': return left != right
        return False