# src/main_expressions_if.py - PsX interpreter with expressions and if statements
from lexer_expressions_if import tokenize
from parser_expressions_if import Parser
from runtime_expressions_if import Runtime

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