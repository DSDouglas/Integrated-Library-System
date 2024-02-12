class User:
    def __init__(self, name, user_id, password):
        self._name = str(name)
        self._user_id = str(user_id)
        self._password = str(password)

    def get_name(self):
        return self._name

    def name(self, name):
        self._name = str(name)

    def get_user_id(self):
        return self._user_id

    def user_id(self, user_id):
        self._user_id = user_id

    def get_password(self):
        return self._password

    def password(self, password):
        self._password = password

    def __str__(self):
        return f"User(name={self._name}, user_id={self._user_id}, password={self._password})"
