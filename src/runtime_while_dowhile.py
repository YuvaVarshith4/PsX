# src/runtime5.py

class Runtime:

    def __init__(self):
        self.env = {}

    def eval(self, nodes):

        for node in nodes:
            self.execute(node)

    def execute(self, node):

        if node.type == "VarDecl":

            self.env[node.value] = self.eval_expr(node.children[0])

        elif node.type == "Assign":

            self.env[node.value] = self.eval_expr(node.children[0])

        elif node.type == "Print":

            print(self.eval_expr(node.children[0]))

        elif node.type == "While":

            left, op, right = node.children[0].value

            while self.compare(self.eval_value(left), op, self.eval_value(right)):

                for stmt in node.children[1].value:
                    self.execute(stmt)

        elif node.type == "DoWhile":

            body = node.children[0].value
            left, op, right = node.children[1].value

            while True:

                for stmt in body:
                    self.execute(stmt)

                if not self.compare(self.eval_value(left), op, self.eval_value(right)):
                    break

    # ------------------

    def eval_expr(self, node):
        if isinstance(node, str):
            return self.eval_value(node)
        if node.type == "Value":
            return self.eval_value(node.value)
        elif node.type == "BinOp":
            left = self.eval_expr(node.children[0])
            right = self.eval_expr(node.children[1])
            if node.value == "+":
                return left + right
            elif node.value == "-":
                return left - right
            elif node.value == "*":
                return left * right
            elif node.value == "/":
                return left / right
        return self.eval_value(node.value) if hasattr(node, 'value') else node

    def eval_value(self, val):

        if val in self.env:
            return self.env[val]

        try:
            return int(val)
        except:
            pass

        if val.startswith('"') and val.endswith('"'):
            return val[1:-1]

        return val

    # ------------------

    def compare(self, a, op, b):

        if op == ">":
            return a > b
        if op == "<":
            return a < b
        if op == "==":
            return a == b
        if op == ">=":
            return a >= b
        if op == "<=":
            return a <= b
        if op == "!=":
            return a != b

        return False