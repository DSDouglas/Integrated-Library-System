from user import User


class Librarian(User):
    def __init__(self, first_name, last_name, email, user_id, password):
        super().__init__(first_name, last_name, email, user_id, password)

    def __str__(self):
        return f"Librarian(first_name={self.get_first_name()}, last_name={self.get_last_name()}, " \
               f"email={self.get_email()}, user_id={self.get_user_id()}, password={self.get_password()})"
