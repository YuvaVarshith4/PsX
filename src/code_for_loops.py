from code_generator import generate_three_address_code
def generate_for_loops_code(ast):
    """Three address code generation for for loops"""
    return generate_three_address_code(ast, "for_loops")
