from user import User
from data_loader import DataMover


class Admin(User):
    def __init__(self, name, user_id, password, checkout_limit=4):
        super().__init__(name, user_id, password)

        self._checkout_limit = checkout_limit
        self.data_mover = DataMover()

    def create_patron(self):
        self.data_mover.create_patron()

    def check_out_book(self):
        self.data_mover.check_out_book()

    def check_in_book(self):
        self.data_mover.check_in_book()

    def get_checkout_limit(self):
        return self._checkout_limit

    def checkout_limit(self, checkout_limit):
        self._checkout_limit = int(checkout_limit)

    def __str__(self):
        return f"Admin(name={self.name}, user_id={self.user_id}, password={self.password}," \
               f"checkout_limit={self.checkout_limit}) "
