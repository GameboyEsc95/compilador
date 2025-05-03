from simbolos.t_simbolos import TablaSimbolos
from simbolos.simbolos import Variable
from semantico.err_semanticos import *

from lark import Tree

class AnalizadorSemantico:
    def __init__(self):
        self.tabla = TablaSimbolos()
        self.ambito_actual = "global"
        self.errores = []  # Lista para almacenar los errores semánticos encontrados

    def analizar(self, arbol: Tree):
        self._analizar_nodo(arbol)
        self.tabla.guardar_en_json()
        self.tabla.imprimir()
        return self.errores  # Devolvemos la lista de errores

    def _analizar_nodo(self, nodo):
        if isinstance(nodo, Tree):
            metodo = getattr(self, f"_nodo_{nodo.data}", None)
            if metodo:
                try:
                    metodo(nodo)
                except ErrorSemantico as e:
                    self.errores.append(e)
            for hijo in nodo.children:
                self._analizar_nodo(hijo)


    def _nodo_declaracion_variable(self, nodo):
        tipo_nodo = nodo.children[0]
        nombre_token = nodo.children[1]
        linea = nodo.meta.line if hasattr(nodo, 'meta') else None

        if tipo_nodo.data == "tipo" and hasattr(tipo_nodo, 'children') and len(tipo_nodo.children) == 1:
            tipo = tipo_nodo.children[0].value
        elif tipo_nodo.data == "tipo" and hasattr(tipo_nodo, 'value'):
            tipo = tipo_nodo.value
        elif tipo_nodo.data == "tipo" and not hasattr(tipo_nodo, 'value'):
            # Último recurso: buscar el primer token descendiente
            def get_first_token_value(tree):
                if hasattr(tree, 'children'):
                    for child in tree.children:
                        value = get_first_token_value(child)
                        if value:
                            return value
                    return None
                elif hasattr(tree, 'value'):
                    return tree.value
                return None

            tipo = get_first_token_value(tipo_nodo)
            if not tipo:
                raise Exception(f"No se pudo encontrar el valor del tipo en: {tipo_nodo}")
        else:
            raise Exception(f"Estructura inesperada para el tipo: {tipo_nodo}")

        if nombre_token.type == "IDENTIFICADOR":
            nombre = nombre_token.value
        else:
            raise Exception(f"Estructura inesperada en nodo de nombre: {nombre_token}")

        if self.tabla.esta_declarado_en_ambito_actual(nombre):
            raise ErrorDuplicadoEnAmbito(nombre, linea)

        simbolo = Variable(nombre, tipo, self.ambito_actual, linea)
        self.tabla.insertar(simbolo)




    def _nodo_asignacion(self, nodo):
        nombre = nodo.children[0].value
        valor = nodo.children[1]
        linea = nodo.meta.line if hasattr(nodo, 'meta') else None

        simbolo = self.tabla.buscar(nombre)
        if not simbolo:
            raise ErrorVariableNoDeclarada(nombre, linea)

        tipo_valor = self._evaluar_tipo(valor)
        if simbolo.tipo != tipo_valor:
            raise ErrorAsignacionInvalida(simbolo.tipo, tipo_valor, linea)

        simbolo.inicializado = True

    def _evaluar_tipo(self, nodo):
        if nodo.data == "numero":
            return "entero"
        elif nodo.data == "cadena":
            return "cadena"
        elif nodo.data == "expresion_binaria":
            tipo_izq = self._evaluar_tipo(nodo.children[0])
            tipo_der = self._evaluar_tipo(nodo.children[2])
            operador = nodo.children[1].value
            if tipo_izq != tipo_der:
                raise ErrorTipoIncompatible(operador, tipo_izq, tipo_der, nodo.meta.line)
            return tipo_izq
        # Pendiente agregar más casos

    def _nodo_bloque(self, nodo):
        self.tabla.abrir_ambito()
        for instruccion in nodo.children:
            self._analizar_nodo(instruccion)
        self.tabla.cerrar_ambito()