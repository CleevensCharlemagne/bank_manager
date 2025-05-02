import customtkinter as ctk
from screens.clientsScreen import ClientsFrame
from screens.comptesScreen import CompteFrame  # 👈 Assure-toi que ce chemin est correct
from PIL import Image
from Icon import *

class EcranPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tableau de bord")
        self.geometry("900x700")

        # Conteneur principal
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # Initialisation des frames
        self.frame_menu = FrameMenuPrincipal(self.container, self)
        self.frame_menu.pack(fill="both", expand=True)

    def revenir_accueil(self):
        """Retourner à l'écran principal."""
        self.clear_frames()
        self.frame_menu = FrameMenuPrincipal(self.container, self)
        self.frame_menu.pack(fill="both", expand=True)
        self.changer_titre("Tableau de bord")  # Changer le titre lorsque tu reviens à l'écran principal

    def afficher_clients(self):
        self.clear_frames()
        self.frame_clients = ClientsFrame(self.container, self)  # Passer self (EcranPrincipal) ici
        self.frame_clients.pack(fill="both", expand=True)
        self.changer_titre("Clients")

    def afficher_comptes(self):
        self.clear_frames()
        self.frame_comptes = CompteFrame(self.container, self)  # Passer self comme controller
        self.frame_comptes.pack(fill="both", expand=True)
        self.changer_titre("Comptes")

    def clear_frames(self):
        for widget in self.container.winfo_children():
            widget.pack_forget()

    def quitter(self):
        self.destroy()

    def changer_titre(self, nouveau_titre: str):
        self.title(nouveau_titre)  # Modifie le titre de la fenêtre




class FrameMenuPrincipal(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.title = ctk.CTkLabel(self, text="Tableau de bord", font=("Segoe UI", 20, "bold"))
        self.title.pack(pady=(70, 50))

        self.btn_clients = ctk.CTkButton(
            self, text="Clients", command=self.controller.afficher_clients, width=300, height=40, font=("Arial", 16)
        )
        self.btn_clients.pack(pady=10)

        self.btn_comptes = ctk.CTkButton(
            self, text="Comptes", command=self.controller.afficher_comptes, width=300, height=40, font=("Arial", 16)
        )
        self.btn_comptes.pack(pady=10)

        self.btn_quitter = ctk.CTkButton(
            self, text="Quitter", fg_color="#959595", hover_color="#737373",
            command=self.controller.quitter, width=300, height=40, font=("Arial", 16)
        )
        self.btn_quitter.pack(pady=(50, 70))


