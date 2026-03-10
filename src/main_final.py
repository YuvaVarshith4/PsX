# src/main_ifelse_loops.py - Main entry point for PsX interpreter
import sys
from lexer_final import tokenize
from parser_final import Parser
from runtime_final import Runtime

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main_ifelse_loops.py <file.psx>")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, 'r') as f:
        code = f.read()

    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()

    runtime = Runtime()
    runtime.eval(ast)
