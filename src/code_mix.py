from code_generator import generate_three_address_code
def generate_mix_code(ast):
    """Three address code generation for mix/hybrid features"""
    return generate_three_address_code(ast, "mix")
