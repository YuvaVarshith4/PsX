
import sys
from lexer_expressions_if import tokenize
from parser_expressions_if import Parser
from runtime_expressions_if import Runtime
from semantic_expressions_if import analyze_expressions_if
from code_expressions_if import generate_expressions_if_code

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main_expressions_if.py <file.psx>")
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
        
      
        semantic_result = analyze_expressions_if(ast)
        if semantic_result['errors']:
            print("Semantic Errors:")
            for error in semantic_result['errors']:
                print(f"  {error}")
        if semantic_result['warnings']:
            print("Semantic Warnings:")
            for warning in semantic_result['warnings']:
                print(f"  {warning}")
        
      
        code_result = generate_expressions_if_code(ast)
        
      
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