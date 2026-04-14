from code_generator import generate_three_address_code
def generate_meth_short_code(ast):
    """Three address code generation for methods and shortcuts"""
    return generate_three_address_code(ast, "meth_short")
