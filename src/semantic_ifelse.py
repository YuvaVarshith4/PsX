from semantic_analyzer import analyze_semantics
def analyze_ifelse(ast):
    """Semantic analysis for if/else statements"""
    return analyze_semantics(ast, "ifelse")
