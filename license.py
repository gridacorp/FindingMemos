import tkinter as tk
import os
import uuid

# --- Generación y almacenamiento de ID de instalación único ---
# Se guarda en un archivo oculto junto al script para persistir entre ejecuciones.
ID_FILE = os.path.join(os.path.dirname(__file__), '.install_id')
try:
    if os.path.exists(ID_FILE):
        with open(ID_FILE, 'r') as f:
            INSTALL_ID = f.read().strip()
    else:
        INSTALL_ID = str(uuid.uuid4())
        with open(ID_FILE, 'w') as f:
            f.write(INSTALL_ID)
except Exception:
    INSTALL_ID = 'UNKNOWN'

# Tu texto de licencia completo:
LICENSE_TEXT = r"""
iGuanitas Source-Available No Comercial License v1.0

Copyright (C) 2025 Jose Antonio Sifuentes Maltos

...

FIN DE LA LICENCIA
"""

def show_license_and_get_acceptance():
    """Muestra el texto de la licencia en un diálogo y devuelve True si el usuario acepta."""
    dlg = tk.Tk()
    dlg.title("Licencia de Uso - iGuanitas")
    dlg.geometry("700x500")

    txt = tk.Text(dlg, wrap="word")
    txt.insert("1.0", LICENSE_TEXT)
    txt.config(state="disabled")
    txt.pack(fill=tk.BOTH, expand=True)

    accepted = tk.BooleanVar(value=False)
    def on_accept():
        accepted.set(True)
        dlg.destroy()
    def on_decline():
        dlg.destroy()

    frame = tk.Frame(dlg)
    tk.Button(frame, text="Acepto", command=on_accept, width=12).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(frame, text="No acepto", command=on_decline, width=12).pack(side=tk.LEFT, padx=5, pady=5)
    frame.pack()

    dlg.mainloop()
    return accepted.get()