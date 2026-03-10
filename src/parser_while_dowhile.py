# src/parser_while_dowhile.py - Parser for while and do-while loops
from lexer_expressions_if import Token

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

    def expect(self, type_):
        tok = self.peek()
        if not tok or tok.type != type_:
            raise SyntaxError(f"Expected {type_}, got {tok}")
        self.advance()

    def parse(self):
        nodes = []
        while self.peek():
            stmt = self.statement()
            if stmt:
                nodes.append(stmt)
        return nodes

    def statement(self):

        tok = self.peek()

        if tok.type == "VAR":
            return self.var_decl()

        if tok.type == "PRINT":
            return self.print_stmt()

        if tok.type == "WHILE":
            return self.while_stmt()

        if tok.type == "DO":
            return self.do_while_stmt()

        if tok.type == "IDENT":
            return self.assign_stmt()

        self.advance()
        return None

    # -----------------------
    # ASSIGNMENT
    # -----------------------

    def assign_stmt(self):

        name = self.peek()
        self.advance()

        self.expect("ASSIGN")

        expr = self.parse_expr()

        self.expect("SEMICOLON")

        node = ASTNode("Assign", name.value)
        node.children.append(expr)

        return node

    # -----------------------
    # VAR
    # -----------------------

    def var_decl(self):

        self.advance()

        name = self.peek()
        self.advance()

        self.expect("ASSIGN")

        expr = self.parse_expr()

        self.expect("SEMICOLON")

        node = ASTNode("VarDecl", name.value)
        node.children.append(expr)

        return node

    # -----------------------
    # PRINT
    # -----------------------

    def print_stmt(self):

        self.advance()
        self.expect("LPAREN")

        expr = self.parse_expr()

        self.expect("RPAREN")
        self.expect("SEMICOLON")

        node = ASTNode("Print")
        node.children.append(expr)

        return node

    # -----------------------
    # WHILE
    # -----------------------

    def while_stmt(self):

        self.advance()

        self.expect("LPAREN")

        left = self.peek()
        self.advance()

        op = self.peek()
        self.advance()

        right = self.peek()
        self.advance()

        self.expect("RPAREN")

        self.expect("LBRACE")

        body = []

        while self.peek() and self.peek().type != "RBRACE":
            stmt = self.statement()
            if stmt:
                body.append(stmt)

        self.expect("RBRACE")

        node = ASTNode("While")
        node.children.append(ASTNode("Condition", (left.value, op.value, right.value)))
        node.children.append(ASTNode("Body", body))

        return node

    # -----------------------
    # DO WHILE
    # -----------------------

    def do_while_stmt(self):

        self.advance()

        self.expect("LBRACE")

        body = []

        while self.peek() and self.peek().type != "RBRACE":
            stmt = self.statement()
            if stmt:
                body.append(stmt)

        self.expect("RBRACE")

        self.expect("WHILE")
        self.expect("LPAREN")

        left = self.peek()
        self.advance()

        op = self.peek()
        self.advance()

        right = self.peek()
        self.advance()

        self.expect("RPAREN")
        self.expect("SEMICOLON")

        node = ASTNode("DoWhile")
        node.children.append(ASTNode("Body", body))
        node.children.append(ASTNode("Condition", (left.value, op.value, right.value)))

        return node

    # -----------------------
    # EXPRESSION PARSING
    # -----------------------

    def parse_expr(self):
        return self.parse_term()

    def parse_term(self):
        node = self.parse_factor()
        while self.peek() and self.peek().type in ("PLUS", "MINUS"):
            op = self.peek()
            self.advance()
            right = self.parse_factor()
            bin_op = ASTNode("BinOp", op.value)
            bin_op.children.append(node)
            bin_op.children.append(right)
            node = bin_op
        return node

    def parse_factor(self):
        tok = self.peek()
        if tok.type in ("NUMBER", "IDENT", "STRING"):
            self.advance()
            return ASTNode("Value", tok.value)
        elif tok.type == "LPAREN":
            self.advance()
            expr = self.parse_expr()
            self.expect("RPAREN")
            return expr
        else:
            raise SyntaxError(f"Unexpected token {tok}")