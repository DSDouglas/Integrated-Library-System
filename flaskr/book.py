class Book:
    def __init__(self, title, author, date_published, publisher, genre, isbn):
        self._title = str(title)
        self._author = str(author)
        self._date_published = int(date_published)
        self._publisher = str(publisher)
        self._genre = str(genre)
        self._isbn = int(isbn)
        self._checkout = False  # Initialize as not checked out
        self.onhold = False  # Initialized as False

    def get_title(self):
        return self._title

    def title(self, title):
        self._title = str(title)

    def get_author(self):
        return self._author

    def author(self, author):
        self._author = str(author)

    def get_date_published(self):
        return self._date_published

    def date_published(self, date_published):
        self._date_published = int(date_published)

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

    def get_checkout(self):
        return self._checkout

    def check_out(self):
        self._checkout = False

    def get_onhold(self):
        return self.onhold

    def onhold(self, onhold):
        self.onhold = onhold

    def __str__(self):
        return f"Book(title={self._title}, author={self._author}, date_published={self._date_published}, " \
               f"publisher={self._publisher}, genre={self._genre}, ISBN={self._isbn}, " \
               f"checkout={self._checkout}, checkin={self.get_onhold})"
