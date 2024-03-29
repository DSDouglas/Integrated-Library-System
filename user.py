class User:
    def __init__(self, firstname, last_name, email, user_id, password):
        self._firstname = str(firstname)
        self._lastname = str(last_name)
        self._email = str(email)
        self._user_id = str(user_id)
        self._password = str(password)

    def get_firstname(self):
        return self._firstname

    def firstname(self, first_name):
        self._firstname = str(first_name)

    def get_lastname(self):
        return self._lastname

    def last_name(self, last_name):
        self._lastname = str(last_name)

    def get_email(self):
        return self._email

    def email(self, email):
        self._email = str(email)

    def get_user_id(self):
        return self._user_id

    def user_id(self, user_id):
        self._user_id = user_id

    def get_password(self):
        return self._password

    def password(self, password):
        self._password = password

    def __str__(self):
        return f"User(first_name={self.get_firstname}, last_name={self.get_lastname}, email={self.get_email}, " \
               f"user_id={self.get_user_id}, password={self.get_password})"
