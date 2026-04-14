from semantic_analyzer import analyze_semantics
def analyze_func(ast):
    """Semantic analysis for functions"""
    return analyze_semantics(ast, "func")
