# parser/parser.py

from lark import Lark, Tree
from lark.exceptions import UnexpectedInput

# Leer gramática desde archivo externo
with open("gramatica.ebnf", "r", encoding="utf-8") as file:
    GRAMATICA = file.read()
    print("Gramática cargada correctamente:\n")
    print(GRAMATICA)


# Crear el parser usando LALR
try:
    parser = Lark(GRAMATICA, start="start", parser="lalr", lexer="basic")
    print("✅ El parser fue creado correctamente.")
except Exception as e:
    print("❌ Error al crear el parser:")
    print(e)



def parsear_codigo(codigo):
    """
    Parsea el código fuente completo y retorna el árbol sintáctico.
    Lanza excepciones si hay errores.
    """
    return parser.parse(codigo)


def parsear_bloque_seguro(codigo):
    """
    Parsea el código de forma segura.
    Retorna (árbol, error) donde uno de los dos puede ser None.
    """
    try:
        arbol = parser.parse(codigo)
        return arbol, None
    except UnexpectedInput as e:
        return None, e
    
# Agregado temporalmente para pruebas
if __name__ == "__main__":
    ejemplo = "print(1 + 2);"  # Ajusta esto según tu lenguaje
    try:
        arbol = parser.parse(ejemplo)
        print("✅ Cadena de prueba parseada exitosamente.")
        print(arbol.pretty())
    except Exception as e:
        print("❌ Error al parsear la cadena de prueba:")
        print(e)

