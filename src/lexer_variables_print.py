import re

TOKEN_SPEC = [
    ('NUMBER',   r'\d+(\.\d+)?'),
    ('STRING',   r'"[^"]*"'),
    ('VAR',      r'\bvar\b'),
    ('IF',       r'\bif\b'),
    ('ELSE',     r'\belse\b'),
    ('PRINT',    r'\bprint\b'),
    ('IDENT',    r'[A-Za-z_][A-Za-z0-9_]*'),
    ('ASSIGN',   r'='),
    ('SEMICOLON',r';'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('LBRACE',   r'\{'),
    ('RBRACE',   r'\}'),
    ('GE',       r'>='),
    ('LE',       r'<='),
    ('EQ',       r'=='),
    ('NE',       r'!='),
    ('GT',       r'>'),
    ('LT',       r'<'),
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

if __name__ == "__main__":
    code = 'var x = 10; print("Hello PsX");'
    tokens = tokenize(code)
    for t in tokens:
        print(t)