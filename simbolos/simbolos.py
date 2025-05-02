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
