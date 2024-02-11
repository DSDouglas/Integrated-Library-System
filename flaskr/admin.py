from user import User


class Admin(User):
    def __init__(self, name, user_id, password, checkout_limit=4):
        super().__init__(name, user_id, password)

        self._checkout_limit = checkout_limit

    def get_checkout_limit(self):
        return self._checkout_limit

    def checkout_limit(self, checkout_limit):
        self._checkout_limit = int(checkout_limit)

    def __str__(self):
        return f"Admin(name={self.name}, user_id={self.user_id}, password={self.password}," \
               f"checkout_limit={self.checkout_limit}) "
