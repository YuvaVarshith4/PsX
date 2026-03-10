# src/runtime.py
class Runtime:
    def __init__(self):
        self.env = {}

    def eval(self, nodes):
        for node in nodes:
            self.execute(node)

    def execute(self, node):
        if node.type == 'VarDecl':
            name = node.value
            value = self.eval_value(node.children[0])
            self.env[name] = value
        elif node.type == 'Print':
            value = self.eval_value(node.children[0])
            print(value)
        elif node.type == 'If':
            cond_node = node.children[0]
            left, op, right = cond_node.value
            left_val = self.eval_value(ASTNode('Value', left))
            right_val = self.eval_value(ASTNode('Value', right))
            if self.compare(left_val, op, right_val):
                for stmt in node.children[1].value:
                    self.execute(stmt)

    def eval_value(self, node):
        val = node.value
        # Check if val is variable
        if val in self.env:
            return self.env[val]
        # Check if val is integer literal
        try:
            return int(val)
        except ValueError:
            pass
        # Check if val is float
        try:
            return float(val)
        except ValueError:
            pass
        # String literal
        if val.startswith('"') and val.endswith('"'):
            return val[1:-1]
        return val  # fallback

    def compare(self, left, op, right):
        # Ensure left and right are numbers if possible
        try:
            left = float(left)
            right = float(right)
        except:
            pass
        if op == '>':
            return left > right
        elif op == '<':
            return left < right
        elif op == '==':
            return left == right
        elif op == '>=':
            return left >= right
        elif op == '<=':
            return left <= right
        elif op == '!=':
            return left != right
        return False

# Helper ASTNode class for eval_value
class ASTNode:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
        self.children = []