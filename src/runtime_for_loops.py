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
            self.env[node.value] = self.eval_value(node.children[0])
        elif node.type == 'Assign':
            self.env[node.value] = self.eval_expression(node.children[0])
        elif node.type == 'Print':
            print(self.eval_expression(node.children[0]))
        elif node.type == 'If':
            cond_node = node.children[0]
            left, op, right = cond_node.value
            left_val = self.eval_value(ASTNode('Value', left))
            right_val = self.eval_value(ASTNode('Value', right))
            if self.compare(left_val, op, right_val):
                for stmt in node.children[1].value:
                    self.execute(stmt)
            else:
                for stmt in node.children[2].value:
                    self.execute(stmt)
        elif node.type == 'For':
            var_name = node.children[0].value
            start = int(node.children[1].value)
            end = int(node.children[2].value)
            step = self.eval_expression(node.children[3])
          
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
        try:
            return int(val)
        except:
            pass
        try:
            return float(val)
        except:
            pass
        if val.startswith('"') and val.endswith('"'):
            return val[1:-1]
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