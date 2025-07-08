import tkinter as tk from tkinter import filedialog, messagebox import pdfplumber import os import webbrowser

Importar la licencia y la telemetría

from license import show_license_and_get_acceptance import telemetry

Importar la función de "Acerca de"

from acerca_de import mostrar_acerca_de

1) Mostrar licencia y salir si no se acepta

if not show_license_and_get_acceptance(): exit()

2) Enviar evento de inicio a Google Analytics

telemetry.ping_ga_startup()

---- Funciones de la aplicación ----

def seleccionar_pdfs(): archivos = filedialog.askopenfilenames( title="Seleccionar archivos PDF", filetypes=(("Archivos PDF", ".pdf"), ("Todos los archivos", ".*")) ) if archivos: ruta_entry.delete(0, tk.END) ruta_entry.insert(0, "; ".join(archivos))

def buscar_palabra_clave(): rutas_pdfs = ruta_entry.get() palabras_clave = palabra_entry.get()

if not rutas_pdfs:
    messagebox.showwarning("Advertencia", "Por favor, selecciona al menos un archivo PDF.")
    return
if not palabras_clave:
    messagebox.showwarning("Advertencia", "Por favor, ingresa al menos una palabra clave.")
    return

try:
    resultados_text.delete("1.0", tk.END)
    rutas = rutas_pdfs.split("; ")
    palabras = [p.strip().lower() for p in palabras_clave.split(",") if p.strip()]
    resultados = []

    for ruta_pdf in rutas:
        if not os.path.exists(ruta_pdf):
            resultados.append(f"Archivo no encontrado: {ruta_pdf}")
            continue

        with pdfplumber.open(ruta_pdf) as pdf:
            for num_pagina, pagina in enumerate(pdf.pages, start=1):
                texto = pagina.extract_text()
                if texto:
                    texto = texto.replace("\n", " ")
                    for palabra in palabras:
                        inicio = 0
                        while (pos := texto.lower().find(palabra, inicio)) != -1:
                            ic = max(pos - 100, 0)
                            fc = min(pos + len(palabra) + 100, len(texto))
                            contexto = texto[ic:fc].strip()
                            resultados.append(
                                f"Archivo: {os.path.basename(ruta_pdf)}\n"
                                f"Página {num_pagina}: ...{contexto}...\n"
                            )
                            inicio = pos + len(palabra)

    if resultados:
        resultados_text.insert(tk.END, "\n".join(resultados))
    else:
        resultados_text.insert(tk.END, "No se encontraron coincidencias.")

except Exception as e:
    messagebox.showerror("Error", f"Ocurrió un error al procesar los PDFs: {e}")

def exportar_resultados(): contenido = resultados_text.get("1.0", tk.END).strip() if not contenido: messagebox.showwarning("Advertencia", "No hay resultados para exportar.") return

archivo = filedialog.asksaveasfilename(
    title="Guardar resultados",
    defaultextension=".txt",
    filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
)
if archivo:
    try:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(contenido)
        messagebox.showinfo("Éxito", f"Resultados exportados correctamente a {archivo}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

---- Interfaz gráfica ----

ventana = tk.Tk() ventana.title("Finding Memo, by Jose Sifuentes (AGU - TP)")

Menú de la aplicación

menu_bar = tk.Menu(ventana)

Menú Ayuda

ayuda_menu = tk.Menu(menu_bar, tearoff=0) ayuda_menu.add_command(label="Acerca de", command=mostrar_acerca_de) menu_bar.add_cascade(label="Ayuda", menu=ayuda_menu) ventana.config(menu=menu_bar)

Controles

tk.Label(ventana, text="Archivos PDF:").grid(row=0, column=0, padx=10, pady=5) ruta_entry = tk.Entry(ventana, width=50) ruta_entry.grid(row=0, column=1, padx=10, pady=5) tk.Button(ventana, text="Seleccionar", command=seleccionar_pdfs).grid(row=0, column=2, padx=10, pady=5)

tk.Label(ventana, text="Palabras clave (separadas por comas):").grid(row=1, column=0, padx=10, pady=5) palabra_entry = tk.Entry(ventana, width=50) palabra_entry.grid(row=1, column=1, padx=10, pady=5) tk.Button(ventana, text="Buscar", command=buscar_palabra_clave).grid(row=1, column=2, padx=10, pady=5)

Área de resultados

tk.Label(ventana, text="Resultados:").grid(row=2, column=0, padx=10, pady=5, sticky="nw") resultados_text = tk.Text(ventana, width=70, height=20) resultados_text.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

Botones inferior

tk.Button(ventana, text="Exportar Resultados", command=exportar_resultados).grid(row=3, column=1, pady=10)

Botón de donación en PayPal

tk.Button(ventana, text="Donar en PayPal", command=lambda: webbrowser.open("https://www.paypal.com/donate/?hosted_button_id=KQZ5A7HXTULZL"), bg="#0070BA", fg="white").grid(row=3, column=2, pady=10)

ventana.mainloop()

