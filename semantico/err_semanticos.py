class ErrorSemantico(Exception):
    """Clase base para todos los errores semánticos."""

    def __init__(self, mensaje, linea=None):
        self.mensaje = mensaje
        self.linea = linea

    def __str__(self):
        if self.linea is not None:
            return f"[Línea {self.linea}] Error semántico: {self.mensaje}"
        return f"Error semántico: {self.mensaje}"


# ----------------------
# Errores de Tipos
# ----------------------

class ErrorTipoIncompatible(ErrorSemantico):
    def __init__(self, operador, tipo1, tipo2, linea):
        mensaje = f"Tipos incompatibles: no se puede aplicar '{operador}' entre '{tipo1}' y '{tipo2}'."
        super().__init__(mensaje, linea)


class ErrorAsignacionInvalida(ErrorSemantico):
    def __init__(self, tipo_var, tipo_valor, linea):
        mensaje = f"No se puede asignar un valor de tipo '{tipo_valor}' a una variable de tipo '{tipo_var}'."
        super().__init__(mensaje, linea)


class ErrorRetornoInvalido(ErrorSemantico):
    def __init__(self, tipo_esperado, tipo_retornado, linea):
        mensaje = f"Se esperaba retornar '{tipo_esperado}' pero se encontró '{tipo_retornado}'."
        super().__init__(mensaje, linea)


# ----------------------
# Errores de Declaración y Ámbito
# ----------------------

class ErrorVariableNoDeclarada(ErrorSemantico):
    def __init__(self, nombre, linea):
        mensaje = f"La variable '{nombre}' no ha sido declarada."
        super().__init__(mensaje, linea)


class ErrorDuplicadoEnAmbito(ErrorSemantico):
    def __init__(self, nombre, linea):
        mensaje = f"El identificador '{nombre}' ya ha sido declarado en este ámbito."
        super().__init__(mensaje, linea)


class ErrorVariableFueraDeAmbito(ErrorSemantico):
    def __init__(self, nombre, linea):
        mensaje = f"Se intentó acceder a '{nombre}' fuera de su ámbito de validez."
        super().__init__(mensaje, linea)


# ----------------------
# Errores de Inicialización y Uso
# ----------------------

class ErrorVariableNoInicializada(ErrorSemantico):
    def __init__(self, nombre, linea):
        mensaje = f"La variable '{nombre}' se ha utilizado sin haber sido inicializada."
        super().__init__(mensaje, linea)


class ErrorModificarConstante(ErrorSemantico):
    def __init__(self, nombre, linea):
        mensaje = f"No se puede modificar el valor de la constante '{nombre}'."
        super().__init__(mensaje, linea)


# ----------------------
# Errores de Funciones
# ----------------------

class ErrorNumeroParametros(ErrorSemantico):
    def __init__(self, nombre, esperados, encontrados, linea):
        mensaje = f"La función '{nombre}' esperaba {esperados} parámetro(s) pero se encontraron {encontrados}."
        super().__init__(mensaje, linea)


class ErrorFuncionSinRetorno(ErrorSemantico):
    def __init__(self, nombre, linea):
        mensaje = f"La función '{nombre}' debe retornar un valor, pero no contiene ninguna instrucción de retorno."
        super().__init__(mensaje, linea)


# ----------------------
# Errores Específicos del Lenguaje
# ----------------------

class ErrorDivisionPorCero(ErrorSemantico):
    def __init__(self, linea):
        mensaje = "Posible división por cero detectada en tiempo de compilación."
        super().__init__(mensaje, linea)


class ErrorCastingPeligroso(ErrorSemantico):
    def __init__(self, tipo_origen, tipo_destino, linea):
        mensaje = f"Conversión de '{tipo_origen}' a '{tipo_destino}' puede causar pérdida de datos."
        super().__init__(mensaje, linea)
