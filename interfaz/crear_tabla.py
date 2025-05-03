import json
from lark import Tree, Token 
def _obtener_info_valor(expr_node):
    try:
        # Asume una estructura simple: expr -> term -> factor -> tipo_valor
        term_node = expr_node.children[0]
        factor_node = term_node.children[0]
        value_node = factor_node.children[0] # Ej: Tree(Token('RULE', 'number'), [Token(...)])
        value_type_token = value_node.data # Ej: Token('RULE', 'number')
        value_literal_token = value_node.children[0] # Ej: Token('SIGNED_NUMBER', '10')

        if value_type_token.value == 'number':
            tipo = "number"
            try:
                # Intenta convertir a entero, si falla, a flotante
                valor = int(value_literal_token.value)
            except ValueError:
                valor = float(value_literal_token.value)
            size = 4 # Tamaño simulado para números
            return valor, tipo, size
        elif value_type_token.value == 'string':
            tipo = "string"
            # Quita las comillas del valor del token
            valor = value_literal_token.value.strip('"')
            size = 8 # Tamaño simulado para strings (ej. puntero + datos)
            return valor, tipo, size
        # TODO: Añadir más tipos si tu gramática los soporta (booleanos, etc.)
        # TODO: Manejar si el factor es otro identificador (x = y)
        # TODO: Manejar expresiones aritméticas (x = 1 + 2) - más complejo

    except (IndexError, AttributeError, ValueError) as e:
        # La estructura no es la esperada o es una expresión no soportada aún
        print(f"Advertencia: No se pudo interpretar la expresión: {expr_node}. Error: {e}")
        pass
    return None, "desconocido", 0 # Valor por defecto o error

import json
from lark import Tree, Token

# ... (código de _obtener_info_valor sin cambios por ahora) ...

def extraer_tabla_simbolos(tree):
    print("--- Iniciando extraer_tabla_simbolos ---") # DEBUG
    if not isinstance(tree, Tree):
        print(f"ERROR: Se esperaba un objeto Tree, se recibió {type(tree)}")
        return []
        
    print(f"Árbol recibido (primer nivel): data={tree.data}, children={tree.children[:5]}...") # DEBUG (muestra un poco del árbol)
    tabla_simbolos = []
    direccion_actual = 0x1000

    nodos_a_visitar = [tree]
    visitados_count = 0 # Contador para evitar bucles infinitos si algo va mal

    while nodos_a_visitar and visitados_count < 1000: # Límite de seguridad
        visitados_count += 1
        nodo = nodos_a_visitar.pop()

        # Ignorar Tokens directamente en la lista principal (si los hubiera)
        if not isinstance(nodo, Tree):
            # print(f"DEBUG: Ignorando nodo (no es Tree): {type(nodo)}") # Descomentar si es necesario
            continue

        print(f"DEBUG: Procesando nodo Tree: data='{nodo.data}' (Tipo: {type(nodo.data)})") # DEBUG crucial

        # --- ¡Prueba este cambio! ---
        # Compara con el string del nombre de la regla
        nombre_regla_asignacion = 'assignment' # <- ¡¡Asegúrate que este sea el nombre correcto!!
        if nodo.data == nombre_regla_asignacion:
            print(f"DEBUG: >>> ¡Nodo '{nombre_regla_asignacion}' encontrado! <<<") # DEBUG
            try:
                identificador_node = nodo.children[0]
                expr_node = nodo.children[1]
                print(f"DEBUG:   identificador_node: {identificador_node}") # DEBUG
                print(f"DEBUG:   expr_node: {expr_node}") # DEBUG

                # Acceso al nombre (puede fallar si la estructura es diferente)
                nombre_identificador = identificador_node.children[0].value
                print(f"DEBUG:   Nombre extraído: {nombre_identificador}") # DEBUG

                # Llamada a la función auxiliar
                valor, tipo, tamano = _obtener_info_valor(expr_node)
                print(f"DEBUG:   Info valor: valor={valor}, tipo={tipo}, tamano={tamano}") # DEBUG

                if valor is not None and tipo != "desconocido":
                    direccion_str = f"0x{direccion_actual:04X}"
                    entrada_tabla = {
                        "identifier": nombre_identificador,
                        "tipo": tipo,
                        "dirección": direccion_str,
                        "valor": valor
                    }
                    print(f"DEBUG:   +++ Añadiendo a tabla: {entrada_tabla}") # DEBUG
                    tabla_simbolos.append(entrada_tabla)
                    direccion_actual += tamano
                else:
                    print(f"DEBUG:   --- No se añadió a tabla (valor={valor}, tipo={tipo})") #DEBUG

            except (IndexError, AttributeError) as e:
                print(f"DEBUG:   *** EXCEPCIÓN al procesar nodo '{nombre_regla_asignacion}': {e} ***") # DEBUG
                # Imprime el nodo problemático para ver su estructura real
                # print(nodo.pretty()) # Descomentar si necesitas ver la estructura detallada
        # --- Fin de la sección de asignación ---

        # Añadir hijos (siempre que sea un Tree) para continuar el recorrido
        # print(f"DEBUG: Añadiendo {len(nodo.children)} hijos a la pila.") # DEBUG
        nodos_a_visitar.extend(reversed(nodo.children))

    if visitados_count >= 1000:
        print("ADVERTENCIA: Se alcanzó el límite de nodos visitados.")

    print(f"--- Finalizando extraer_tabla_simbolos. Tabla final: {tabla_simbolos} ---") # DEBUG
    return tabla_simbolos