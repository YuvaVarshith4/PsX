import sys

def get_interpreter_components(file_type):
    """Dynamically import appropriate components based on file type"""
    
    components = {
        'variables_print': {
            'lexer': 'lexer_variables_print',
            'parser': 'parser_variables_print', 
            'runtime': 'runtime_variables_print',
            'semantic': 'semantic_variables_print',
            'codegen': 'code_variables_print'
        },
        'expressions_if': {
            'lexer': 'lexer_expressions_if',
            'parser': 'parser_expressions_if',
            'runtime': 'runtime_expressions_if', 
            'semantic': 'semantic_expressions_if',
            'codegen': 'code_expressions_if'
        },
        'ifelse': {
            'lexer': 'lexer_expressions_if',
            'parser': 'parser_ifelse',
            'runtime': 'runtime_ifelse',
            'semantic': 'semantic_ifelse', 
            'codegen': 'code_ifelse'
        },
        'for_loops': {
            'lexer': 'lexer_expressions_if',
            'parser': 'parser_for_loops',
            'runtime': 'runtime_for_loops',
            'semantic': 'semantic_for_loops',
            'codegen': 'code_for_loops'
        },
        'while_dowhile': {
            'lexer': 'lexer_expressions_if',
            'parser': 'parser_while_dowhile', 
            'runtime': 'runtime_while_dowhile',
            'semantic': 'semantic_while_dowhile',
            'codegen': 'code_while_dowhile'
        },
        'func': {
            'lexer': 'lexer_func',
            'parser': 'parser_func',
            'runtime': 'runtime_func',
            'semantic': 'semantic_func',
            'codegen': 'code_func'
        },
        'meth_short': {
            'lexer': 'lexer_meth_short',
            'parser': 'parser_meth_short',
            'runtime': 'runtime_meth_short', 
            'semantic': 'semantic_meth_short',
            'codegen': 'code_meth_short'
        },
        'mix': {
            'lexer': 'lexer_mix',
            'parser': 'parser_mix',
            'runtime': 'runtime_mix',
            'semantic': 'semantic_mix',
            'codegen': 'code_mix'
        }
    }
    
    return components.get(file_type, components['mix'])

def detect_file_type(filename):
    """Auto-detect file type based on filename or content"""
    filename_lower = filename.lower()
    
    if 'variables_print' in filename_lower or 'hello.psx' in filename_lower:
        return 'variables_print'
    elif 'expressions_if' in filename_lower or 'hello2.psx' in filename_lower:
        return 'expressions_if'
    elif 'ifelse' in filename_lower or 'hello2.psx' in filename_lower:
        return 'ifelse'
    elif 'for_loops' in filename_lower or 'hello3.psx' in filename_lower:
        return 'for_loops'
    elif 'while_dowhile' in filename_lower or 'hello4.psx' in filename_lower:
        return 'while_dowhile'
    elif 'func' in filename_lower or 'hello6.psx' in filename_lower:
        return 'func'
    elif 'meth' in filename_lower or 'comprehensive.psx' in filename_lower:
        return 'meth_short'
    elif 'mix' in filename_lower or 'ultimate' in filename_lower:
        return 'mix'
    else:
        return 'mix'

def run_psx_complete(filename, file_type=None):
    """Complete PsX execution with all phases"""
    
  
    if file_type is None:
        file_type = detect_file_type(filename)
    
  
    comps = get_interpreter_components(file_type)
    
  
    lexer_module = __import__(comps['lexer'])
    parser_module = __import__(comps['parser'])
    runtime_module = __import__(comps['runtime'])
    semantic_module = __import__(comps['semantic'])
    codegen_module = __import__(comps['codegen'])
    
    print(f"🔧 PsX Complete Interpreter ({file_type})")
    print("=" * 50)
    
    try:
        with open(filename, 'r') as f:
            code = f.read()
        
      
        print("\n📝 Phase 1: Lexical Analysis")
        tokens = lexer_module.tokenize(code)
        print(f"  Generated {len(tokens)} tokens")
        
      
        print("\n🌲 Phase 2: Parsing")
        parser = parser_module.Parser(tokens)
        ast = parser.parse()
        print(f"  Created {len(ast)} AST nodes")
        
      
        print("\n✅ Phase 3: Semantic Analysis")
        semantic_analyzer = getattr(semantic_module, f'analyze_{file_type}')
        semantic_result = semantic_analyzer(ast)
        
        if semantic_result['errors']:
            print("  ❌ Semantic Errors:")
            for error in semantic_result['errors']:
                print(f"    {error}")
        else:
            print("  ✅ No semantic errors found")
            
        if semantic_result['warnings']:
            print("  ⚠️  Semantic Warnings:")
            for warning in semantic_result['warnings']:
                print(f"    {warning}")
        
      
        print("\n🏗️ Phase 4: Three-Address Code Generation")
        codegen_func = getattr(codegen_module, f'generate_{file_type}_code')
        code_result = codegen_func(ast)
        print(f"  Generated {len(code_result['instructions'])} instructions")
        print(f"  Allocated {len(code_result['memory_map'])} memory locations")
        
      
        print("\n🚀 Phase 5: Runtime Execution")
        runtime = runtime_module.Runtime()
        runtime.eval(ast)
        
      
        print("\n📋 Phase 6: Generated Code Output")
        from code_generator import CodeGenerator
        generator = CodeGenerator()
        generator.output_code(code_result)
        
        print("\n" + "=" * 50)
        print("✅ COMPLETE PSX EXECUTION FINISHED")
        print("=" * 50)
        
        return {
            'tokens': len(tokens),
            'ast_nodes': len(ast),
            'semantic_errors': len(semantic_result['errors']),
            'semantic_warnings': len(semantic_result['warnings']),
            'generated_instructions': len(code_result['instructions']),
            'memory_allocations': len(code_result['memory_map'])
        }
        
    except FileNotFoundError:
        print(f"❌ Error: File '{filename}' not found")
        sys.exit(1)
    except SyntaxError as e:
        print(f"❌ Syntax Error: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"❌ Runtime Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("🔧 PsX Complete Interpreter")
        print("Usage: python main_integrated.py <file.psx> [file_type]")
        print("\nFile types:")
        print("  variables_print, expressions_if, ifelse, for_loops")
        print("  while_dowhile, func, meth_short, mix")
        print("\nExamples:")
        print("  python main_integrated.py examples/hello.psx variables_print")
        print("  python main_integrated.py examples/ultimate_mix.psx mix")
        sys.exit(1)
    
    filename = sys.argv[1]
    file_type = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = run_psx_complete(filename, file_type)
    
  
    print(f"\n📊 EXECUTION SUMMARY:")
    print(f"  Tokens: {result['tokens']}")
    print(f"  AST Nodes: {result['ast_nodes']}")
    print(f"  Semantic Errors: {result['semantic_errors']}")
    print(f"  Semantic Warnings: {result['semantic_warnings']}")
    print(f"  Generated Instructions: {result['generated_instructions']}")
    print(f"  Memory Allocations: {result['memory_allocations']}")
