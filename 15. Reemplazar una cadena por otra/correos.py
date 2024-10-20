import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
import os

# Crear ventana gráfica
root = tk.Tk()
root.withdraw()  # Ocultar ventana principal

# Pedir al usuario el número que reemplazará el '4'
num = simpledialog.askstring("Entrada", "Ingresa un número para reemplazar '/4/':")
if not num or not num.isdigit():
    messagebox.showerror("Error", "Debes ingresar un número válido.")
    exit()

# Seleccionar archivo .txt original
archivo_txt = filedialog.askopenfilename(
    title="Urgente correo SPOPA.txt",
    filetypes=[("Archivos de texto", "*.txt")]
)

if not archivo_txt:
    messagebox.showerror("Error", "No se seleccionó ningún archivo.")
    exit()

# Leer el contenido del archivo original
with open(archivo_txt, 'r', encoding='utf-8') as archivo:
    contenido = archivo.read()

# Reemplazar /4/ por /#/ donde # es el número dado por el usuario
nuevo_contenido = contenido.replace("/4/", f"/{num}/")

# Guardar el contenido modificado en un nuevo archivo en la misma carpeta
carpeta = os.path.dirname(archivo_txt)
nuevo_archivo = os.path.join(carpeta, "archivo_modificado.txt")

with open(nuevo_archivo, 'w', encoding='utf-8') as archivo:
    archivo.write(nuevo_contenido)

# Notificar al usuario que la operación fue exitosa
messagebox.showinfo("Éxito", f"Archivo modificado guardado como: {nuevo_archivo}")
