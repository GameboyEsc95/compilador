from anytree import Node
from .parser import parsear_bloque_seguro

def lark_to_anytree(tree):
    def crear_nodo(lark_node):
        nodo = Node(str(lark_node.data) if hasattr(lark_node, "data") else str(lark_node))
        if hasattr(lark_node, "children"):
            for child in lark_node.children:
                nodo_hijo = crear_nodo(child)
                nodo_hijo.parent = nodo
        return nodo
    return crear_nodo(tree)

def analizar_codigo(codigo):
    arbol, error = parsear_bloque_seguro(codigo)
    errores = []
    if error:
        errores.append(str(error))
    return arbol, errores
