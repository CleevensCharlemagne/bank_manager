import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import sqlite3

class CompteFrame(ctk.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller  # Référence à l'instance de EcranPrincipal

        # TOP CONTROLS
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(fill="x", padx=10, pady=(20, 10))

        # Ajouter un champ de recherche
        self.search_entry = ctk.CTkEntry(self.top_frame, placeholder_text="Rechercher...")
        self.search_entry.pack(side="left", padx=5, fill="x", expand=True)

        self.search_button = ctk.CTkButton(self.top_frame, text="Search", command=self.search_action, font=("Roboto Medium", 13, "bold"))
        self.search_button.pack(side="left", padx=5)

        # Style pour le texte des colonnes
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

        # FRAME POUR TREEVIEW
        self.tree_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tree_frame.pack(pady=(5, 10), padx=10, fill="both", expand=True)

        # TREEVIEW TABLE
        columns = ("Numéro de compte", "Nom de compte", "Nom client", "Prenom client", "Solde", "Id_client", "Status", "Créé le", "Fermé le", "type" )
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)

        # Créer les Scrollbars
        self.v_scroll = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.h_scroll = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        # Placement des scrollbars avec la grille
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")

        # Laisser Treeview s'étendre avec la fenêtre
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        # Get all accounts form the database
        self.load_accounts()

        # BOTTOM BUTTONS
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(fill="x", padx=10, pady=10)

        self.button_row = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        self.button_row.pack(anchor="center")

        # Boutons pour ajouter, ouvrir, etc.
        self.button1 = ctk.CTkButton(self.button_row, text="Ajouter", command=self.add_action, font=("Roboto Medium", 13, "bold"))
        self.button1.pack(side="left", padx=15)

        self.button2 = ctk.CTkButton(self.button_row, text="Ouvrir", command=self.edit_action, font=("Roboto Medium", 13, "bold"))
        self.button2.pack(side="left", padx=15)

        self.button3 = ctk.CTkButton(self.button_row, text="Quitter", fg_color="#959595", hover_color="#737373", command=self.quit_action, font=("Roboto Medium", 13, "bold"))
        self.button3.pack(side="left", padx=15)

    # Get all accounts from tha database
    def load_accounts(self):
        """Charge tous les comptes (courant et epargne) depuis la base de données dans le TreeView."""

        # Connect to the database
        conn = sqlite3.connect("banque.db")
        cursor = conn.cursor()

        # Clear existing rows in Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            cursor.execute("""
                SELECT 
                    accounts.account_num, 
                    accounts.account_name, 
                    clients.last_name, 
                    clients.first_name,
                    accounts.balance,
                    accounts.owner_id,  
                    accounts.status, 
                    accounts.creation_date, 
                    accounts.close_date, 
                    accounts.account_type
                FROM accounts
                LEFT JOIN clients ON accounts.owner_id = clients.client_id
                """)

            rows = cursor.fetchall()

            # Insert rows into Treeview
            for row in rows:
                self.tree.insert("", "end", values=row)

        except sqlite3.Error as e:
            print(f"Erreur lors du chargement des comptes : {e}")
        finally:
            conn.close()

    # Méthodes d'action (exemples)
    def search_action(self):
        print("Search clicked")

    def add_action(self):
        print("Add clicked")

    def edit_action(self):
        selected = self.tree.selection()
        if not selected:
            tk.messagebox.showwarning("Avertissement", "Veuillez sélectionner un compte.")
            return

        compte_data = self.tree.item(selected[0], "values")
        CompteDetailsWindow(self, compte_data)

    def quit_action(self):
        """Lorsque l'on clique sur 'Quitter', revenir à l'écran principal."""
        self.controller.revenir_accueil()  # Appel à revenir_accueil de EcranPrincipal

class CompteDetailsWindow(ctk.CTkToplevel):
    def __init__(self, parent, compte_data):
        super().__init__(parent)
        self.title("Détails du compte")
        self.geometry("550x600")

        # Champs de base
        champs_base = [
            ("Numéro de compte", compte_data[0]),
            ("Nom du compte", compte_data[1]),
            ("Nom client", compte_data[2]),
            ("Prénom client", compte_data[3]),
            ("Solde", compte_data[4]),
            ("ID client", compte_data[5]),
            ("Statut", compte_data[6]),
            ("Créé le", compte_data[7]),
            ("Fermé le", compte_data[8]),
            ("Type de compte", compte_data[9])
        ]

        for i, (label_text, value) in enumerate(champs_base):
            label = ctk.CTkLabel(self, text=label_text + ":", anchor="w", font=("Arial", 13))
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            entry = ctk.CTkEntry(self, width=300)
            entry.insert(0, str(value))
            entry.configure(state="readonly")
            entry.grid(row=i, column=1, padx=10, pady=5)

        # Si le compte est de type courant, on ajoute les champs supplémentaires
        if compte_data[9] == "courant":
            courant_info = self.recuperer_courant_details(compte_data[0])

            if courant_info:
                labels_courant = [
                    ("Numéro de compte", courant_info[0]),
                    ("Pourcentage de découvert", courant_info[1]),
                    ("Taux d’intérêt", courant_info[2]),
                    ("Découvert utilisé", courant_info[3]),
                    ("Dette", courant_info[4]),
                ]
                base_index = len(champs_base)
                for j, (libelle, val) in enumerate(labels_courant):
                    label = ctk.CTkLabel(self, text=libelle + ":", anchor="w", font=("Arial", 13))
                    label.grid(row=base_index + j, column=0, padx=10, pady=5, sticky="w")

                    entry = ctk.CTkEntry(self, width=300)
                    entry.insert(0, str(val))
                    entry.configure(state="readonly")
                    entry.grid(row=base_index + j, column=1, padx=10, pady=5)

    def recuperer_courant_details(self, account_num):
        conn = sqlite3.connect("banque.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courant_details WHERE account_num = ?", (account_num,))
        result = cursor.fetchone()
        conn.close()
        return result

