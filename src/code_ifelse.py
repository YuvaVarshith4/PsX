from code_generator import generate_three_address_code
def generate_ifelse_code(ast):
    """Three address code generation for if/else statements"""
    return generate_three_address_code(ast, "ifelse")
