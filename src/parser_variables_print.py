# src/parser_variables_print.py
from lexer_variables_print import Token

class ASTNode:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
        self.children = []
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
            node = self.statement()
            if node:
                nodes.append(node)
        return nodes

    def statement(self):
        tok = self.peek()
        if tok.type == 'VAR':
            return self.var_declaration()
        elif tok.type == 'PRINT':
            return self.print_statement()
        elif tok.type == 'IF':
            return self.if_statement()
        else:
            self.advance()
            return None

    def var_declaration(self):
        self.advance()  # skip 'var'
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
        self.advance()  # skip 'print'
        self.expect('LPAREN')
        value_tok = self.peek()
        self.advance()
        self.expect('RPAREN')
        self.expect('SEMICOLON')
        node = ASTNode('Print')
        node.children.append(ASTNode('Value', value_tok.value))
        return node

    def if_statement(self):
        self.advance()  # skip 'if'
        self.expect('LPAREN')
        cond_left = self.peek()
        self.advance()
        op = self.peek()
        self.advance()
        cond_right = self.peek()
        self.advance()
        self.expect('RPAREN')
        self.expect('LBRACE')
        body = []
        while self.peek() and self.peek().type != 'RBRACE':
            stmt = self.statement()
            if stmt:
             body.append(stmt)
        self.expect('RBRACE')
        node = ASTNode('If')
        node.children.append(ASTNode('Condition', (cond_left.value, op.value, cond_right.value)))
        node.children.append(ASTNode('Body', body))
        return node

    def expect(self, type_):
        tok = self.peek()
        if not tok or tok.type != type_:
            raise SyntaxError(f"Expected {type_}, got {tok}")
        self.advance()