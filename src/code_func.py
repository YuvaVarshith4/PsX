from code_generator import generate_three_address_code
def generate_func_code(ast):
    """Three address code generation for functions"""
    return generate_three_address_code(ast, "func")
