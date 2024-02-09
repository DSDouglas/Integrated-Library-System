from user import User


class Patron(User):
    def __init__(self, name, user_id, password):
        super().__init__(name, user_id, password)

    def __str__(self):
        return f"Patron(name={self.name}, user_id={self.user_id}, password={self.password})"
