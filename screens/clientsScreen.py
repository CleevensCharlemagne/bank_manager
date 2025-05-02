import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from database import database
import sqlite3

class ClientsFrame(ctk.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller  # Référence à l'instance de EcranPrincipal

        # Initialisation de la frame et des widgets dans __init__
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(fill="x", padx=10, pady=(20, 10))

        self.sort_by = ctk.CTkComboBox(self.top_frame, values=["Nom", "Date ASC", "Date DSC"])
        self.sort_by.set("Trier par")
        self.sort_by.pack(side="left", padx=5)

        self.search_entry = ctk.CTkEntry(self.top_frame, placeholder_text="Search...")
        self.search_entry.pack(side="left", padx=5, fill="x", expand=True)

        self.search_button = ctk.CTkButton(self.top_frame, text="Search", command=self.search_action, font=("Roboto Medium", 13, "bold"))
        self.search_button.pack(side="left", padx=5)

        self.show_all_button = ctk.CTkButton(self.top_frame, text="Show All", command=self.show_all_action, font=("Roboto Medium", 13, "bold"))
        self.show_all_button.pack(side="left", padx=5)

        # Style pour le titre des colonnes du tableau
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

        # Frame pour le Treeview
        self.tree_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tree_frame.pack(pady=(5, 10), padx=10, fill="both", expand=True)

        # Table TREEVIEW
        columns = ("ID", "Nom", "Prenom", "NIF", "Adresse", "DDN", "Email", "TEL", "Status", "Date enrg.")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)

        # Ajout des scrollbars
        self.v_scroll = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.h_scroll = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        # Placement des éléments dans la grille
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")

        # Permettre au Treeview de s'étendre avec la fenêtre
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        # Remplir le treeView des clients deja presents dans la base de données
        self.load_clients()

        # Boutons en bas
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(fill="x", padx=10, pady=10)

        self.button_row = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        self.button_row.pack(anchor="center")

        self.button1 = ctk.CTkButton(self.button_row, text="Ajouter", command=self.add_action, font=("Roboto Medium", 13, "bold"))
        self.button1.pack(side="left", padx=15)

        self.button2 = ctk.CTkButton(self.button_row, text="Ouvrir", command=self.edit_action, font=("Roboto Medium", 13, "bold"))
        self.button2.pack(side="left", padx=15)

        self.button3 = ctk.CTkButton(self.button_row, text="Quitter", fg_color="#959595", hover_color="#737373", command=self.quit_action, font=("Roboto Medium", 13, "bold"))
        self.button3.pack(side="left", padx=15)

    # Get all clients from tha database
    def load_clients(self):
        # Connect to the database
        conn = sqlite3.connect("banque.db")
        cursor = conn.cursor()

        # Clear existing rows in Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            # Fetch clients from database
            cursor.execute("SELECT * FROM clients")
            rows = cursor.fetchall()

            # Insert rows into Treeview
            for row in rows:
                self.tree.insert("", "end", values=row)
        except sqlite3.Error as e:
            print(f"Erreur lors du chargement des clients : {e}")
        finally:
            # Close DB connection
            conn.close()

    # Méthodes d'action (exemples)
    def search_action(self):
        print("Search clicked")

    def show_all_action(self):
        print("Show all clicked")

    def add_action(self):
        print("Add clicked")

    def edit_action(self):
        print("Edit clicked")

    def delete_action(self):
        print("Delete clicked")

    def quit_action(self):
        """Lorsque l'on clique sur 'Quitter', revenir à l'écran principal."""
        self.controller.revenir_accueil()  # Appel à revenir_accueil de EcranPrincipal
