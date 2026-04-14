from semantic_analyzer import analyze_semantics
def analyze_variables_print(ast):
    """Semantic analysis for variables and print statements"""
    return analyze_semantics(ast, "variables_print")
