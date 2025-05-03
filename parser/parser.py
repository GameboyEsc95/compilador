# parser/parser.py

from lark import Lark, Tree
from lark.exceptions import UnexpectedInput, UnexpectedToken
from semantico.a_semantico import AnalizadorSemantico  # Importar el analizador semántico

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

def analizar_codigo(codigo_fuente):
    """
    Analiza el código fuente de manera sintáctica y semántica.
    Retorna el árbol sintáctico y una lista de errores (si existen).
    """
    errores = []
    tree = None
    try:
        # Análisis sintáctico
        tree = parser.parse(codigo_fuente)
        
        # Análisis semántico (nuevo paso)
        analizador_semantico = AnalizadorSemantico()  # Aquí no le pasas ningún argumento
        errores_semanticos = analizador_semantico.analizar(tree)  # Ahora pasas el árbol para ser analizado
        errores.extend(errores_semanticos)
        
    except UnexpectedToken as e:
        errores.append(f"Error de sintaxis: Token inesperado '{e.token}' en la línea {e.line}, columna {e.column}.")
    except UnexpectedInput as e:
        errores.append(f"Error de entrada inesperada: {str(e)}")
    except Exception as e:
        errores.append(f"Error general: {str(e)}")
    
    return tree, errores

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
