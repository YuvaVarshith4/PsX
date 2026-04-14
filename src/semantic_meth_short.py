from semantic_analyzer import analyze_semantics
def analyze_meth_short(ast):
    """Semantic analysis for methods and shortcuts"""
    return analyze_semantics(ast, "meth_short")
