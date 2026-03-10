# src/main_for_loops.py - PsX interpreter with for loops
from lexer_expressions_if import tokenize
from parser_for_loops import Parser
from runtime_for_loops import Runtime

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