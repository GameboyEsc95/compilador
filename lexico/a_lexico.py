from lark import Lark, Token, UnexpectedInput

# Gramática léxica simple
gramatica = r"""
    start: (ASIGNACION | PALABRA | NUMERO | OPERADOR | WS)*
    ASIGNACION: "="
    PALABRA: /[a-zA-Z_][a-zA-Z0-9_]*/
    NUMERO: /\d+(\.\d+)?/
    OPERADOR: /[\+\-\*\/]/
    WS: /\s+/
    %ignore WS
"""

parser = Lark(gramatica, parser='lalr', lexer='standard')

def analizar_lexico(texto):
    try:
        arbol = parser.parse(texto)
        tokens = [f"{token.type}: '{token.value}'" for token in arbol.scan_values(lambda v: isinstance(v, Token))]
        return "\n".join(tokens)
    except UnexpectedInput as e:
        return f"Error de análisis: {e}"
