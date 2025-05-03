import customtkinter as ctk
import subprocess
from anytree import RenderTree

# Reemplaza estos imports con tus módulos reales
from parser import parser, analizar_codigo, lark_to_anytree

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
            tree_text = "Árbol de análisis sintáctico:\n"
            for pre, fill, node in RenderTree(anytree_root):
                tree_text += f"{pre}{node.name}\n"
            tree_text += "\nEl código es válido.\n"
            self.output.insert("end", tree_text)

        for error in errores:
            self.error_output.insert("end", error + "\n")

        # Aquí puedes simular la tabla de símbolos para pruebas:
        simbolos = [
            ["x", "Variable", "int", "global", "0x001", "1", "10", "activo", "-", "1"],
            ["y", "Variable", "float", "local", "0x002", "3", "3.14", "activo", "-", "1"],
        ]
        for fila in simbolos:
            self._agregar_fila(fila)

    def _agregar_fila(self, datos):
        num_fila = self.header_frame.grid_size()[1]  # filas actuales
        if num_fila < 5:
            for i, dato in enumerate(datos):
                texto = dato if dato is not None else "-"
                label = ctk.CTkLabel(self.header_frame, text=texto, anchor="w", padx=5)
                label.grid(row=num_fila, column=i, padx=5, pady=5, sticky="nsew")
        else:
            self._mostrar_archivo()

    def _mostrar_archivo(self):
        #subprocess.Popen(["notepad.exe", "tabla_simbolos.json"])
        pass