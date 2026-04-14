from code_generator import generate_three_address_code
def generate_expressions_if_code(ast):
    """Three address code generation for expressions and if/else statements"""
    return generate_three_address_code(ast, "expressions_if")
