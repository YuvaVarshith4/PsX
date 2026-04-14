import re

TOKEN_SPEC = [
    ('NUMBER',   r'\d+(\.\d+)?'),
    ('STRING',   r'"[^"]*"'),
    ('VAR',      r'\bvar\b'),
    ('FOR',      r'\bfor\b'),
    ('IF',       r'\bif\b'),
    ('ELSE',     r'\belse\b'),
    ('PRINT',    r'\bprint\b'),
    ('WHILE', r'\bwhile\b'),
    ('DO', r'\bdo\b'),
    ('IDENT',    r'[A-Za-z_][A-Za-z0-9_]*'),
    ('GE',       r'>='),
    ('LE',       r'<='),
    ('EQ',       r'=='),
    ('NE',       r'!='),
    ('ASSIGN',   r'='),
    ('SEMICOLON',r';'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('LBRACE',   r'\{'),
    ('RBRACE',   r'\}'),
    ('RANGE',    r'\.\.'),
    ('COMMA',    r','),   
    ('GT',       r'>'),
    ('LT',       r'<'),
    ('PLUS',     r'\+'),
    ('MINUS',    r'-'),
    ('MULT',     r'\*'),
    ('DIV',      r'/'),
    ('SKIP',     r'[ \t]+'),
    ('NEWLINE',  r'\n'),
]

token_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPEC)

class Token:
    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value
        self.line = line
    def __repr__(self):
        return f"{self.type}({self.value})"

def tokenize(code):
    tokens = []
    line_num = 1
    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NEWLINE':
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        tokens.append(Token(kind, value, line_num))
    return tokens