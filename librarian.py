import csv
import pymysql

from patron import Patron
from user import User
from data_loader import DataMover


class Librarian(User):
    def __init__(self, name, user_id, password):
        super().__init__(name, user_id, password)
        self.data_mover = DataMover()

    def create_patron(self):
        self.data_mover.create_patron()

    def check_out_book(self):
        self.data_mover.check_out_book()

    def check_in_book(self):
        self.data_mover.check_in_book()

    def __str__(self):
        return f"Librarian(name={self.get_name()}, user_id={self.get_user_id()}, password={self.get_password()})"
