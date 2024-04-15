from user import User


class Librarian(User):
    def __init__(self, firstname, lastname, email, user_id, password):
        super().__init__(firstname, lastname, email, user_id, password)

    def __str__(self):
        return f"Librarian(first_name={self.get_firstname()}, last_name={self.get_lastname()}, " \
               f"email={self.get_email()}, user_id={self.get_user_id()}, password={self.get_password()})"
