import uuid
from datetime import date

class Client:
    def __init__(self, last_name, first_name, tax_id, address, birth_date, email, phone):
        self._last_name = last_name
        self._first_name = first_name
        self._tax_id = tax_id
        self._address = address
        self._birth_date = birth_date  # datetime.date or 'YYYY-MM-DD'
        self._email = email
        self._phone = phone
        self._status = '1'  # '1' for active, '0' for inactive
        self._registration_date = date.today()
        self._client_id = self._generate_client_id(tax_id)

    def _generate_client_id(self, tax_id):
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, tax_id))

    @property
    def client_id(self):
        return self._client_id

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @property
    def tax_id(self):
        return self._tax_id

    @tax_id.setter
    def tax_id(self, value):
        self._tax_id = value
        # Update client_id if tax_id changes
        self._client_id = self._generate_client_id(value)

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        self._birth_date = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def registration_date(self):
        return self._registration_date
