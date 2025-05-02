import json
import os
from datetime import datetime

class TablaSimbolos:
    def __init__(self):
        self.pila_ambitos = [{}]  # Pila de diccionarios: cada uno representa un ámbito
        self.archivo_json = "datos/tabla_simbolos.json"
        self._crear_directorio_salida()

    def _crear_directorio_salida(self):
        if not os.path.exists("datos"):
            os.makedirs("datos")

    def abrir_ambito(self):
        """Inicia un nuevo ámbito (por ejemplo, dentro de una función o bloque)"""
        self.pila_ambitos.append({})

    def cerrar_ambito(self):
        """Cierra el ámbito más reciente"""
        if len(self.pila_ambitos) > 1:
            self.pila_ambitos.pop()
        else:
            raise Exception("No se puede cerrar el ámbito global")

    def insertar(self, simbolo):
        """Agrega un nuevo símbolo al ámbito actual"""
        ambito_actual = self.pila_ambitos[-1]
        nombre = simbolo.nombre

        if nombre in ambito_actual:
            raise Exception(f"Error: identificador '{nombre}' ya declarado en este ámbito.")
        ambito_actual[nombre] = simbolo

    def buscar(self, nombre):
        """Busca un símbolo desde el ámbito más interno hacia afuera"""
        for ambito in reversed(self.pila_ambitos):
            if nombre in ambito:
                return ambito[nombre]
        return None

    def esta_declarado_en_ambito_actual(self, nombre):
        """Verifica si un identificador ya está en el ámbito actual"""
        return nombre in self.pila_ambitos[-1]

    def obtener_todos(self):
        """Retorna todos los símbolos visibles (merge de todos los ámbitos)"""
        todos = {}
        for ambito in self.pila_ambitos:
            todos.update(ambito)
        return todos

    def guardar_en_json(self):
        """Guarda el contenido actual en un archivo JSON"""
        datos = {
            nombre: simbolo.to_dict()
            for nombre, simbolo in self.obtener_todos().items()
        }
        with open(self.archivo_json, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    def imprimir(self):
        """Muestra por consola el contenido actual de la tabla"""
        for nivel, ambito in enumerate(self.pila_ambitos):
            print(f"\nÁmbito nivel {nivel}:")
            for simbolo in ambito.values():
                print(simbolo)
# simbolos/simbolos.py

class Identificador:
    def __init__(self, nombre, tipo, ambito, linea):
        self.nombre = nombre
        self.tipo = tipo  # Tipo de dato (primitivo, compuesto, puntero, etc.)
        self.ambito = ambito  # Ej: 'global', 'funcion1'
        self.linea = linea
        self.inicializado = False
        self.referencias = 0

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "tipo": self.tipo,
            "ámbito": self.ambito,
            "línea_declaración": self.linea,
            "inicializado": self.inicializado,
            "referencias": self.referencias
        }

    def __repr__(self):
        return f"[{self.__class__.__name__}] {self.nombre} (tipo: {self.tipo}, ámbito: {self.ambito})"


class Variable(Identificador):
    def __init__(self, nombre, tipo, ambito, linea, direccion=None, tamaño=None, constante=False):
        super().__init__(nombre, tipo, ambito, linea)
        self.direccion = direccion  # Dirección relativa en memoria
        self.tamaño = tamaño        # Tamaño en bytes
        self.constante = constante  # Si es una constante
        self.modificable = not constante

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "categoría": "variable",
            "tamaño": self.tamaño,
            "dirección": self.direccion,
            "constante": self.constante,
            "modificable": self.modificable
        })
        return base


class Funcion(Identificador):
    def __init__(self, nombre, tipo_retorno, ambito, linea, parametros=None, implementada=False):
        super().__init__(nombre, "función", ambito, linea)
        self.tipo_retorno = tipo_retorno
        self.parametros = parametros if parametros else []  # Lista de (nombre, tipo, modo_paso)
        self.implementada = implementada
        self.variables_locales = []  # Puede referenciar a su tabla de símbolos local

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "categoría": "función",
            "tipo_retorno": self.tipo_retorno,
            "parámetros": self.parametros,
            "implementada": self.implementada
        })
        return base


class TipoUsuario(Identificador):
    def __init__(self, nombre, ambito, linea, estructura=None, metodos=None, herencia=None, restricciones=None):
        super().__init__(nombre, "tipo_usuario", ambito, linea)
        self.estructura = estructura if estructura else {}  # Campos y tipos
        self.metodos = metodos if metodos else []          # Lista de métodos asociados
        self.herencia = herencia                           # Nombre del tipo padre
        self.restricciones = restricciones if restricciones else []

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "categoría": "tipo_definido_usuario",
            "estructura": self.estructura,
            "métodos": self.metodos,
            "herencia": self.herencia,
            "restricciones": self.restricciones
        })
        return base
