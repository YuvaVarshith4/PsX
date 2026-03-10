# src/main_ifelse.py - PsX interpreter with if-else statements
from lexer_expressions_if import tokenize
from parser_ifelse import Parser
from runtime_ifelse import Runtime

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        code = f.read()

    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()

    runtime = Runtime()
    runtime.eval(ast)