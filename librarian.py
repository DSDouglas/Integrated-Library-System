from user import User
from data_loader import DataMover


class Librarian(User):
    def __init__(self, name, user_id, password):
        super().__init__(name, user_id, password)
        self.data_mover = DataMover()

    def create_patron(self, name, user_id, password):
        self.data_mover.create_patron(name, user_id, password)

    def check_out_book(self, isbn):
        self.data_mover.check_out_book(isbn)

    def check_in_book(self, isbn):
        self.data_mover.check_in_book(isbn)

    def __str__(self):
        return f"Librarian(name={self.get_name()}, user_id={self.get_user_id()}, password={self.get_password()})"
