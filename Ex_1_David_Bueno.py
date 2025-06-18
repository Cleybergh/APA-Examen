import tkinter as tk
from tkinter import filedialog
import re

def seleccionar_archivo_entrada():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

def seleccionar_archivo_salida():
    root = tk.Tk()
    root.withdraw()
    return filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

def normalizar_horas(texto):
    texto = re.sub(r'(\d{1,2})h(\d{1,2})m', lambda m: f"{int(m[1]):02d}:{int(m[2]):02d}", texto)
    texto = re.sub(r'(\d{1,2})h', lambda m: f"{int(m[1]):02d}:00", texto)

    texto = re.sub(r'(\d{1,2})\s+y\s+media', lambda m: f"{int(m[1]):02d}:30", texto)
    texto = re.sub(r'(\d{1,2})\s+y\s+cuarto', lambda m: f"{int(m[1]):02d}:15", texto)
    texto = re.sub(r'(\d{1,2})\s+menos\s+cuarto', lambda m: f"{(int(m[1]) - 1)%24:02d}:45", texto)

    texto = re.sub(r'(\d{1,2})\s+de\s+la\s+mañana', lambda m: f"{int(m[1])%12:02d}:00", texto)
    texto = re.sub(r'(\d{1,2})\s+de\s+la\s+tarde', lambda m: f"{(int(m[1])%12 + 12):02d}:00", texto)
    texto = re.sub(r'(\d{1,2})\s+de\s+la\s+noche', lambda m: f"{0 if int(m[1]) == 12 else int(m[1])%24:02d}:00", texto)

    texto = re.sub(r'(\d{1,2})\s+en\s+punto', lambda m: f"{int(m[1]):02d}:00", texto)

    return texto

def procesar_archivo():
    entrada = seleccionar_archivo_entrada()
    if not entrada:
        print("No se seleccionó archivo de entrada.")
        return

    salida = seleccionar_archivo_salida()
    if not salida:
        print("No se seleccionó archivo de salida.")
        return

    with open(entrada, 'r', encoding='utf-8') as f:
        contenido = f.read()

    contenido_normalizado = normalizar_horas(contenido)

    with open(salida, 'w', encoding='utf-8') as f:
        f.write(contenido_normalizado)

    print("Normalización completa. Archivo guardado en:", salida)

if __name__ == "__main__":
    procesar_archivo()
