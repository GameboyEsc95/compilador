import customtkinter as ctk
import subprocess
from anytree import RenderTree
from interfaz.crear_tabla import *
import os               
from datetime import datetime 
from tkinter import messagebox

from analizador import parser, analizar_codigo, lark_to_anytree

class InterfazApp:
    def __init__(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.ventana = ctk.CTk()
        self.ventana.title("Analizador Sintáctico con Tabla de Símbolos")
        self.ventana.geometry("1000x700")
        self._crear_widgets()
        self._crear_tabla_simbolos()
        self.ventana.mainloop()

    def _crear_widgets(self):
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self.ventana)
        self.frame_principal.pack(padx=10, pady=10, fill="both", expand=True)

        # Subdivisión en izquierda y derecha
        self.frame_izquierdo = ctk.CTkFrame(self.frame_principal)
        self.frame_izquierdo.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.frame_derecho = ctk.CTkFrame(self.frame_principal)
        self.frame_derecho.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Textbox de código fuente
        self.textbox = ctk.CTkTextbox(self.frame_izquierdo, width=450, height=300)
        self.textbox.pack(pady=10, padx=10, fill="both", expand=True)

        # Botón compilar
        boton_compilar = ctk.CTkButton(self.frame_izquierdo, text="Compilar", command=self._compilar)
        boton_compilar.pack(pady=5)

        # Área de salida de árbol
        self.output = ctk.CTkTextbox(self.frame_derecho, width=440, height=150)
        self.output.pack(pady=5, padx=5, fill="both", expand=True)

        # Área de errores
        self.error_output = ctk.CTkTextbox(self.frame_derecho, width=440, height=150, text_color="red")
        self.error_output.pack(pady=5, padx=5, fill="both", expand=True)

    def _crear_tabla_simbolos(self):
        encabezados = ['Identificador', 'Categoría', 'Tipo de dato', 'Ámbito', 
                       'Dirección de memoria', 'Línea de declaración', 'Valor', 
                       'Estado', 'Estructura', 'Contador ']

        bottom_frame = ctk.CTkFrame(self.ventana)
        bottom_frame.pack(pady=10, fill="x")

        self.header_frame = ctk.CTkFrame(bottom_frame)
        self.header_frame.pack(fill="x")

        for i, encabezado in enumerate(encabezados):
            label = ctk.CTkLabel(self.header_frame, text=encabezado, anchor="w", padx=5)
            label.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            self.header_frame.grid_columnconfigure(i, weight=1)
    

    def _compilar(self):
    
        self.output.delete("1.0", "end")
        self.error_output.delete("1.0", "end")

        codigo = self.textbox.get("1.0", "end").strip()
        tree, errores = analizar_codigo(codigo)
        
        if tree:
            anytree_root = lark_to_anytree(tree)
            tabla_simulada = extraer_tabla_simbolos(tree)
            print(f"Tabla: {tabla_simulada}" )
            tree_text = "Árbol de análisis sintáctico:\n"
            print(anytree_root)
            i = 0
            for pre, fill, node in RenderTree(anytree_root):
                i += 1
                print(f"pre: {pre}, node {node.name}", fill, i)
                tree_text += f"{pre}{node.name}\n"
            tree_text += "\nEl código es válido.\n"
            self.output.insert("end", tree_text)


        for error in errores:
            self.error_output.insert("end", error + "\n")
        simbolos =[]
        for json in tabla_simulada:
            lista = []
            lista.append(json['identifier'])
            lista.append(json['tipo'])
            lista.append(json['dirección'])
            lista.append(json['valor'])
            simbolos.append(lista)
            print(simbolos)
        # Aquí puedes simular la tabla de símbolos para pruebas:
        for fila in simbolos:
            self._agregar_fila(fila, tabla_simulada)
        
        if len(simbolos) >= 5:
                self._mostrar_archivo(tabla_simulada)

    def _agregar_fila(self, datos, tabla):
        num_fila = self.header_frame.grid_size()[1]  # filas actuales
        if num_fila <= 4:
            for i, dato in enumerate(datos):
                texto = dato if dato is not None else "-"
                label = ctk.CTkLabel(self.header_frame, text=texto, anchor="w", padx=5)
                label.grid(row=num_fila, column=i, padx=5, pady=5, sticky="nsew")
        

    def _mostrar_archivo(self, tabla):

        nombre_carpeta = "Tablas_simbolos"
        try:
            os.makedirs(nombre_carpeta, exist_ok=True)
            #print(f"Directorio '{nombre_carpeta}' asegurado/creado.")
        except OSError as error:

            print(f"Error al crear el directorio '{nombre_carpeta}': {error}")
            # Podrías querer detener el script aquí o guardar en el directorio actual
            nombre_carpeta = "." # Guarda en el directorio actual como fallback (opcional)

        ahora = datetime.now()
        timestamp = ahora.strftime("%y%m%d%H%M%S") 
        nombre_archivo_base = f"tabla_simbolos_{timestamp}.txt"
        #Ruta completa
        ruta_completa_archivo = os.path.join(nombre_carpeta, nombre_archivo_base)
        print(f"Se guardará el archivo en: {ruta_completa_archivo}")

        try:
            with open(ruta_completa_archivo, 'w', encoding='utf-8') as archivo:
                
                archivo.write(str(tabla))
            if messagebox.askyesno(nombre_archivo_base, "archivo creado correctamente ¿Quieres abrirlo?"):
                os.startfile(ruta_completa_archivo)
            else: 
                pass

            #print(f"Archivo '{nombre_archivo_base}' guardado exitosamente en '{nombre_carpeta}'.")

        except IOError as error:
            # Captura errores específicos de lectura/escritura de archivos
            print(f"Error al escribir en el archivo '{ruta_completa_archivo}': {error}")
        except Exception as e:
            # Captura cualquier otro error inesperado
            print(f"Ocurrió un error inesperado: {e}")
