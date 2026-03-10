# src/main_mix.py
import sys
from lexer_mix import tokenize
from parser_mix import Parser
from runtime_mix import Runtime

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main_mix.py <file.psx>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, 'r') as f:
            code = f.read()

        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()

        runtime = Runtime()
        runtime.eval(ast)
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"Runtime Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)