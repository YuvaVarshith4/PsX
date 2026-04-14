from code_generator import generate_three_address_code
def generate_while_dowhile_code(ast):
    """Three address code generation for while and do-while loops"""
    return generate_three_address_code(ast, "while_dowhile")
