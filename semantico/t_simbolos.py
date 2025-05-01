from collections import defaultdict

# ----------------------------
# Clase Base: Identificador
# ----------------------------

class Identificador:
    def __init__(self, nombre, tipo, ambito, linea_decl, inicializado=False):
        self.nombre = nombre
        self.tipo = tipo  # Tipo primitivo, estructurado, puntero, etc.
        self.ambito = ambito  # Nivel de anidamiento
        self.linea_declaracion = linea_decl
        self.inicializado = inicializado
        self.referencias = 0

    def registrar_referencia(self):
        self.referencias += 1


# ----------------------------
# Subclase: Variable
# ----------------------------

class Variable(Identificador):
    def __init__(self, nombre, tipo, ambito, linea_decl,
                 tamanio_memoria=0, direccion_relativa=0,
                 constante=False, modificable=True):
        super().__init__(nombre, tipo, ambito, linea_decl)
        self.tamanio_memoria = tamanio_memoria
        self.direccion_relativa = direccion_relativa
        self.constante = constante
        self.modificable = modificable


# ----------------------------
# Subclase: Funcion / Procedimiento
# ----------------------------

class Funcion(Identificador):
    def __init__(self, nombre, tipo_retorno, firma, lista_parametros, linea_decl):
        super().__init__(nombre, 'funcion', None, linea_decl)
        self.tipo_retorno = tipo_retorno
        self.firma = firma  # Puede ser un string o tupla con tipos
        self.lista_parametros = lista_parametros  # Lista de dicts o tuplas
        self.tabla_simbolos_local = TablaSimbolos()  # Ámbito local
        self.implementada = False


# ----------------------------
# Subclase: Tipo definido por el usuario
# ----------------------------

class TipoDefinido(Identificador):
    def __init__(self, nombre, estructura_interna, metodos_asociados, herencia=None, restricciones=None):
        super().__init__(nombre, 'tipo_usuario', None, None)
        self.estructura_interna = estructura_interna  # Campos internos del tipo
        self.metodos_asociados = metodos_asociados  # Métodos definidos para el tipo
        self.herencia = herencia
        self.restricciones = restricciones or []


# ----------------------------
# Tabla de Símbolos con Ámbitos
# ----------------------------

class TablaSimbolos:
    def __init__(self):
        # Pila de diccionarios para representar los distintos niveles de ámbito
        self.ambitos = [{}]
        self.nivel_actual = 0

    def entrar_ambito(self):
        self.nivel_actual += 1
        self.ambitos.append({})

    def salir_ambito(self):
        if self.nivel_actual > 0:
            self.ambitos.pop()
            self.nivel_actual -= 1
        else:
            raise RuntimeError("No se puede salir del ámbito global")

    def insertar(self, identificador):
        actual = self.ambitos[-1]
        if identificador.nombre in actual:
            raise ValueError(f"Identificador '{identificador.nombre}' ya declarado en este ámbito.")
        actual[identificador.nombre] = identificador

    def buscar(self, nombre):
        for ambito in reversed(self.ambitos):
            if nombre in ambito:
                return ambito[nombre]
        return None  # No encontrado

    def buscar_en_ambito_actual(self, nombre):
        return self.ambitos[-1].get(nombre, None)

    def mostrar_tabla(self):
        for nivel, ambito in enumerate(self.ambitos):
            print(f"Ámbito nivel {nivel}:")
            for nombre, simbolo in ambito.items():
                print(f"  {nombre} -> {type(simbolo).__name__}, tipo: {simbolo.tipo}, línea: {simbolo.linea_declaracion}")
