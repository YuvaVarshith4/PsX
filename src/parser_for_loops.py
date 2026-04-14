from lexer_expressions_if import Token
class ASTNode:
    def __init__(self, type_, value=None, line=None):
        self.type = type_
        self.value = value
        self.children = []
        self.line = line
    def __repr__(self):
        return f"{self.type}({self.value}) {self.children}"
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    def advance(self):
        self.pos += 1
    def parse(self):
        nodes = []
        while self.peek():
            stmt = self.statement()
            if stmt:
                nodes.append(stmt)
        return nodes
    def statement(self):
        tok = self.peek()
        if not tok:
            return None
        if tok.type == 'VAR':
            return self.var_declaration()
        elif tok.type == 'PRINT':
            return self.print_statement()
        elif tok.type == 'IF':
            return self.if_statement()
        elif tok.type == 'FOR':
            return self.for_statement()
        elif tok.type == 'IDENT':
            return self.assignment_statement()
        else:
            self.advance()
            return None
  
  
  
    def for_statement(self):
        self.advance()
        self.expect('LPAREN')
      
        type_tok = None
        ident_tok = self.peek()
        if ident_tok.value in ('int', 'float'):
            type_tok = ident_tok.value
            self.advance()
            var_tok = self.peek()
            self.advance()
        else:
            var_tok = self.peek()
            self.advance()
        self.expect('ASSIGN')
        start_tok = self.peek()
        self.advance()
        self.expect('RANGE')
        end_tok = self.peek()
        self.advance()
        self.expect('COMMA')
        step_node = self.parse_expression()
        self.expect('RPAREN')
        self.expect('LBRACE')
        body_nodes = []
        while self.peek() and self.peek().type != 'RBRACE':
            stmt = self.statement()
            if stmt:
                body_nodes.append(stmt)
        self.expect('RBRACE')
        node = ASTNode('For')
        node.children.append(ASTNode('Var', var_tok.value))
        node.children.append(ASTNode('Start', start_tok.value))
        node.children.append(ASTNode('End', end_tok.value))
        node.children.append(step_node)
        node.children.append(ASTNode('Body', body_nodes))
        return node
  
  
  
    def assignment_statement(self):
        var_tok = self.peek()
        self.advance()
        self.expect('ASSIGN')
        value_node = self.parse_expression()
        self.expect('SEMICOLON')
        node = ASTNode('Assign', var_tok.value)
        node.children.append(value_node)
        return node
    def var_declaration(self):
        self.advance()
        name_tok = self.peek()
        self.advance()
        self.expect('ASSIGN')
        value_tok = self.peek()
        self.advance()
        self.expect('SEMICOLON')
        node = ASTNode('VarDecl', name_tok.value)
        node.children.append(ASTNode('Value', value_tok.value))
        return node
    def print_statement(self):
        self.advance()
        self.expect('LPAREN')
        value_tok = self.peek()
        self.advance()
        self.expect('RPAREN')
        self.expect('SEMICOLON')
        node = ASTNode('Print')
        node.children.append(ASTNode('Value', value_tok.value))
        return node
    def if_statement(self):
        self.advance()
        self.expect('LPAREN')
        left_tok = self.peek()
        self.advance()
        op_tok = self.peek()
        self.advance()
        right_tok = self.peek()
        self.advance()
        self.expect('RPAREN')
        self.expect('LBRACE')
        body_nodes = []
        while self.peek() and self.peek().type != 'RBRACE':
            stmt = self.statement()
            if stmt:
                body_nodes.append(stmt)
        self.expect('RBRACE')
        else_nodes = []
        if self.peek() and self.peek().type == 'ELSE':
            self.advance()
            self.expect('LBRACE')
            while self.peek() and self.peek().type != 'RBRACE':
                stmt = self.statement()
                if stmt:
                    else_nodes.append(stmt)
            self.expect('RBRACE')
        node = ASTNode('If')
        node.children.append(ASTNode('Condition', (left_tok.value, op_tok.value, right_tok.value)))
        node.children.append(ASTNode('Body', body_nodes))
        node.children.append(ASTNode('Else', else_nodes))
        return node
  
  
  
    def parse_expression(self):
        node = self.parse_term()
        while self.peek() and self.peek().type in ('PLUS', 'MINUS'):
            op_tok = self.peek()
            self.advance()
            right = self.parse_term()
            op_node = ASTNode('BinOp', op_tok.value)
            op_node.children.append(node)
            op_node.children.append(right)
            node = op_node
        return node
    def parse_term(self):
        node = self.parse_factor()
        while self.peek() and self.peek().type in ('MULT', 'DIV'):
            op_tok = self.peek()
            self.advance()
            right = self.parse_factor()
            op_node = ASTNode('BinOp', op_tok.value)
            op_node.children.append(node)
            op_node.children.append(right)
            node = op_node
        return node
    def parse_factor(self):
        tok = self.peek()
        if tok.type in ('NUMBER', 'STRING', 'IDENT'):
            self.advance()
            return ASTNode('Value', tok.value)
        elif tok.type == 'LPAREN':
            self.advance()
            node = self.parse_expression()
            self.expect('RPAREN')
            return node
        elif tok.type in ('PLUS', 'MINUS'):
            op_tok = self.peek()
            self.advance()
            factor = self.parse_factor()
            if op_tok.value == '+':
                return factor
            else:
              
                zero = ASTNode('Value', '0')
                op_node = ASTNode('BinOp', '-')
                op_node.children.append(zero)
                op_node.children.append(factor)
                return op_node
        else:
            raise SyntaxError(f"Unexpected token {tok}")
    def expect(self, type_):
        tok = self.peek()
        if not tok or tok.type != type_:
            raise SyntaxError(f"Expected {type_}, got {tok}")
        self.advance()