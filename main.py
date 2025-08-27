import tkinter as tk
from tkinter import messagebox
import pyperclip
from zabbix_connect import ZabbixConnect  # Asegúrate de que el archivo zabbix_connect.py esté en el mismo directorio

class ZabbixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zabbix Impresoras")
        
        self.output_message = tk.StringVar()
        
        # Configurar la interfaz de usuario
        self.create_widgets()
        
        # Obtener el mensaje inicial
        self.fetch_message()
    
    def create_widgets(self):
        # Area de texto para mostrar el mensaje
        self.text_area = tk.Text(self.root, height=20, width=80)
        self.text_area.pack(pady=10)
        
        # Botón para copiar el mensaje
        self.copy_button = tk.Button(self.root, text="Copiar al portapapeles", command=self.copy_to_clipboard)
        self.copy_button.pack(pady=5)
        
        # Botón para actualizar el mensaje
        self.update_button = tk.Button(self.root, text="Actualizar mensaje", command=self.fetch_message)
        self.update_button.pack(pady=5)
    
    def fetch_message(self):
        try:
            zabbix = ZabbixConnect()
            resultado = zabbix.obtener_mensaje()
            if resultado:
                message, fuera_de_rango = resultado
                # Mostrar diálogos por cada impresora fuera de rango
                for impresora in fuera_de_rango:
                    texto = (
                        f"El valor del contador para {impresora['nombre']} está fuera del rango permitido.\n"
                        f"Valor actual: {impresora['actual']}\n"
                        f"Valor mes anterior: {impresora['anterior']}\n\n"
                        "¿Desea ignorar y continuar o cancelar el proceso?"
                    )
                    respuesta = messagebox.askquestion(
                        "Contador fuera de rango", texto, icon='warning'
                    )
                    if respuesta == 'no':
                        messagebox.showinfo("Proceso cancelado", "El proceso ha sido cancelado por el usuario.")
                        return
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, message)
                self.output_message.set(message)
            else:
                messagebox.showerror("Error", "No se pudo obtener el mensaje de Zabbix.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
    
    def copy_to_clipboard(self):
        message = self.output_message.get()
        if message:
            pyperclip.copy(message)
            messagebox.showinfo("Información", "Mensaje copiado al portapapeles.")
        else:
            messagebox.showwarning("Advertencia", "No hay mensaje para copiar.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ZabbixApp(root)
    root.mainloop()