from code_generator import generate_three_address_code
def generate_variables_print_code(ast):
    """Three address code generation for variables and print statements"""
    return generate_three_address_code(ast, "variables_print")
