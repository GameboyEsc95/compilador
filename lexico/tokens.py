# tokens.py

PALABRAS_RESERVADAS = {
    "if", "else", "while", "for", "return", "print", "int", "float", "bool", "true", "false"
}

TOKENS = {
    "ASIGNACION": "=",
    "OPERADOR_SUMA": r"\+",
    "OPERADOR_RESTA": r"-",
    "OPERADOR_MULT": r"\*",
    "OPERADOR_DIV": r"/",
    "PARENTESIS_IZQ": r"\(",
    "PARENTESIS_DER": r"\)",
    "LLAVE_IZQ": r"\{",
    "LLAVE_DER": r"\}",
    "IDENTIFICADOR": r"[a-zA-Z_][a-zA-Z0-9_]*",
    "NUMERO": r"\d+(\.\d+)?",
}
