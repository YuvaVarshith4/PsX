# src/main_variables_print.py - PsX interpreter with variables and print
import sys
from lexer_variables_print import tokenize
from parser_variables_print import Parser
from runtime_variables_print import Runtime

if len(sys.argv) < 2:
    print("Usage: python main_variables_print.py <file.psx>")
    sys.exit(1)

file_path = sys.argv[1]
with open(file_path, "r") as f:
    code = f.read()

tokens = tokenize(code)
parser = Parser(tokens)
ast = parser.parse()

runtime = Runtime()
runtime.eval(ast)