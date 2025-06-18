import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import subprocess

# --- FUNCIONES FANTASMA (INTERFAZ) ---
# Estas llamadas se espera que existan con esta interfaz.
# No se evalúa su contenido.

def estereo2mono(ficEste, ficMono, canal=2):
    print(f"estereo2mono({ficEste}, {ficMono}, canal={canal})")

def mono2stereo(ficIzq, ficDer, ficEste):
    print(f"mono2stereo({ficIzq}, {ficDer}, {ficEste})")

def codEstereo(ficEste, ficCod):
    print(f"codEstereo({ficEste}, {ficCod})")

def decEstereo(ficCod, ficEste):
    print(f"decEstereo({ficCod}, {ficEste})")

# --- UTILIDADES ---
def seleccionar_archivo(titulo="Seleccionar archivo"):
    return filedialog.askopenfilename(title=titulo, filetypes=[("WAV files", "*.wav")])

def seleccionar_multiples_archivos(titulo="Seleccionar archivos"):
    return filedialog.askopenfilenames(title=titulo, filetypes=[("WAV files", "*.wav")])

def guardar_como():
    return filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])

def reproducir(path):
    try:
        if sys.platform == "win32":
            # Windows: usar start
            subprocess.Popen(['start', '', path], shell=True)
        elif sys.platform.startswith("linux"):
            # Linux: usar aplay o paplay (si tienes uno instalado)
            try:
                subprocess.Popen(['aplay', path])
            except FileNotFoundError:
                subprocess.Popen(['paplay', path])
        else:
            messagebox.showerror("Error", "Sistema operativo no soportado para reproducción.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo reproducir el audio:\n{e}")

class MonoGUI:
    def __init__(self, root):
        self.root = root
        root.title("APA - Conversor Mono/Estéreo")
        root.geometry("700x500")

        # Estilos ttk
        self.style = ttk.Style()
        self.style.theme_use('default')

        self.style.configure("Dark.TFrame", background="#3a3a3a")
        self.style.configure("Dark.TLabel", background="#3a3a3a", foreground="white")
        self.style.configure("Dark.TButton", background="#555555", foreground="white")
        self.style.map("Dark.TButton",
                       background=[('active', '#777777')])

        # Fondo de la ventana root
        root.configure(bg="#2b2b2b")

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True)

        self.tab_estereo_a_mono()
        self.tab_mono_a_estereo()
        self.tab_codifica()
        self.tab_descodifica()

    def crear_titulo(self, parent, texto):
        # Título grande con tk.Label que sí admite bg/fg
        label = tk.Label(parent, text=texto, font=("Helvetica", 18, "bold"), bg="#3a3a3a", fg="#aaddff")
        label.pack(pady=10)

    def tab_estereo_a_mono(self):
        tab = ttk.Frame(self.tabs, style="Dark.TFrame")
        self.tabs.add(tab, text="Estéreo a Mono")

        self.crear_titulo(tab, "Conversión Estéreo a Mono")

        self.eam_input = tk.StringVar()
        self.eam_output = tk.StringVar()
        self.eam_canal = tk.IntVar(value=2)

        ttk.Label(tab, text="Archivo estéreo:", style="Dark.TLabel").pack(anchor="w", padx=10, pady=3)
        ttk.Entry(tab, textvariable=self.eam_input, width=60).pack(padx=10, pady=2)
        ttk.Button(tab, text="Seleccionar", command=lambda: self.eam_input.set(seleccionar_archivo()), style="Dark.TButton").pack(padx=10, pady=3)

        ttk.Button(tab, text="Reproducir entrada", command=lambda: reproducir(self.eam_input.get()), style="Dark.TButton").pack(padx=10, pady=5)

        ttk.Label(tab, text="Canal (0: Izq, 1: Der, 2: Suma, 3: Dif):", style="Dark.TLabel").pack(anchor="w", padx=10, pady=3)
        ttk.Entry(tab, textvariable=self.eam_canal).pack(padx=10, pady=2)

        ttk.Button(tab, text="Guardar como...", command=lambda: self.eam_output.set(guardar_como()), style="Dark.TButton").pack(padx=10, pady=3)
        ttk.Button(tab, text="Convertir", command=self.convertir_eam, style="Dark.TButton").pack(padx=10, pady=5)
        ttk.Button(tab, text="Reproducir salida", command=lambda: reproducir(self.eam_output.get()), style="Dark.TButton").pack(padx=10, pady=5)

    def convertir_eam(self):
        try:
            estereo2mono(self.eam_input.get(), self.eam_output.get(), self.eam_canal.get())
            messagebox.showinfo("OK", "Conversión completada.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def tab_mono_a_estereo(self):
        tab = ttk.Frame(self.tabs, style="Dark.TFrame")
        self.tabs.add(tab, text="Mono a Estéreo")

        self.crear_titulo(tab, "Conversión Mono a Estéreo")

        self.mas_izq = tk.StringVar()
        self.mas_der = tk.StringVar()
        self.mas_out = tk.StringVar()

        ttk.Label(tab, text="Canal Izquierdo:", style="Dark.TLabel").pack(anchor="w", padx=10, pady=3)
        ttk.Entry(tab, textvariable=self.mas_izq, width=60).pack(padx=10, pady=2)
        ttk.Button(tab, text="Seleccionar", command=lambda: self.mas_izq.set(seleccionar_archivo()), style="Dark.TButton").pack(padx=10, pady=3)
        ttk.Button(tab, text="Reproducir Izq", command=lambda: reproducir(self.mas_izq.get()), style="Dark.TButton").pack(padx=10, pady=3)

        ttk.Label(tab, text="Canal Derecho:", style="Dark.TLabel").pack(anchor="w", padx=10, pady=3)
        ttk.Entry(tab, textvariable=self.mas_der, width=60).pack(padx=10, pady=2)
        ttk.Button(tab, text="Seleccionar", command=lambda: self.mas_der.set(seleccionar_archivo()), style="Dark.TButton").pack(padx=10, pady=3)
        ttk.Button(tab, text="Reproducir Der", command=lambda: reproducir(self.mas_der.get()), style="Dark.TButton").pack(padx=10, pady=3)

        ttk.Button(tab, text="Guardar como...", command=lambda: self.mas_out.set(guardar_como()), style="Dark.TButton").pack(padx=10, pady=5)
        ttk.Button(tab, text="Unir", command=self.convertir_mas, style="Dark.TButton").pack(padx=10, pady=5)
        ttk.Button(tab, text="Reproducir salida", command=lambda: reproducir(self.mas_out.get()), style="Dark.TButton").pack(padx=10, pady=5)

    def convertir_mas(self):
        try:
            mono2stereo(self.mas_izq.get(), self.mas_der.get(), self.mas_out.get())
            messagebox.showinfo("OK", "Conversión completada.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def tab_codifica(self):
        tab = ttk.Frame(self.tabs, style="Dark.TFrame")
        self.tabs.add(tab, text="Codifica Estéreo")

        self.crear_titulo(tab, "Codificación Estéreo")

        self.cod_in = tk.StringVar()
        self.cod_out = tk.StringVar()

        ttk.Label(tab, text="Archivo estéreo:", style="Dark.TLabel").pack(anchor="w", padx=10, pady=3)
        ttk.Entry(tab, textvariable=self.cod_in, width=60).pack(padx=10, pady=2)
        ttk.Button(tab, text="Seleccionar", command=lambda: self.cod_in.set(seleccionar_archivo()), style="Dark.TButton").pack(padx=10, pady=3)
        ttk.Button(tab, text="Reproducir", command=lambda: reproducir(self.cod_in.get()), style="Dark.TButton").pack(padx=10, pady=5)

        ttk.Button(tab, text="Guardar como...", command=lambda: self.cod_out.set(guardar_como()), style="Dark.TButton").pack(padx=10, pady=5)
        ttk.Button(tab, text="Codificar", command=self.convertir_cod, style="Dark.TButton").pack(padx=10, pady=5)

    def convertir_cod(self):
        try:
            codEstereo(self.cod_in.get(), self.cod_out.get())
            messagebox.showinfo("OK", "Codificación completada.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def tab_descodifica(self):
        tab = ttk.Frame(self.tabs, style="Dark.TFrame")
        self.tabs.add(tab, text="Descodifica Estéreo")

        self.crear_titulo(tab, "Descodificación Estéreo")

        self.dec_in = tk.StringVar()
        self.dec_out = tk.StringVar()

        ttk.Label(tab, text="Archivo codificado:", style="Dark.TLabel").pack(anchor="w", padx=10, pady=3)
        ttk.Entry(tab, textvariable=self.dec_in, width=60).pack(padx=10, pady=2)
        ttk.Button(tab, text="Seleccionar", command=lambda: self.dec_in.set(seleccionar_archivo()), style="Dark.TButton").pack(padx=10, pady=3)
        ttk.Button(tab, text="Reproducir", command=lambda: reproducir(self.dec_in.get()), style="Dark.TButton").pack(padx=10, pady=5)

        ttk.Button(tab, text="Guardar como...", command=lambda: self.dec_out.set(guardar_como()), style="Dark.TButton").pack(padx=10, pady=5)
        ttk.Button(tab, text="Descodificar", command=self.convertir_dec, style="Dark.TButton").pack(padx=10, pady=5)
        ttk.Button(tab, text="Reproducir salida", command=lambda: reproducir(self.dec_out.get()), style="Dark.TButton").pack(padx=10, pady=5)

    def convertir_dec(self):
        try:
            decEstereo(self.dec_in.get(), self.dec_out.get())
            messagebox.showinfo("OK", "Descodificación completada.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = MonoGUI(root)
    root.mainloop()