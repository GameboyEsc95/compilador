from lark import Lark, Token, UnexpectedInput
from tokens import TOKENS, PALABRAS_RESERVADAS

def generar_gramatica():
    reglas = []

    reglas.append("start: (" + " | ".join(TOKENS.keys()) + ")*")
    
    for nombre, regex in TOKENS.items():
        reglas.append(f"{nombre}: /{regex}/")

    reglas.append("%ignore WS")  # ignorar espacios en blanco
    return "\n".join(reglas)

gramatica = generar_gramatica()
parser = Lark(gramatica, parser='lalr', lexer='standard')


def analizar_lexico(texto):
    try:
        arbol = parser.parse(texto)
        tokens = []
        for token in arbol.scan_values(lambda v: isinstance(v, Token)):
            if token.type == "PALABRA":
                if token.value in PALABRAS_RESERVADAS:
                    tokens.append(f"RESERVADA: '{token.value}'")
                elif token.value in {"int", "float", "bool", "string"}:
                    tokens.append(f"TIPO: '{token.value}'")
                else:
                    tokens.append(f"IDENTIFICADOR: '{token.value}'")

        return "\n".join(tokens)
    except UnexpectedInput as e:
        return f"Error de análisis: {e}"
