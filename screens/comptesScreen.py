import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

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
        AjouterCompteWindow(self)

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
        self.geometry("700x650")
        self.compte_data = compte_data
        self.entrees = []

        # Container scrollable
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(container, orientation="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        content_frame = ctk.CTkFrame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        account_num = compte_data[0]
        owners = self.get_account_owners(account_num)
        if owners:
            owner_names = ", ".join([f"{prenom} {nom}" for prenom, nom in owners])
            titre_texte = f"Compte enregistré au nom de : {owner_names}"
        else:
            titre_texte = "Compte enregistré au nom de : (inconnu)"

        titre_label = ctk.CTkLabel(self, text=titre_texte, font=ctk.CTkFont(size=18, weight="bold"))
        titre_label.pack(pady=20)

        # Données principales
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

        self.editable_entries = []  # list of entries that should be editable

        for i, (label_text, value) in enumerate(champs_base):
            row_frame = ctk.CTkFrame(content_frame, fg_color="transparent")  # fond transparent
            row_frame.pack(pady=5, anchor="center")  # centré horizontalement

            label = ctk.CTkLabel(row_frame, text=label_text + " :", width=200, anchor="e", font=("Roboto Medium", 13, "bold"))
            label.pack(side="left", padx=10)

            entry = ctk.CTkEntry(row_frame, width=300)
            entry.insert(0, str(value))
            entry.configure(state="readonly")
            entry.pack(side="left")
            self.entrees.append(entry)

        # Champs compte courant
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
                for (label_text, value) in labels_courant:
                    row_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                    row_frame.pack(pady=5, anchor="center")

                    label = ctk.CTkLabel(row_frame, text=label_text + " :", width=200, anchor="e", font=("Roboto Medium", 13, "bold"))
                    label.pack(side="left", padx=10)

                    entry = ctk.CTkEntry(row_frame, width=300)
                    entry.insert(0, str(value))
                    entry.configure(state="readonly")
                    entry.pack(side="left")
                    self.entrees.append(entry)

        # Scroll molette
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # --- BOUTONS EN BAS ---
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        self.btn_fermer = ctk.CTkButton(button_frame, text="Fermer", command=self.fermer_compte, font=("Roboto Medium", 13, "bold"))
        self.btn_fermer.pack(side="left", padx=10)

        self.btn_quitter = ctk.CTkButton(button_frame, text="Quitter", command=self.destroy, font=("Roboto Medium", 13, "bold"))
        self.btn_quitter.pack(side="left", padx=10)

    def fermer_compte(self):
        # Action personnalisée pour "Fermer" (peut-être désactiver le compte)
        print("Compte fermé (à implémenter)")

    def recuperer_courant_details(self, account_num):
        conn = sqlite3.connect("banque.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courant_details WHERE account_num = ?", (account_num,))
        result = cursor.fetchone()
        conn.close()
        return result

    def get_account_owners(self, account_num):
        conn = sqlite3.connect("banque.db")
        cursor = conn.cursor()

        # Récupérer le propriétaire principal
        cursor.execute("""
            SELECT c.first_name, c.last_name
            FROM accounts a
            JOIN clients c ON a.owner_id = c.client_id
            WHERE a.account_num = ?
        """, (account_num,))
        owners = cursor.fetchall()

        # Récupérer les co-titulaires supplémentaires
        cursor.execute("""
            SELECT c.first_name, c.last_name
            FROM account_owners ao
            JOIN clients c ON ao.client_id = c.client_id
            WHERE ao.account_num = ? AND c.client_id != (
                SELECT owner_id FROM accounts WHERE account_num = ?
            )
        """, (account_num, account_num))
        co_owners = cursor.fetchall()

        conn.close()
        return owners + co_owners

class AjouterCompteWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ajouter un compte")
        self.geometry("500x600")
        self.entries = {}
        self.type_compte = tk.StringVar(value="courant")

        ctk.CTkLabel(self, text="Type de compte :", font=("Roboto", 14)).pack(pady=10)
        type_menu = ctk.CTkOptionMenu(self, values=["courant", "epargne"], variable=self.type_compte, command=self.afficher_champs_specifiques)
        type_menu.pack()

        self.frame_formulaire = ctk.CTkFrame(self)
        self.frame_formulaire.pack(pady=20, padx=20, fill="both", expand=True)

        self.afficher_formulaire_base()
        self.afficher_champs_specifiques("courant")

        bouton_ajouter = ctk.CTkButton(self, text="Créer le compte", command=self.ajouter_compte)
        bouton_ajouter.pack(pady=10)

    def afficher_formulaire_base(self):
        labels = ["Numéro de compte", "Nom du compte", "Solde initial"]
        for label in labels:
            frame = ctk.CTkFrame(self.frame_formulaire)
            frame.pack(pady=5)
            ctk.CTkLabel(frame, text=label + " :", width=150, anchor="e").pack(side="left", padx=10)
            entry = ctk.CTkEntry(frame, width=250)
            entry.pack(side="left")
            self.entries[label] = entry

        # d'abord charger les clients
        self.clients_disponibles = self.charger_clients()
        client_noms = ["(Aucun)"] + [nom for _, nom in self.clients_disponibles]

        # Variables liées aux menus déroulants
        self.owner_var = tk.StringVar()
        self.copro1_var = tk.StringVar()
        self.copro2_var = tk.StringVar()

        self.copro1_var.set("Aucun")
        self.copro2_var.set("Aucun")

        # Menu propriétaire principal
        frame_owner = ctk.CTkFrame(self.frame_formulaire)
        frame_owner.pack(pady=5)
        ctk.CTkLabel(frame_owner, text="Propriétaire principal :", width=150, anchor="e").pack(side="left", padx=10)
        self.owner_menu = ctk.CTkOptionMenu(frame_owner, variable=self.owner_var, values=client_noms,
                                            command=self.verifier_unique_client_selection)
        self.owner_menu.pack(side="left")

        # Menu copropriétaire 1
        frame_copro1 = ctk.CTkFrame(self.frame_formulaire)
        frame_copro1.pack(pady=5)
        ctk.CTkLabel(frame_copro1, text="Copropriétaire 1 :", width=150, anchor="e").pack(side="left", padx=10)
        self.copro1_menu = ctk.CTkOptionMenu(frame_copro1, variable=self.copro1_var, values=client_noms,
                                             command=self.verifier_unique_client_selection)
        self.copro1_menu.pack(side="left")

        # Menu copropriétaire 2
        frame_copro2 = ctk.CTkFrame(self.frame_formulaire)
        frame_copro2.pack(pady=5)
        ctk.CTkLabel(frame_copro2, text="Copropriétaire 2 :", width=150, anchor="e").pack(side="left", padx=10)
        self.copro2_menu = ctk.CTkOptionMenu(frame_copro2, variable=self.copro2_var, values=client_noms,
                                             command=self.verifier_unique_client_selection)
        self.copro2_menu.pack(side="left")

    def afficher_champs_specifiques(self, type_compte):
        if hasattr(self, 'frame_specifique'):
            self.frame_specifique.destroy()
        self.frame_specifique = ctk.CTkFrame(self.frame_formulaire)
        self.frame_specifique.pack(pady=10)

        self.entries["Spécifique"] = {}

        if type_compte == "courant":
            for label in ["Pourcentage de découvert", "Taux d’intérêt", "Découvert utilisé", "Dette"]:
                frame = ctk.CTkFrame(self.frame_specifique)
                frame.pack(pady=5)
                ctk.CTkLabel(frame, text=label + " :", width=150, anchor="e").pack(side="left", padx=10)
                entry = ctk.CTkEntry(frame, width=250)
                entry.pack(side="left")
                self.entries["Spécifique"][label] = entry

            # Activer les menus pour les copropriétaires
            self.copro1_menu.configure(state="normal")
            self.copro2_menu.configure(state="normal")
        else:
            # Désactiver les menus pour les copropriétaires
            self.copro2_menu.configure(state="disabled")

    def charger_clients(self):
        conn = sqlite3.connect("banque.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT client_id, first_name, last_name FROM clients")
            # Création de la liste avec format : "id - Prénom Nom"
            return [(row[0], f"{row[0]} - {row[1]} {row[2]}") for row in cursor.fetchall()]
        except sqlite3.Error as e:
            tk.messagebox.showerror("Erreur", f"Erreur lors du chargement des clients : {e}")
            return []
        finally:
            conn.close()

    def get_id_client_by_nom(self, nom_affiche):
        if nom_affiche == "Aucun":
            return None
        for id_client, nom_formate in self.clients_disponibles:
            if nom_formate == nom_affiche:
                return id_client
        return None

    def verifier_unique_client_selection(self, value=None):
        # Récupérer les clients sélectionnés dans les menus
        id_principal = self.get_id_client_by_nom(self.owner_var.get())
        id_copro1 = self.get_id_client_by_nom(self.copro1_var.get())
        id_copro2 = self.get_id_client_by_nom(self.copro2_var.get())

        # Vérification : si le propriétaire principal est le même que l'un des copropriétaires
        if (id_copro1 == id_principal or id_copro2 == id_principal):
            messagebox.showerror("Erreur",
                                 "Un client ne peut pas être à la fois propriétaire principal et copropriétaire.")
            return False

        # Vérifier que copropriétaire 1 et copropriétaire 2 ne sont pas les mêmes
        if (id_copro1 == id_copro2) and (id_copro1 != None and id_copro2 != None):
            messagebox.showerror("Erreur", "Copropriétaire 1 et copropriétaire 2 ne peuvent pas être les mêmes.")
            return False

        return True

    def ajouter_compte(self):
        if not self.verifier_unique_client_selection():
            return

        # Récupération des champs de saisie
        numero = self.entries["Numéro de compte"].get().strip()
        nom = self.entries["Nom du compte"].get().strip()
        solde = self.entries["Solde initial"].get().strip()

        # Vérification de la validité des champs
        if not numero or not nom or not solde:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        try:
            solde = float(solde)
        except ValueError:
            messagebox.showerror("Erreur", "Le solde initial doit être un nombre.")
            return

        # Récupérer les ID des clients sélectionnés
        id_principal = self.get_id_client_by_nom(self.owner_var.get())
        id_copro1 = self.get_id_client_by_nom(self.copro1_var.get())
        id_copro2 = self.get_id_client_by_nom(self.copro2_var.get())

        if id_principal is None:
            messagebox.showerror("Erreur", "Propriétaire principal invalide.")
            return

        # Connexion à la base de données
        conn = sqlite3.connect("banque.db")
        cursor = conn.cursor()

        try:
            # Insertion dans la table comptes
            cursor.execute(
                "INSERT INTO accounts (account_num, account_name balance, owner_id) VALUES (?, ?, ?, ?)",
                (numero, nom, solde, id_principal)
            )

            # Insertion des copropriétaires si sélectionnés
            for id_copro in [id_copro1, id_copro2]:
                if id_copro and id_copro != id_principal:
                    cursor.execute(
                        "INSERT INTO account_owners (account_num, client_id) VALUES (?, ?)",
                        (numero, id_copro)
                    )

            conn.commit()
            messagebox.showinfo("Succès", "Compte ajouté avec succès.")
            self.destroy()
            self.master_app.actualiser_tableau()  # Si nécessaire pour rafraîchir la vue principale

        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur", "Le numéro de compte existe déjà.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")
        finally:
            conn.close()



