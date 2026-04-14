from semantic_analyzer import analyze_semantics
def analyze_while_dowhile(ast):
    """Semantic analysis for while and do-while loops"""
    return analyze_semantics(ast, "while_dowhile")
