import datetime
import pymysql


class Book:
    def __init__(self, title, author, pub_year, publisher, genre, isbn, patron_id=None, on_hold=False,
                 hold_end=None, checkout_date=None, due_date=None):

        self._title = str(title)
        self._author = str(author)
        self._pub_year = int(pub_year)
        self._publisher = str(publisher)
        self._genre = str(genre)
        self._isbn = int(isbn)
        self._patron_id = str(patron_id) if patron_id else None
        self._checkout_date = checkout_date
        self._due_date = due_date
        self._on_hold = on_hold
        self._hold_end = hold_end

    def get_title(self):
        return self._title

    def title(self, title):
        self._title = str(title)

    def get_author(self):
        return self._author

    def author(self, author):
        self._author = str(author)

    def get_pub_year(self):
        return self._pub_year

    def pub_year(self, pub_year):
        self._pub_year = int(pub_year)

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

    def get_patron_id(self):
        return self._patron_id

    def patron_id(self, patron_id):
        self._patron_id = str(patron_id)

    def get_checkout_date(self):
        return self._checkout_date

    def checkout_date(self, checkout_date):
        self._checkout_date = checkout_date

    def get_due_date(self):
        return self._due_date

    def due_date(self, due_date):
        self._due_date = due_date


    def get_hold_end(self):
        return self._hold_end

    def hold_end(self, hold_end):
        self._hold_end = hold_end

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

    def calculate_hold_expiry(self):
        if self._hold_end and datetime.date.today() > self._hold_end:
            self.on_hold(False)

    def check_out(self):
        self._checkout_date = datetime.date.today()
        self._due_date = self._checkout_date + datetime.timedelta(days=7)
        self._fee = False
        self._fee_amount = 0.0
        self._on_hold = False
        self.update_table()

    def check_in(self):
        self._checkout_date = None
        self._due_date = None
        self._fee = False
        self._fee_amount = 0.0
        self._on_hold = False
        self._hold_end = None
        self._patron_id = None
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
                    patron_id = %s,
                    checkout_date = %s,
                    due_date = %s,
                    fee = %s,
                    fee_amount = %s,
                    on_hold = %s,
                    hold_end = %s
                WHERE isbn = %s
                """

                cursor.execute(update_query, (
                    self._patron_id,
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

    def __str__(self):
        return f"Book(title={self.get_title()}, author={self.get_author()}," \
               f" date_published={self.get_pub_year()}, " \
               f"publisher={self.get_publisher()}, genre={self.get_genre()}, ISBN={self.get_isbn()}, " \
               f"patron_id={self.get_patron_id()}, checkout_date={self.get_checkout_date()}, " \
               f"due_date={self.get_due_date()}, " \
               f"on_hold={self.get_on_hold()})"
