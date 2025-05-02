# Dependencias necesarias: pip install lark-parser customtkinter
import customtkinter as ctk
from interfaz.interfaz import *

# Crear la ventana principal
root = ctk.CTk()
root.title("Analizador Sintáctico con Tabla de Símbolos")
root.geometry("950x600")

# Configuración del grid (4 partes)
root.grid_rowconfigure(0, weight=1)  # Fila 1 (parte superior)
root.grid_rowconfigure(1, weight=2)  # Fila 2 (parte inferior)
root.grid_columnconfigure(0, weight=1)  # Columna 1 (izquierda)
root.grid_columnconfigure(1, weight=1)  # Columna 2 (derecha)

# Frame izquierdo (para editor de texto)
frame_izquierdo = ctk.CTkFrame(root)
frame_izquierdo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Frame derecho (para salida de análisis)
frame_derecho = ctk.CTkFrame(root)
frame_derecho.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Frame inferior para la tabla de símbolos
bottom_frame = ctk.CTkFrame(root)
bottom_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Frame izquierdo (para el editor de texto)
text_editor = ctk.CTkTextbox(frame_izquierdo, width=450, height=300)
text_editor.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

# Frame de salida de árbol 
frame_salida_arbol = ctk.CTkFrame(frame_derecho)
frame_salida_arbol.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# Frame errores
frame_errores = ctk.CTkFrame(frame_derecho)
frame_errores.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

# Frame Tabla de símbolos
frame_tabla = ctk.CTkFrame(bottom_frame)
frame_tabla.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

# Áreas de salida (dentro de los frames)
output = ctk.CTkTextbox(frame_salida_arbol, width=440, height=150)
output.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

error_output = ctk.CTkTextbox(frame_errores, width=440, height=150, text_color="red")
error_output.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")



root.mainloop()