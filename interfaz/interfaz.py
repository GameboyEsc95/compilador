import customtkinter as ctk
from lexico.a_lexico import analizar_lexico


class InterfazApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.ventana = ctk.CTk()
        self.ventana.geometry("800x600")
        self.ventana.title("Compilador modular")

        self._crear_widgets()
        self.ventana.mainloop()

    def _crear_widgets(self):
        self._crear_textbox_codigo()
        self._crear_botones_accion()
        self._crear_textbox_consola()

    def _crear_textbox_codigo(self):
        self.textbox = ctk.CTkTextbox(self.ventana, width=750, height=300)
        self.textbox.pack(pady=10)
        self.textbox.insert("0.0", "Escribe tu código aquí...")

    def _crear_botones_accion(self):
        frame_botones = ctk.CTkFrame(self.ventana)
        frame_botones.pack(pady=10)

        self.boton_analizar = ctk.CTkButton(
            frame_botones, text="Analizar", command=self._analizar_codigo)
        self.boton_analizar.pack(side="left", padx=10)

        self.boton_limpiar = ctk.CTkButton(
            frame_botones, text="Limpiar", command=self._limpiar_campos)
        self.boton_limpiar.pack(side="left", padx=10)

    def _crear_textbox_consola(self):
        self.consola = ctk.CTkTextbox(self.ventana, width=750, height=200)
        self.consola.pack(pady=10)
        self.consola.insert("0.0", "Consola de salida...")

    def _analizar_codigo(self):
        codigo = self.textbox.get("0.0", "end").strip()
        self.consola.delete("0.0", "end")
        
        if not codigo:
            self.consola.insert("0.0", "Error: El campo de código está vacío.")
            return

        resultado = analizar_lexico(codigo)
        self.consola.insert("0.0", resultado)


        # Aquí llamaría a tu analizador léxico/sintáctico
        self.consola.delete("0.0", "end")
        self.consola.insert("0.0", f"Procesando:\n{codigo}")

    def _limpiar_campos(self):
        self.textbox.delete("0.0", "end")
        self.consola.delete("0.0", "end")
        self.consola.insert("0.0", "Consola de salida...")

# Ejecución
if __name__ == "__main__":
    app = InterfazApp()
