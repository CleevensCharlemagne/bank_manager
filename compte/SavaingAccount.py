from compte.Account import Account

class CompteEpargne(Account):

    def withdraw(self, amount: float):
        """Withdraw from the savings account."""
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            return f"Successfully withdrew ${amount}. New balance: ${self.balance:.2f}"
        elif amount <= 0:
            return "Amount to withdraw must be positive."
        else:
            return "Insufficient funds for withdrawal."

    def __str__(self):
        if self.status == "1":
            return f"Compte Epargne\n" \
                   f"Nom de compte: {self.accountName}\n" \
                   f"Numéro de compte: {self.accountNum}\n" \
                   f"Solde: $ {self.balance:.2f}"
        else:
            return f"Compte Epargne\n" \
                   f"Nom de compte: {self.accountName}\n" \
                   f"Numéro de compte: {self.accountNum}\n" \
                   f"!!! Ce compte est fermé !!!"
