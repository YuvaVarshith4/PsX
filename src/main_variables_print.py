
import sys
from lexer_variables_print import tokenize
from parser_variables_print import Parser
from runtime_variables_print import Runtime
from semantic_variables_print import analyze_variables_print
from code_variables_print import generate_variables_print_code

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main_variables_print.py <file.psx>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, 'r') as f:
            code = f.read()

      
        tokens = tokenize(code)
        print(f"Lexical Analysis: {len(tokens)} tokens generated")
        
      
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"Parsing: {len(ast)} AST nodes created")
        
      
        semantic_result = analyze_variables_print(ast)
        if semantic_result['errors']:
            print("Semantic Errors:")
            for error in semantic_result['errors']:
                print(f"  {error}")
        if semantic_result['warnings']:
            print("Semantic Warnings:")
            for warning in semantic_result['warnings']:
                print(f"  {warning}")
        
      
        code_result = generate_variables_print_code(ast)
        
      
        print("\n=== EXECUTION ===")
        runtime = Runtime()
        runtime.eval(ast)
        
      
        print("\n=== GENERATED CODE ===")
        from code_generator import CodeGenerator
        generator = CodeGenerator()
        generator.output_code(code_result)
        
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