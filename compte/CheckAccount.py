from compte.Account import Account
from client.Client import Client

class CompteCourant(Account):
    def __init__(self, name: str, num: str, balance: float, owner: Client, overdraft_percentage: float,
                 interest_rate: float):
        """Initialise un compte courant avec un pourcentage de découvert autorisé et un taux d'intérêt pour le découvert."""
        super().__init__(name, num, balance, owner)
        self._overdraft_percentage = overdraft_percentage  # Pourcentage du découvert autorisé
        self._interest_rate = interest_rate  # Taux d'intérêt appliqué au découvert
        self._overdraft_used = 0  # Montant utilisé du découvert
        self._debt = 0  # Dette due à la banque (calculée sur le montant du découvert utilisé)

    # Getter et Setter pour overdraft_percentage
    @property
    def overdraft_percentage(self):
        return self._overdraft_percentage

    @overdraft_percentage.setter
    def overdraft_percentage(self, value: float):
        if value >= 0:
            self._overdraft_percentage = value
        else:
            print("Le pourcentage de découvert ne peut pas être négatif.")

    # Getter et Setter pour interest_rate
    @property
    def interest_rate(self):
        return self._interest_rate

    @interest_rate.setter
    def interest_rate(self, value: float):
        if value >= 0:
            self._interest_rate = value
        else:
            print("Le taux d'intérêt ne peut pas être négatif.")

    # Getter et Setter pour overdraft_used (découvert utilisé)
    @property
    def overdraft_used(self):
        return self._overdraft_used

    @overdraft_used.setter
    def overdraft_used(self, value: float):
        if value >= 0:
            self._overdraft_used = value
        else:
            print("Le montant du découvert utilisé ne peut pas être négatif.")

    # Getter et Setter pour debt (la dette due à la banque)
    @property
    def debt(self):
        return self._debt

    def withdraw(self, amount: float):
        """Retirer des fonds du compte courant en tenant compte du découvert autorisé et de la dette due à la banque."""
        if amount > 0:
            overdraft_limit = self.balance * (self._overdraft_percentage / 100)
            if self.balance + overdraft_limit >= amount:
                self.balance -= amount
                if self.balance < 0:  # Si le solde devient négatif, on utilise le découvert
                    self._overdraft_used = abs(self.balance)
                    self._debt = self._overdraft_used * (
                                self._interest_rate / 100)  # Calcul de la dette à la banque
                return f"Retrait de ${amount}. Nouveau solde: ${self.balance:.2f}. Dette à la banque: ${self._debt:.2f}"
            else:
                return f"Fonds insuffisants. Solde et découvert autorisé: ${self.balance + overdraft_limit:.2f}"
        else:
            return "Le montant de retrait doit être positif."

    def deposit(self, amount: float):
        """Dépôt sur le compte. Si le compte a utilisé son découvert, appliquer les intérêts et ajuster la dette."""
        if amount > 0:
            self.balance += amount
            if self._overdraft_used > 0:  # Si le découvert a été utilisé
                if amount >= self._debt:  # Si le dépôt est suffisant pour couvrir la dette
                    self.balance -= (amount - self._debt)  # Réduire le solde du compte en conséquence
                    self._debt = 0  # Effacer la dette
                    return f"Dépôt de ${amount}. Nouveau solde: ${self.balance:.2f}. Dette payée."
                else:  # Si le dépôt est inférieur à la dette
                    self._debt -= amount  # Réduire la dette avec le dépôt effectué
                    return f"Dépôt de ${amount}. Nouveau solde: ${self.balance:.2f}. Dette restante: ${self._debt:.2f}"

            return f"Dépôt de ${amount}. Nouveau solde: ${self.balance:.2f}"
        else:
            return "Le montant de dépôt doit être positif."

    def __str__(self):
        """Retourne une chaîne de caractères pour décrire le compte courant."""
        if self.status == "1":
            overdraft_limit = self.balance * (self._overdraft_percentage / 100)
            return f"Compte Courant\n" \
                   f"Nom de compte: {self.accountName}\n" \
                   f"Numéro de compte: {self.accountNum}\n" \
                   f"Solde: $ {self.balance:.2f}\n" \
                   f"Découvert autorisé: $ {overdraft_limit:.2f} ({self._overdraft_percentage}% du solde)\n" \
                   f"Dette due à la banque: $ {self._debt:.2f}"
        else:
            return f"Compte Courant\n" \
                   f"Nom de compte: {self.accountName}\n" \
                   f"Numéro de compte: {self.accountNum}\n" \
                   f"!!! Ce compte est fermé !!!"
