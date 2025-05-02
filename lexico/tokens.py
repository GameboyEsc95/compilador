TOKENS = {
    # Operadores
    "ASIGNACION": r"=",
    "OPERADOR": r"[\+\-\*/%]",
    "COMPARADOR": r"(==|!=|<=|>=|<|>)",
    "LOGICO": r"(and|or|not)",

    # Tipos de datos
    "TIPO": r"(int|float|bool|string)",

    # Identificadores y literales
    "PALABRA": r"[a-zA-Z_][a-zA-Z0-9_]*",
    "NUMERO": r"\d+(\.\d+)?",
    "CADENA": r'"[^"\n]*"',  # cadenas entre comillas dobles

    # Delimitadores
    "PUNTO_COMA": r";",
    "COMA": r",",
    "PARENTESIS_IZQ": r"\(",
    "PARENTESIS_DER": r"\)",
    "LLAVE_IZQ": r"\{",
    "LLAVE_DER": r"\}",

    # Espacios
    "WS": r"\s+",
}

PALABRAS_RESERVADAS = {
    "if", "else", "while", "for", "return", "def", "print", "input",
    "True", "False", "None", "and", "or", "not", "in", "is", "break", "continue"
}
