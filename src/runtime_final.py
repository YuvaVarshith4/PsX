class Runtime:
    def __init__(self):
        self.env = {}
    def eval(self, nodes):
        for node in nodes:
            self.execute(node)
  
  
  
    def execute(self, node):
        if node.type == 'VarDecl':
            self.env[node.value] = self.eval_expr(node.children[0])
        
        elif node.type == 'Assign':
            self.env[node.value] = self.eval_expr(node.children[0])
        
        elif node.type == 'Print':
            print(self.eval_expr(node.children[0]))
        
        elif node.type == 'If':
            cond_node = node.children[0]
            left_expr, op, right_expr = cond_node.value
            left_val = self.eval_expr(left_expr)
            right_val = self.eval_expr(right_expr)
            
            if self.compare(left_val, op, right_val):
                for stmt in node.children[1].value:
                    self.execute(stmt)
            elif len(node.children) > 2 and node.children[2].value:
                for stmt in node.children[2].value:
                    self.execute(stmt)
        
        elif node.type == 'While':
            cond_node = node.children[0]
            left_expr, op, right_expr = cond_node.value
            
            while self.compare(self.eval_expr(left_expr), op, self.eval_expr(right_expr)):
                for stmt in node.children[1].value:
                    self.execute(stmt)
        
        elif node.type == 'DoWhile':
            body = node.children[0].value
            cond_node = node.children[1]
            left_expr, op, right_expr = cond_node.value
            
            while True:
                for stmt in body:
                    self.execute(stmt)
                if not self.compare(self.eval_expr(left_expr), op, self.eval_expr(right_expr)):
                    break
        
        elif node.type == 'For':
            var_name = node.children[0].value
            start = int(node.children[1].value)
            end = int(node.children[2].value)
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
  
  
  
    def eval_expr(self, node):
        if isinstance(node, str):
            return self.eval_value(node)
        
        if node.type == 'Value':
            return self.eval_value(node.value)
        
        elif node.type == 'BinOp':
            left = self.eval_expr(node.children[0])
            right = self.eval_expr(node.children[1])
            if node.value == '+':
                return left + right
            elif node.value == '-':
                return left - right
            elif node.value == '*':
                return left * right
            elif node.value == '/':
                return left / right
        
        return self.eval_value(node.value) if hasattr(node, 'value') else node
  
  
  
    def eval_value(self, val):
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
        
        if isinstance(val, str) and val.startswith('"') and val.endswith('"'):
            return val[1:-1]
        
        return val
  
  
  
    def compare(self, left, op, right):
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
