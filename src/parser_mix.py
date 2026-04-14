
from lexer_mix import Token
class ASTNode:
    def __init__(self, type_, value=None, line=None):
        self.type = type_
        self.value = value
        self.children = []
        self.line = line
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    def peek_next(self):
        return self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
    def advance(self):
        self.pos += 1
    def expect(self, type_):
        tok = self.peek()
        if not tok or tok.type != type_:
            raise SyntaxError(f"Expected {type_}, got {tok}")
        self.advance()
    def create_node(self, type_, value=None):
        """Helper to create ASTNode with current line number"""
        current_token = self.tokens[self.pos - 1] if self.pos > 0 else None
        line = current_token.line if current_token else None
        return ASTNode(type_, value, line)
    def parse(self):
        nodes = []
        while self.peek():
            stmt = self.statement()
            if stmt:
                nodes.append(stmt)
        return nodes
    def statement(self):
        tok = self.peek()
        if not tok: return None
        if tok.type == 'VAR': return self.var_declaration()
        elif tok.type == 'FUNCTION': return self.function_declaration()
        elif tok.type == 'RETURN': return self.return_statement()
        elif tok.type == 'PRINT': return self.print_statement()
        elif tok.type == 'IF': return self.if_statement()
        elif tok.type == 'WHILE': return self.while_statement()
        elif tok.type == 'DO': return self.do_while_statement()
        elif tok.type == 'FOR': return self.for_statement()
        elif tok.type == 'IDENT': return self.assignment_or_function_call()
        else:
            self.advance()
            return None
    def function_declaration(self):
        self.advance()
        name_tok = self.peek()
        self.advance()
        self.expect('LPAREN')
        params = []
        if self.peek() and self.peek().type != 'RPAREN':
            params.append(self.peek().value)
            self.advance()
            while self.peek() and self.peek().type == 'COMMA':
                self.advance()
                params.append(self.peek().value)
                self.advance()
        self.expect('RPAREN')
        self.expect('LBRACE')
        body = []
        while self.peek() and self.peek().type != 'RBRACE':
            stmt = self.statement()
            if stmt: body.append(stmt)
        self.expect('RBRACE')
        node = self.create_node('FunctionDecl', name_tok.value)
        node.children.append(self.create_node('Params', params))
        node.children.append(self.create_node('Body', body))
        return node
    def var_declaration(self):
        self.advance() 
        name_tok = self.peek()
        self.advance()
        self.expect('ASSIGN')
        value_expr = self.parse_expression()
        self.expect('SEMICOLON')
        node = self.create_node('VarDecl', name_tok.value)
        node.children.append(value_expr)
        return node
    def assignment_or_function_call(self):
        name_tok = self.peek()
        self.advance()
        ident_name = name_tok.value
        while self.peek() and self.peek().type == 'DOT':
            self.advance()
            prop_tok = self.peek()
            self.expect('IDENT')
            ident_name += '.' + prop_tok.value
            
        if self.peek() and self.peek().type == 'ASSIGN':
            self.advance()
            expr = self.parse_expression()
            self.expect('SEMICOLON')
            node = self.create_node('Assign', ident_name)
            node.children.append(expr)
            return node
        elif self.peek() and self.peek().type in ('PLUS_ASSIGN', 'MINUS_ASSIGN', 'MULT_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN'):
            op_tok = self.peek()
            self.advance()
            expr = self.parse_expression()
            self.expect('SEMICOLON')
            node = self.create_node('AssignOp', (ident_name, op_tok.value))
            node.children.append(expr)
            return node
        elif self.peek() and self.peek().type in ('INC', 'DEC'):
            op_tok = self.peek()
            self.advance()
            self.expect('SEMICOLON')
            return self.create_node('Update', (ident_name, op_tok.value))
        elif self.peek() and self.peek().type == 'LBRACKET':
            self.advance()
            index_expr = self.parse_expression()
            self.expect('RBRACKET')
            self.expect('ASSIGN')
            expr = self.parse_expression()
            self.expect('SEMICOLON')
            node = self.create_node('ArrayAssign', ident_name)
            node.children.append(index_expr)
            node.children.append(expr)
            return node
        elif self.peek() and self.peek().type == 'LPAREN':
            return self.function_call(ident_name)
        else:
            raise SyntaxError(f"Expected assignment or call after identifier, got {self.peek()}")
    def function_call(self, func_name):
        self.expect('LPAREN')
        args = []
        if self.peek() and self.peek().type != 'RPAREN':
            args.append(self.parse_expression())
            while self.peek() and self.peek().type == 'COMMA':
                self.advance()
                args.append(self.parse_expression())
        self.expect('RPAREN')
        self.expect('SEMICOLON')
        node = self.create_node('Call', func_name)
        for arg in args:
            node.children.append(arg)
        return node
    def print_statement(self):
        self.advance() 
        self.expect('LPAREN')
        expr_node = self.parse_expression()
        self.expect('RPAREN')
        self.expect('SEMICOLON')
        node = self.create_node('Print')
        node.children.append(expr_node)
        return node
    def return_statement(self):
        self.advance()
        expr = None
        if self.peek() and self.peek().type != 'SEMICOLON':
            expr = self.parse_expression()
        self.expect('SEMICOLON')
        node = self.create_node('Return')
        if expr: node.children.append(expr)
        return node
    def if_statement(self):
        self.advance()
        self.expect('LPAREN')
        cond_expr = self.parse_expression()
        self.expect('RPAREN')
        self.expect('LBRACE')
        if_body = []
        while self.peek() and self.peek().type != 'RBRACE':
            stmt = self.statement()
            if stmt: if_body.append(stmt)
        self.expect('RBRACE')
        else_body = []
        if self.peek() and self.peek().type == 'ELSE':
            self.advance()
            self.expect('LBRACE')
            while self.peek() and self.peek().type != 'RBRACE':
                stmt = self.statement()
                if stmt: else_body.append(stmt)
            self.expect('RBRACE')
        node = self.create_node('If')
        node.children.append(cond_expr)
        node.children.append(self.create_node('Body', if_body))
        node.children.append(self.create_node('Else', else_body))
        return node
    def while_statement(self):
        self.advance()
        self.expect('LPAREN')
        cond_expr = self.parse_expression()
        self.expect('RPAREN')
        self.expect('LBRACE')
        body = []
        while self.peek() and self.peek().type != 'RBRACE':
            stmt = self.statement()
            if stmt: body.append(stmt)
        self.expect('RBRACE')
        node = self.create_node('While')
        node.children.append(cond_expr)
        node.children.append(self.create_node('Body', body))
        return node
    def do_while_statement(self):
        self.advance()
        self.expect('LBRACE')
        body = []
        while self.peek() and self.peek().type != 'RBRACE':
            stmt = self.statement()
            if stmt: body.append(stmt)
        self.expect('RBRACE')
        self.expect('WHILE')
        self.expect('LPAREN')
        cond_expr = self.parse_expression()
        self.expect('RPAREN')
        self.expect('SEMICOLON')
        node = self.create_node('DoWhile')
        node.children.append(self.create_node('Body', body))
        node.children.append(cond_expr)
        return node
    def for_statement(self):
        self.advance()
        self.expect('LPAREN')
        ident_tok = self.peek()
        if ident_tok.value in ('int', 'float'):
            self.advance()
            var_tok = self.peek()
            self.advance()
        else:
            var_tok = self.peek()
            self.advance()
        self.expect('ASSIGN')
        start_expr = self.parse_expression() 
        self.expect('RANGE')
        end_expr = self.parse_expression()   
        self.expect('COMMA')
        step_expr = self.parse_expression()  
        self.expect('RPAREN')
        self.expect('LBRACE')
        body_nodes = []
        while self.peek() and self.peek().type != 'RBRACE':
            stmt = self.statement()
            if stmt: body_nodes.append(stmt)
        self.expect('RBRACE')
        node = self.create_node('For')
        node.children.append(self.create_node('Var', var_tok.value))
        node.children.append(start_expr)
        node.children.append(end_expr)
        node.children.append(step_expr)
        node.children.append(self.create_node('Body', body_nodes))
        return node
    def parse_expression(self):
        if self.peek() and self.peek().type == 'IDENT':
            next_tok = self.peek_next()
            if next_tok and next_tok.type == 'ARROW':
                ident_tok = self.peek()
                self.advance()
                self.advance()
                if self.peek() and self.peek().type == 'LBRACE':
                    self.expect('LBRACE')
                    body = []
                    while self.peek() and self.peek().type != 'RBRACE':
                        stmt = self.statement()
                        if stmt: body.append(stmt)
                    self.expect('RBRACE')
                    node = self.create_node('ArrowFunc')
                    node.children.append(self.create_node('Params', [ident_tok.value]))
                    node.children.append(self.create_node('Body', body))
                    return node
                else:
                    body_expr = self.parse_expression()
                    node = self.create_node('ArrowFunc')
                    node.children.append(self.create_node('Params', [ident_tok.value]))
                    node.children.append(body_expr)
                    return node
        return self.parse_comparison()
    def parse_comparison(self):
        node = self.parse_arithmetic()
        if self.peek() and self.peek().type in ('EQ', 'NE', 'GT', 'LT', 'GE', 'LE'):
            op_tok = self.peek()
            self.advance()
            right = self.parse_arithmetic()
            op_node = self.create_node('BinOp', op_tok.value)
            op_node.children.append(node)
            op_node.children.append(right)
            node = op_node
        return node
    def parse_arithmetic(self):
        node = self.parse_term()
        while self.peek() and self.peek().type in ('PLUS', 'MINUS'):
            op_tok = self.peek()
            self.advance()
            right = self.parse_term()
            op_node = self.create_node('BinOp', op_tok.value)
            op_node.children.append(node)
            op_node.children.append(right)
            node = op_node
        return node
    def parse_term(self):
        node = self.parse_power()
        while self.peek() and self.peek().type in ('MULT', 'DIV', 'MOD'):
            op_tok = self.peek()
            self.advance()
            right = self.parse_power()
            op_node = self.create_node('BinOp', op_tok.value)
            op_node.children.append(node)
            op_node.children.append(right)
            node = op_node
        return node
    def parse_power(self):
        node = self.parse_factor()
        while self.peek() and self.peek().type == 'POWER':
            op_tok = self.peek()
            self.advance()
            right = self.parse_factor()
            op_node = self.create_node('BinOp', op_tok.value)
            op_node.children.append(node)
            op_node.children.append(right)
            node = op_node
        return node
    def parse_factor(self):
        tok = self.peek()
        if tok.type in ('NUMBER', 'STRING'):
            self.advance()
            return self.create_node('Value', tok.value)
        elif tok.type == 'LBRACKET': 
            self.advance()
            elements = []
            if self.peek() and self.peek().type != 'RBRACKET':
                elements.append(self.parse_expression())
                while self.peek() and self.peek().type == 'COMMA':
                    self.advance()
                    elements.append(self.parse_expression())
            self.expect('RBRACKET')
            node = self.create_node('ArrayLiteral')
            for el in elements:
                node.children.append(el)
            return node
        elif tok.type == 'IDENT':
            self.advance()
            ident_name = tok.value
            while self.peek() and self.peek().type == 'DOT':
                self.advance()
                prop_tok = self.peek()
                self.expect('IDENT')
                ident_name += '.' + prop_tok.value
                
            if self.peek() and self.peek().type == 'LBRACKET': 
                self.advance()
                index_expr = self.parse_expression()
                self.expect('RBRACKET')
                node = self.create_node('ArrayIndex', ident_name)
                node.children.append(index_expr)
                return node
            elif self.peek() and self.peek().type == 'LPAREN': 
                self.advance()
                args = []
                if self.peek() and self.peek().type != 'RPAREN':
                    args.append(self.parse_expression())
                    while self.peek() and self.peek().type == 'COMMA':
                        self.advance()
                        args.append(self.parse_expression())
                self.expect('RPAREN')
                node = self.create_node('Call', ident_name)
                for arg in args:
                    node.children.append(arg)
                return node
            return self.create_node('Value', ident_name)
        elif tok.type == 'LPAREN':
            self.advance()
            if self.is_arrow_function():
                return self.parse_arrow_function_from_paren()
            else:
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
                zero = self.create_node('Value', '0')
                op_node = self.create_node('BinOp', '-')
                op_node.children.append(zero)
                op_node.children.append(factor)
                return op_node
        else:
            raise SyntaxError(f"Unexpected token {tok}")
    def is_arrow_function(self):
        i = self.pos
        while i < len(self.tokens) and self.tokens[i].type != 'RPAREN': i += 1
        if i < len(self.tokens) and self.tokens[i].type == 'RPAREN': i += 1
        return i < len(self.tokens) and self.tokens[i].type == 'ARROW'
    def parse_arrow_function_from_paren(self):
        params = []
        if self.peek() and self.peek().type != 'RPAREN':
            params.append(self.peek().value)
            self.advance()
            while self.peek() and self.peek().type == 'COMMA':
                self.advance()
                params.append(self.peek().value)
                self.advance()
        self.expect('RPAREN')
        self.expect('ARROW')
        if self.peek() and self.peek().type == 'LBRACE':
            self.expect('LBRACE')
            body = []
            while self.peek() and self.peek().type != 'RBRACE':
                stmt = self.statement()
                if stmt: body.append(stmt)
            self.expect('RBRACE')
            node = self.create_node('ArrowFunc')
            node.children.append(self.create_node('Params', params))
            node.children.append(self.create_node('Body', body))
        else:
            expr = self.parse_expression()
            node = self.create_node('ArrowFunc')
            node.children.append(self.create_node('Params', params))
            node.children.append(expr)
        return node