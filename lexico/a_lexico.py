from lark import Lark, Token, UnexpectedInput
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tokens import TOKENS, PALABRAS_RESERVADAS
from parser.parser import *

def generar_gramatica():
    reglas = []

    reglas.append("start: (" + " | ".join(TOKENS.keys()) + ")*")
    
    for nombre, regex in TOKENS.items():
        reglas.append(f"{nombre}: /{regex}/")

    reglas.append("%ignore WS")  # ignorar espacios en blanco
    return "\n".join(reglas)

gramatica = generar_gramatica()



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
