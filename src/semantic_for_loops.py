from semantic_analyzer import analyze_semantics
def analyze_for_loops(ast):
    """Semantic analysis for for loops"""
    return analyze_semantics(ast, "for_loops")
