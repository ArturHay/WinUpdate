import subprocess
import re
import tkinter as tk
from tkinter import ttk

# Fonction pour mettre à jour l'application sélectionnée
def update_app():
    # Récupère l'élément sélectionné dans le widget table
    selected_item = table_widget.selection()[0]
    # Récupère l'ID de l'application à partir de l'élément sélectionné
    app_id = table_widget.item(selected_item)["values"][1]
    # Construit la commande pour mettre à jour l'application en utilisant l'ID récupéré
    command = f"winget upgrade {app_id}"
    # Exécute la commande et met à jour l'application
    result = subprocess.run(command, shell=True, text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Affiche le résultat dans la console de logs
    log_console.insert(tk.END, result.stdout + result.stderr + "\n")

# Fonction pour créer un widget table avec les en-têtes et les lignes fournies
def create_table_widget(parent, headers, rows):
    table = ttk.Treeview(parent, columns=headers, show="headings", height=len(rows))

    # Configure les en-têtes et les colonnes de la table
    for header in headers:
        table.heading(header, text=header)
        table.column(header, anchor="w")

    # Remplit la table avec les lignes fournies
    for row in rows:
        table.insert("", "end", values=row)

    return table

# Initialise les en-têtes et les lignes
headers = ["Nom", "ID", "Version", "Disponible", "Source"]
rows = []

# Exécute la commande 'winget upgrade' et récupère le résultat
result = subprocess.check_output("winget upgrade", shell=True, text=True, encoding="utf-8")

# Filtre les lignes du résultat pour ne conserver que celles commençant par un caractère non espace
lines = [line for line in result.splitlines() if re.match(r"^\S", line)]

# Extrait les informations de chaque ligne et les ajoute aux lignes
for line in lines[1:]:
    match = re.search(r"^(.+?)\s{2,}(.+?)\s{2,}(.+?)\s{2,}(.+?)\s{2,}(.+)$", line.strip())
    if match:
        rows.append(match.groups())

# Crée la fenêtre principale et la configure
root = tk.Tk()
root.title("Mises à jour disponibles")

# Crée et affiche le widget table
table_widget = create_table_widget(root, headers, rows)
table_widget.pack(padx=10, pady=10)

# Crée et affiche le bouton 'Update App'
update_button = tk.Button(root, text="Update App", command=update_app)
update_button.pack(padx=10, pady=10)

# Crée et affiche la console de logs
log_console = tk.Text(root, wrap=tk.WORD, height=10)
log_console.pack(padx=10, pady=10)

# Démarre la boucle principale de la fenêtre
root.mainloop()
