import datetime
import pymysql


class Book:
    def __init__(self, title, author, pub_year, publisher, genre, isbn):
        self._title = str(title)
        self._author = str(author)
        self._pub_year = int(pub_year)
        self._publisher = str(publisher)
        self._genre = str(genre)
        self._isbn = int(isbn)
        self._user_id = ""
        self._checkout_date = None
        self._due_date = None
        self._fee = False
        self._fee_amount = 0.0
        self._on_hold = False
        self._hold_end = None

    def get_title(self):
        return self._title

    def title(self, title):
        self._title = str(title)

    def get_author(self):
        return self._author

    def author(self, author):
        self._author = str(author)

    def get_put_year(self):
        return self._pub_year

    def pub_year(self, pub_year):
        self._pub_year= int(pub_year)

    def get_publisher(self):
        return self._publisher

    def publisher(self, publisher):
        self._publisher = str(publisher)

    def get_genre(self):
        return self._genre

    def genre(self, genre):
        self._genre = str(genre)

    def get_isbn(self):
        return self._isbn

    def isbn(self, isbn):
        self._isbn = int(isbn)

    def get_user_id(self):
        return self._user_id

    def user_id(self, user_id):
        self._user_id = str(user_id)
        self.update_table()

    def get_checkout_date(self):
        return self._checkout_date

    def checkout_date(self, checkout_date):
        self._checkout_date = checkout_date
        self.update_table()

    def get_due_date(self):
        return self._due_date

    def due_date(self, due_date):
        self._due_date = due_date
        self.update_table()

    def get_fee(self):
        return self._fee

    def fee(self, fee):
        self._fee = fee
        self.update_table()

    def get_fee_amount(self):
        return self._fee_amount

    def fee_amount(self, fee_amount):
        self._fee_amount = fee_amount
        self.update_table()

    def get_hold_end(self):
        return self._hold_end

    def hold_end(self, hold_end):
        self._hold_end = hold_end
        self.update_table()

    def get_on_hold(self):
        return self._on_hold

    def on_hold(self, on_hold):
        if on_hold:
            # Set hold_end to 3 days from today
            hold_end_date = datetime.date.today() + datetime.timedelta(days=3)
            self.hold_end(hold_end_date)
        else:
            # Clear hold_end when on_hold is set to False
            self.hold_end(None)
        self._on_hold = on_hold
        self.update_table()

    def calculate_hold_expiry(self):
        if self._hold_end and datetime.date.today() > self._hold_end:
            self.on_hold(False)

    def check_out(self):
        self._checkout_date = datetime.date.today()
        self._due_date = self._checkout_date + datetime.timedelta(days=7)
        self._fee = False
        self._fee_amount = 0.0
        self.update_table()

    def update_table(self):
        try:
            # Connect to the database
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='Noelle0718',
                database='librarysystem'
            )

            with connection.cursor() as cursor:
                # Update the Book entry in the database
                update_query = """
                UPDATE Book
                SET
                    user_id = %s,
                    checkout_date = %s,
                    due_date = %s,
                    fee = %s,
                    fee_amount = %s,
                    on_hold = %s,
                    hold_end = %s
                WHERE isbn = %s
                """

                cursor.execute(update_query, (
                    self._user_id,
                    self._checkout_date,
                    self._due_date,
                    self._fee,
                    self._fee_amount,
                    self._on_hold,
                    self._hold_end,
                    self._isbn
                ))

            # Commit the changes and close the connection
            connection.commit()
            connection.close()

        except pymysql.MySQLError as error:
            print(f"Failed to connect to the database: {error}")

    def calculate_fee(self):
        if self._due_date and datetime.date.today() > self._due_date:
            days_overdue = (datetime.date.today() - self._due_date).days
            self._fee_amount = days_overdue * 0.5  # 50 cents per day overdue
            self._fee = True
        else:
            self._fee_amount = 0.0
            self._fee = False
        self.update_table()

    def __str__(self):
        return f"Book(title={self.get_title()}, author={self.get_author()}," \
               f" date_published={self.get_put_year()}, " \
               f"publisher={self.get_publisher()}, genre={self.get_genre()}, ISBN={self.get_isbn()}, " \
               f"user_id={self.get_user_id()}, checkout_date={self.get_checkout_date()}, " \
               f"due_date={self.get_due_date()}, " \
               f"fee={self.get_fee()}, fee_amount={self.get_fee_amount()}, on_hold={self.get_on_hold()})"
