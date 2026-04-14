from lexer_expressions_if import tokenize
from parser_while_dowhile import Parser
from runtime_while_dowhile import Runtime
import sys

filename = sys.argv[1]

with open(filename) as f:
    code = f.read()

tokens = tokenize(code)

parser = Parser(tokens)

ast = parser.parse()

runtime = Runtime()

runtime.eval(ast)