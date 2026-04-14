from semantic_analyzer import analyze_semantics
def analyze_expressions_if(ast):
    """Semantic analysis for expressions and if/else statements"""
    return analyze_semantics(ast, "expressions_if")
