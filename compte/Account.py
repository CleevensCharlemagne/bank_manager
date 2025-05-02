from abc import ABC, abstractmethod
from datetime import date
from client.Client import Client

class Account(ABC):
    def __init__(self, name: str, num: str, balance: float, owner: Client):
        if not isinstance(owner, Client):
            raise TypeError("Owner must be an instance of the Client class.")

        self._accountName = name
        self._accountNum = num
        self._balance = balance
        self._owner = owner
        self._status = '1'  # '1' for active, '0' for closed
        self._creationDate = date.today()
        self._closeDate = None

    # Getter and Setter for accountName
    @property
    def accountName(self):
        return self._accountName

    @accountName.setter
    def accountName(self, value: str):
        self._accountName = value

    # Getter and Setter for accountNum
    @property
    def accountNum(self):
        return self._accountNum

    @accountNum.setter
    def accountNum(self, value: str):
        self._accountNum = value

    # Getter and Setter for balance
    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value: float):
        if value >= 0:
            self._balance = value
        else:
            raise ValueError("Balance cannot be negative!")

    # Getter and Setter for status
    @property
    def status(self):
        return self._status

    # Getter for creationDate (read-only)
    @property
    def creationDate(self):
        return self._creationDate

    # Getter and Setter for closeDate
    @property
    def closeDate(self):
        return self._closeDate

    def deposit(self, amount: float):
        """Deposit funds into the account."""
        if amount >= 10:
            self._balance += amount
            return f"Deposited ($ {amount}). New balance: ($ {self._balance})"
        else:
            return "Insufficient amount for deposit! Minimum deposit: $ 10"

    @abstractmethod
    def withdraw(self, amount: float):
        """Abstract method for withdrawing funds."""
        pass

    def closeAccount(self):
        """Close the account."""
        if self._status == "1":
            self._status = '0'
            self._closeDate = date.today()
            self._balance = 0.0  # Balance is reset when the account is closed
            return f"Account closed. Final balance: ($ {self._balance})"

    def openAccount(self):
        """Reopen a closed account."""
        if self._status == "0":
            self._status = "1"
            self._closeDate = None
            return "Account reopened."

