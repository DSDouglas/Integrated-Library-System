import datetime
import pymysql
import csv
from patron import Patron
from admin import Admin
from librarian import Librarian
import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


with open(os.path.join(BASE_DIR, "config.json")) as config_file:
    config = json.load(config_file)


class DataMover:
    """
    DataMover class for handling database operations.

    Attributes:
    - connection: Connection object for interacting with the MySQL database.
    """

    def __init__(self):
        """Initialize DataMover with a None connection."""
        self.connection = None

    def connect_to_database(self):
        """
        Establish a connection to the database.

        Sets the 'connection' attribute to the established connection.
        """
        try:
            DATABASES = config.get("DATABASES", {})
            self.connection = pymysql.connect(
                host=DATABASES["default"]["HOST"],
                user=DATABASES["default"]["USER"],
                password=DATABASES["default"]["PASSWORD"],
                database=DATABASES["default"]["NAME"],
            )
        except pymysql.MySQLError as error:
            print(f"Failed to connect to the database: {error}")

    def create_tables(self, cursor):
        """
        Create database tables if they do not exist.

        Args:
        - cursor: Cursor object for executing SQL queries on the database.
        """
        # SQL statements for creating tables
        table_queries = [
            """CREATE TABLE IF NOT EXISTS Admin (
                admin_id INT AUTO_INCREMENT PRIMARY KEY,
                firstname VARCHAR(255),
                lastname VARCHAR(255),
                email VARCHAR(255),
                user_id VARCHAR(255),
                password VARCHAR(255)
            )""",
            """CREATE TABLE IF NOT EXISTS Librarian (
                librarian_id INT AUTO_INCREMENT PRIMARY KEY,
                firstname VARCHAR(255),
                lastname VARCHAR(255),
                email VARCHAR(255),
                user_id VARCHAR(255),
                password VARCHAR(255)
            )""",
            """CREATE TABLE IF NOT EXISTS Patron (
                patron_id INT AUTO_INCREMENT PRIMARY KEY,
                firstname VARCHAR(255),
                lastname VARCHAR(255),
                email VARCHAR(255),
                user_id VARCHAR(255),
                password VARCHAR(255)
            )""",
            """CREATE TABLE IF NOT EXISTS Book (
                book_id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                author VARCHAR(255),
                pub_year YEAR,
                publisher VARCHAR(255),
                genre VARCHAR(255),
                isbn BIGINT,
                patron_id INT,
                on_hold BOOLEAN,
                hold_end DATE,
                checkout_date DATE,
                due_date DATE,
                FOREIGN KEY (patron_id) REFERENCES Patron(patron_id)
            )""",
            """CREATE TABLE IF NOT EXISTS Fee (
                fee_id INT AUTO_INCREMENT PRIMARY KEY,
                book_id INT,
                fee_amount DECIMAL(10, 2),
                user_id VARCHAR(255),
                FOREIGN KEY (book_id) REFERENCES Book(book_id)
                );""",
        ]

        # Execute each table creation query
        for query in table_queries:
            cursor.execute(query)

    def insert_data(self, cursor, class_instances):
        """
        Insert data into the database tables.

        Args:
        - cursor: Cursor object for executing SQL queries on the database.
        - class_instances: List of class instances to insert into the corresponding tables.
        """
        for instance in class_instances:
            # Get the name of the class (table) of the current instance
            table_name = instance.__class__.__name__

            # Get the names of the attributes (columns) of the instance without underscores
            columns = ", ".join(
                column.lstrip("_") for column in instance.__dict__.keys()
            )

            # Convert attribute values to strings for the SQL query
            values = ", ".join(
                (
                    f"NULL"
                    if value is None
                    else f"'{value}'" if isinstance(value, str) else str(value)
                )
                for value in instance.__dict__.values()
            )

            # Construct the SQL insert query without underscores in column names
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            print("query", query)

            # Execute the insert query using the cursor
            cursor.execute(query)

    def delete_data(self, cursor, class_name, condition):
        """
        Delete data from a specific table based on a condition.

        Args:
        - cursor: Cursor object for executing SQL queries on the database.
        - class_name: Name of the table to delete data from.
        - condition: Condition to filter the data to be deleted.
        """
        query = f"DELETE FROM {class_name} WHERE {condition}"
        cursor.execute(query)

    def save_to_csv(self, class_name, instance):
        """
        Save failed connection information to a CSV file.

        Args:
        - class_name: Name of the class (table) from which the connection failed.
        - instance: Class instance containing the failed connection information.
        """
        csv_file_path = f"{class_name}_failed_connections.csv"
        with open(csv_file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([class_name] + list(instance.__dict__.values()))

    def validate_user_credentials(self, user_id, password, role):
        """
        Validate user credentials by checking the database and CSV file.

        Args:
        - user_id: User ID for authentication.
        - password: Password for authentication.
        - role: User role (Librarian, Admin, or Patron).

        Returns:
        - True if authentication is successful, False otherwise.
        """
        if not self.connection or not self.connection.open:
            self.connect_to_database()
        try:
            # Check if there is an active connection
            if self.connection:
                # Use a cursor to execute SQL queries
                with self.connection.cursor() as cursor:
                    # Query the database to find the user by user_id
                    cursor.execute(
                        f"SELECT * FROM {role} WHERE user_id = %s AND password = %s",
                        (user_id, password),
                    )
                    result = cursor.fetchone()

                # If a result is found, authentication is successful
                if result:
                    return True

        except pymysql.MySQLError as error:
            # Handle the case where the connection to the database fails
            print(f"Failed to connect to the database: {error}")
            print(error.args)

        # If not found in the database or connection failed, check the CSV file
        csv_file_path = f"{role}_failed_connections.csv"
        try:
            with open(csv_file_path, mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    # Check if the row has enough elements and the username and password match
                    if len(row) >= 6 and row[3] == user_id and row[5] == password:
                        return True
        except FileNotFoundError:
            pass  # Continue if the file doesn't exist

        # Return False if no match is found
        return False

    def create_patron(self, first_name, last_name, email, user_id, password):
        """
        Create a patron user in the database.

        Args:
        - first_name: First name of the patron.
        - last_name: Last name of the patron.
        - email: Email address of the patron.
        - user_id: User ID of the patron.
        - password: Password of the patron.
        """

        try:
            # Connect to the database and check if user_id exists
            self.connect_to_database()

            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM Patron WHERE user_id = '{user_id}'")
                result = cursor.fetchone()

            if result:
                print("User ID already exists. Please try again.")
                return

            # If user_id doesn't exist, create a new Patron instance and update the database
            new_patron = Patron(first_name, last_name, email, user_id, password)

            with self.connection.cursor() as cursor:
                self.insert_data(cursor, [new_patron])
                self.connection.commit()

            print("Patron created successfully!")

        except (pymysql.MySQLError, AttributeError) as error:
            print(f"Failed to connect to the database: {error}")

            # Check the Patron_failed_connections.csv file
            csv_file_path = "Patron_failed_connections.csv"
            try:
                with open(csv_file_path, mode="r") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) >= 3 and row[1] == user_id:
                            print(
                                "User ID already exists in the failed connections. Please try again."
                            )
                            return
            except FileNotFoundError:
                pass  # Continue if the file doesn't exist

            # If user_id not found in the failed connections, add a new row
            with open(csv_file_path, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["Patron"] + [first_name, last_name, email, user_id, password]
                )

            print("Patron created successfully! (Added to failed connections)")

    def create_librarian(self, first_name, last_name, email, user_id, password):
        """
        Create a librarian user in the database.

        Args:
        - first_name: First name of the librarian.
        - last_name: Last name of the librarian.
        - email: Email address of the librarian.
        - user_id: User ID of the librarian.
        - password: Password of the librarian.
        """
        try:
            # Connect to the database and check if user_id exists
            self.connect_to_database()

            with self.connection.cursor() as cursor:

                cursor.execute(f"SELECT * FROM Librarian WHERE user_id = '{user_id}'")
                result = cursor.fetchone()

            if result:
                print("User ID already exists. Please try again.")
                return

            # If user_id doesn't exist, create a new Librarian instance and update the database
            new_librarian = Librarian(first_name, last_name, email, user_id, password)
            with self.connection.cursor() as cursor:
                self.insert_data(cursor, [new_librarian])
                self.connection.commit()

            print("Librarian created successfully!")

        except pymysql.MySQLError as error:
            print(f"Failed to connect to the database: {error}")

            # Check the Librarian_failed_connections.csv file
            csv_file_path = "Librarian_failed_connections.csv"
            try:
                with open(csv_file_path, mode="r") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) >= 3 and row[1] == user_id:
                            print(
                                "User ID already exists in the failed connections. Please try again."
                            )
                            return
            except FileNotFoundError:
                pass  # Continue if the file doesn't exist

            # If user_id not found in the failed connections, add a new row
            with open(csv_file_path, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["Librarian"] + [first_name, last_name, email, user_id, password]
                )

            print("Librarian created successfully! (Added to failed connections)")

    def create_admin(self, first_name, last_name, email, user_id, password):
        """
        Create an admin user in the database.

        Args:
        - first_name: First name of the admin.
        - last_name: Last name of the admin.
        - email: Email address of the admin.
        - user_id: User ID of the admin.
        - password: Password of the admin.
        """
        try:
            # Connect to the database and check if user_id exists
            self.connect_to_database()

            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM Admin WHERE user_id = '{user_id}'")
                result = cursor.fetchone()

            if result:
                print("User ID already exists. Please try again.")
                return

            # If user_id doesn't exist, create a new Admin instance and update the database
            new_admin = Admin(first_name, last_name, email, user_id, password)
            with self.connection.cursor() as cursor:
                self.insert_data(cursor, [new_admin])
                self.connection.commit()

            print("Admin created successfully!")

        except pymysql.MySQLError as error:
            print(f"Failed to connect to the database: {error}")

            # Check the Admin_failed_connections.csv file
            csv_file_path = "Admin_failed_connections.csv"
            try:
                with open(csv_file_path, mode="r") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) >= 3 and row[1] == user_id:
                            print(
                                "User ID already exists in the failed connections. Please try again."
                            )
                            return
            except FileNotFoundError:
                pass  # Continue if the file doesn't exist

            # If user_id not found in the failed connections, add a new row
            with open(csv_file_path, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["Admin"] + [first_name, last_name, email, user_id, password]
                )

            print("Admin created successfully! (Added to failed connections)")

    def check_out_book(self, isbn, user_id):
        try:
            # Connect to the database
            self.connect_to_database()

            with self.connection.cursor() as cursor:
                # Get patron_id based on user_id
                cursor.execute(
                    "SELECT patron_id FROM Patron WHERE user_id = %s", (user_id,)
                )
                result = cursor.fetchone()

                if result:
                    patron_id = result[0]

                    # Call the search_user_id method to get the user's books
                    books = self.search_user_id(user_id)

                    # Check the number of books and outstanding fees
                    if len(books) >= 4:
                        print(
                            "Sorry, you have reached the checkout limit (4 books). Please return some books before "
                            "checking out more."
                        )
                    if any(book[12] for book in books):
                        print(
                            "Sorry, you have outstanding fees. Please pay your fees before checking out more books."
                        )
                    if any(
                        book[10] and datetime.date.today() > book[10] for book in books
                    ):
                        print(
                            "Sorry, you have overdue books. Please return overdue books and pay fees before checking "
                            "out new books."
                        )
                    else:
                        # Proceed with the checkout process
                        # Update the Book entry in the database
                        update_query = """
                        UPDATE Book
                        SET
                            patron_id = %s,
                            checkout_date = %s,
                            due_date = %s
                        WHERE isbn = %s
                        """

                        checkout_date = datetime.date.today()
                        due_date = checkout_date + datetime.timedelta(days=7)

                        cursor.execute(
                            update_query, (patron_id, checkout_date, due_date, isbn)
                        )

                        # Calculate and update fees
                        book = self.search_isbn(isbn)
                        if book:
                            self.calculate_fee(
                                book[0]
                            )  # Assuming search_isbn returns a single book

                        print("Book checked out successfully!")

                else:
                    print(f"User with user_id {user_id} not found.")

        except (pymysql.MySQLError, AttributeError) as error:
            print(f"Failed to connect to the database or execute the query: {error}")

        finally:
            # Commit the changes and close the database connection
            self.connection.commit()

    def check_in_book(self, isbn, user_id):
        try:
            if not self.connection:
                self.connect_to_database()

            with self.connection.cursor() as cursor:
                # Retrieve book information
                cursor.execute(
                    """
                    SELECT * FROM Book
                    WHERE isbn = %s AND patron_id = (SELECT patron_id FROM Patron WHERE user_id = %s)
                """,
                    (isbn, user_id),
                )
                book = cursor.fetchone()

                if book:
                    # Update book status and remove patron information
                    update_query = """
                    UPDATE Book
                    SET
                        patron_id = NULL,
                        on_hold = FALSE,
                        hold_end = NULL,
                        checkout_date = NULL,
                        due_date = NULL
                    WHERE isbn = %s
                    """
                    cursor.execute(update_query, (isbn,))

                    # Calculate and update fees (including removing existing fees if book is not overdue)
                    self.calculate_fee(book)

                    # Commit the changes
                    self.connection.commit()

                    print("Book checked in successfully.")
                else:
                    print("Book not found or not checked out by the specified user.")

        except (pymysql.MySQLError, AttributeError) as error:
            print(f"Failed to check in book: {error}")

        finally:

            pass

    def search_isbn(self, isbn):
        """
        Search books by ISBN in the database.

        Args:
        - isbn: The ISBN to search for.

        Returns:
        - A list of books matching the ISBN.
        """
        try:
            # Connect to the database and execute the query
            self.connect_to_database()
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM Book WHERE isbn = '{isbn}'")
                books = cursor.fetchall()

            if books:
                print("\nFound books with ISBN {}:\n".format(isbn))
                print(
                    "{:<8} | {:<25} | {:<20} | {:<15} | {}".format(
                        "Book ID", "Title", "Author", "ISBN", "Status"
                    )
                )
                print("-" * 80)

                for book in books:
                    status = "Checked Out" if book[10] else "Available"
                    print(
                        "{:<8} | {:<25} | {:<20} | {:<15} | {}".format(
                            book[0], book[1], book[2], book[6], status
                        )
                    )

                return books
            else:
                print("No books found with ISBN {}.".format(isbn))
                return []

        except pymysql.MySQLError as error:
            print("Failed to connect to the database: {}".format(error))
            return []

        finally:
            # Close the database connection
            self.close_connection()

    def search_genre(self, genre):
        """
        Search books by genre in the database.

        Args:
        - genre: The genre to search for.

        Returns:
        - A list of books matching the genre.
        """
        try:
            # Connect to the database and execute the query
            self.connect_to_database()
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM Book WHERE genre = '{genre}'")
                books = cursor.fetchall()

            if books:
                print("\nFound books with genre {}:\n".format(genre))
                print(
                    "{:<8} | {:<25} | {:<20} | {:<15} | {}".format(
                        "Book ID", "Title", "Author", "ISBN", "Status"
                    )
                )
                print("-" * 80)

                for book in books:
                    status = "Checked Out" if book[10] else "Available"
                    print(
                        "{:<8} | {:<25} | {:<20} | {:<15} | {}".format(
                            book[0], book[1], book[2], book[6], status
                        )
                    )

                return books
            else:
                print("No books found with genre {}.".format(genre))
                return []

        except pymysql.MySQLError as error:
            print("Failed to connect to the database: {}".format(error))
            return []

        finally:

            self.connection.commit()

    def calculate_fee(self, book):
        """
        Calculate and update the overdue fee for a given book.

        Args:
            book (tuple): A tuple containing book information.

        Returns:
            None
        """
        try:
            if not self.connection:
                self.connect_to_database()

            with self.connection.cursor() as cursor:
                if book[11] and datetime.date.today() > book[11]:
                    days_overdue = (datetime.date.today() - book[11]).days
                    fee_amount = days_overdue * 0.5  # 50 cents per day overdue

                    # Check if there's an existing fee record for this book and user
                    cursor.execute(
                        """
                        SELECT fee_id FROM Fee
                        WHERE book_id = %s AND user_id = %s
                    """,
                        (book[0], book[7]),
                    )
                    existing_fee_id = cursor.fetchone()

                    if existing_fee_id:
                        # Update existing fee record
                        update_query = """
                        UPDATE Fee
                        SET fee_amount = %s
                        WHERE fee_id = %s
                        """
                        cursor.execute(update_query, (fee_amount, existing_fee_id[0]))
                    else:
                        # Insert a new fee record
                        insert_query = """
                        INSERT INTO Fee (book_id, fee_amount, user_id)
                        VALUES (%s, %s, %s)
                        """
                        cursor.execute(insert_query, (book[0], fee_amount, book[7]))

                else:
                    # If book is not overdue, ensure there's no fee record
                    cursor.execute(
                        """
                        DELETE FROM Fee
                        WHERE book_id = %s AND user_id = %s
                    """,
                        (book[0], book[7]),
                    )

        finally:
            self.connection.commit()

    def search_user_id(self, user_id):
        """
        Search for books associated with a specific user ID.

        Args:
            user_id (int): The user ID to search for.

        Returns:
            list: A list of books associated with the user ID, if found. Otherwise, an empty list.
        """
        try:
            if not self.connection:
                self.connect_to_database()

            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT patron_id FROM Patron WHERE user_id = %s", (user_id,)
                )
                result = cursor.fetchone()

                if result:
                    patron_id = result[0]
                    cursor.execute(
                        "SELECT * FROM Book WHERE patron_id = %s", (patron_id,)
                    )
                    books = cursor.fetchall()

                    if books:
                        print(
                            "\nFound books for user with user_id {}:\n".format(user_id)
                        )
                        print(
                            "{:<8} | {:<25} | {:<20} | {:<15} | {:<15} | {}".format(
                                "Book ID",
                                "Title",
                                "Author",
                                "ISBN",
                                "Publisher",
                                "Fee Amount",
                            )
                        )
                        print("-" * 100)

                        for book in books:
                            self.calculate_fee(book)
                            cursor.execute(
                                "SELECT fee_amount FROM Fee WHERE book_id = %s AND user_id = %s",
                                (book[0], patron_id),
                            )
                            fee_amount = (
                                cursor.fetchone()[0] if cursor.rowcount > 0 else 0.0
                            )
                            fee_amount_str = "${:.2f}".format(fee_amount)
                            status = "Available" if not book[10] else "Checked Out"
                            print(
                                "{:<8} | {:<25} | {:<20} | {:<15} | {:<15} | {}".format(
                                    book[0],
                                    book[1],
                                    book[2],
                                    book[6],
                                    book[4],
                                    fee_amount_str,
                                    status,
                                )
                            )

                        return books
                    else:
                        print(
                            "No books found for user with user_id {}.".format(user_id)
                        )
                        return []

                else:
                    print("User with user_id {} not found.".format(user_id))
                    return []

        except pymysql.MySQLError as error:
            print("Failed to connect to the database: {}".format(error))
            return []

        finally:
            self.connection.commit()

    def search_author(self, author):
        """
        Search books by author in the database.

        Args:
        - author: The author to search for.

        Returns:
        - A list of books written by the author.
        """
        try:
            # Connect to the database and execute the query
            self.connect_to_database()
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM Book WHERE author = '{author}'")
                books = cursor.fetchall()

            if books:
                print("\nFound books by author {}:\n".format(author))
                print(
                    "{:<8} | {:<25} | {:<20} | {:<15} | {}".format(
                        "Book ID", "Title", "Author", "ISBN", "Publisher"
                    )
                )
                print("-" * 80)

                for book in books:
                    status = "Checked Out" if book[10] else "Available"
                    print(
                        "{:<8} | {:<25} | {:<20} | {:<15} | {}".format(
                            book[0], book[1], book[2], book[6], book[4], status
                        )
                    )

                return books
            else:
                print("No books found by author {}.".format(author))
                return []

        except pymysql.MySQLError as error:
            print("Failed to connect to the database: {}".format(error))
            return []

        finally:
            pass

    def search_publisher(self, publisher):
        """
        Search books by publisher in the database.

        Args:
        - publisher: The publisher to search for.

        Returns:
        - A list of books published by the publisher.
        """
        try:
            # Connect to the database and execute the query
            self.connect_to_database()
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM Book WHERE publisher = '{publisher}'")
                books = cursor.fetchall()

            if books:
                print("\nFound books published by {}:\n".format(publisher))
                print(
                    "{:<8} | {:<25} | {:<20} | {:<15} | {}".format(
                        "Book ID", "Title", "Author", "ISBN", "Status"
                    )
                )
                print("-" * 80)

                for book in books:
                    status = "Checked Out" if book[10] else "Available"
                    print(
                        "{:<8} | {:<25} | {:<20} | {:<15} | {}".format(
                            book[0], book[1], book[2], book[6], status
                        )
                    )

                return books
            else:
                print("No books found published by {}.".format(publisher))
                return []

        except pymysql.MySQLError as error:
            print("Failed to connect to the database: {}".format(error))
            return []

        finally:
            pass

    def search_title(self, title):
        """
        Search books by title in the database.

        Args:
        - title: The title to search for.

        Returns:
        - A list of books matching the title.
        """
        try:
            # Connect to the database and execute the query
            self.connect_to_database()
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM Book WHERE title LIKE '%{title}%'")
                books = cursor.fetchall()

            if books:
                print("\nFound books with title {}:\n".format(title))
                print(
                    "{:<8} | {:<25} | {:<20} | {:<15} | {}".format(
                        "Book ID", "Title", "Author", "ISBN", "Status"
                    )
                )
                print("-" * 80)

                for book in books:
                    status = "Checked Out" if book[10] else "Available"
                    print(
                        "{:<8} | {:<25} | {:<20} | {:<15} | {}".format(
                            book[0], book[1], book[2], book[6], status
                        )
                    )

                return books
            else:
                print("No books found with title {}.".format(title))
                return []

        except pymysql.MySQLError as error:
            print("Failed to connect to the database: {}".format(error))
            return []

        finally:
            pass

    def put_book_on_hold(self, isbn, user_id):
        """
        Put a book on hold in the database.

        Args:
        - isbn: The ISBN of the book to put on hold.
        - user_id: The user ID of the patron placing the book on hold.
        """
        try:
            # Connect to the database
            self.connect_to_database()

            with self.connection.cursor() as cursor:
                # Get patron_id based on user_id
                cursor.execute(
                    "SELECT patron_id FROM Patron WHERE user_id = %s", (user_id,)
                )
                result = cursor.fetchone()

                if result:
                    patron_id = result[0]

                    # Calculate expiration date (3 days later)
                    hold_end = datetime.date.today() + datetime.timedelta(days=3)

                    # Update the Book entry in the database
                    update_query = """
                    UPDATE Book
                    SET
                        patron_id = %s,
                        on_hold = %s,
                        hold_end = %s
                    WHERE isbn = %s
                    """
                    cursor.execute(update_query, (patron_id, True, hold_end, isbn))

                    print("Book put on hold successfully!")

                else:
                    print(f"User with user_id {user_id} not found.")

        except pymysql.MySQLError as error:
            print(f"Failed to connect to the database: {error}")

        finally:
            # Close the database connection
            self.close_connection()

    def take_book_off_hold(self, isbn):
        """
        Take a book off hold in the database.

        Args:
        - isbn: The ISBN of the book to take off hold.
        """
        try:
            # Connect to the database
            self.connect_to_database()

            with self.connection.cursor() as cursor:
                # Update the Book entry in the database
                update_query = """
                UPDATE Book
                SET
                    patron_id = NULL,
                    on_hold = %s,
                    hold_end = NULL
                WHERE isbn = %s
                """
                cursor.execute(update_query, (False, isbn))

                print("Book taken off hold successfully!")

        except pymysql.MySQLError as error:
            print(f"Failed to connect to the database: {error}")

        finally:
            # Close the database connection
            self.close_connection()

    def pay_overdue_fees(self, user_id, book_id):
        """
        Pay overdue fees for a specific book associated with a user.

        Args:
            user_id (int): The user ID associated with the fees.
            book_id (int): The book ID for which the fees are being paid.

        Returns:
            None
        """
        try:
            if not self.connection:
                self.connect_to_database()

            with self.connection.cursor() as cursor:

                cursor.execute(
                    "SELECT patron_id FROM Patron WHERE user_id = %s", (user_id,)
                )
                result = cursor.fetchone()
                # Check if the fee record exists for the given book_id and user_id
                cursor.execute(
                    "SELECT * FROM Fee WHERE book_id = %s AND user_id = %s",
                    (book_id, result),
                )
                fee_record = cursor.fetchone()

                if fee_record:
                    # Delete the fee record
                    cursor.execute(
                        "DELETE FROM Fee WHERE book_id = %s AND user_id = %s",
                        (book_id, result),
                    )
                    print("Overdue fees for book {} paid successfully.".format(book_id))
                else:
                    print(
                        "No overdue fees found for book {} and user {}.".format(
                            book_id, user_id
                        )
                    )

        except pymysql.MySQLError as error:
            print("Failed to pay overdue fees: {}".format(error))

        finally:
            # Commit the transaction
            self.connection.commit()

    def search_fees_by_user_id(self, user_id):
        """
        Search for fees associated with a user by their user ID.

        Args:
            user_id (int): The user ID to search for.

        Returns:
            list: A list of tuples containing fee information if fees are found, otherwise an empty list.
        """
        try:
            if not self.connection:
                self.connect_to_database()

            with self.connection.cursor() as cursor:
                cursor.execute(
                    "SELECT patron_id FROM Patron WHERE user_id = %s", (user_id,)
                )
                result = cursor.fetchone()
                cursor.execute("SELECT * FROM Fee WHERE user_id = %s", (result,))
                fees = cursor.fetchall()

                if fees:
                    print("\nFound fees for user with user_id {}:\n".format(user_id))
                    print(
                        "{:<8} | {:<8} | {:<10} | {}".format(
                            "Fee ID", "Book ID", "Amount", "Patron ID"
                        )
                    )
                    print("-" * 50)

                    for fee in fees:
                        print(
                            "{:<8} | {:<8} | {:<10} | {}".format(
                                fee[0], fee[1], "${:.2f}".format(fee[2]), fee[3]
                            )
                        )

                    return fees
                else:
                    print("No fees found for user with user_id {}.".format(user_id))
                    return []

        except pymysql.MySQLError as error:
            print("Failed to connect to the database: {}".format(error))
            return []

        finally:
            pass

    def total_books_in_library(self):
        """
        Retrieves the total amount of fees collected from users.

        Returns:
            float: The total amount of fees collected.
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Book")
                result = cursor.fetchone()
                return result[0] if result else 0
        except pymysql.MySQLError as error:
            print(f"Failed to fetch total books: {error}")
            return 0

    def total_fees(self):
        """
        Retrieves the total amount of fees owed by users.

        Returns:
            float: The total amount of fees owed.
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT SUM(fee_amount) FROM Fee")
                result = cursor.fetchone()
                return result[0] if result else 0
        except pymysql.MySQLError as error:
            print(f"Failed to fetch total fees: {error}")
            return 0

    def total_patrons(self):
        """
        Retrieves the total number of patrons in the library.

        Returns:
            int: The total number of patrons.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Patron")
                result = cursor.fetchone()
                return result[0] if result else 0
        except pymysql.MySQLError as error:
            print(f"Failed to fetch total patrons: {error}")
            return 0

    def total_librarians(self):
        """
        Retrieves the total number of librarians in the library.

        Returns:
            int: The total number of librarians.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Librarian")
                result = cursor.fetchone()
                return result[0] if result else 0
        except pymysql.MySQLError as error:
            print(f"Failed to fetch total librarians: {error}")
            return 0

    def total_admins(self):
        """
        Retrieves the total number of administrators in the library.

        Returns:
            int: The total number of administrators.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Admin")
                result = cursor.fetchone()
                return result[0] if result else 0
        except pymysql.MySQLError as error:
            print(f"Failed to fetch total admins: {error}")
            return 0

    def close_connection(self):
        """
        Close the connection to the MySQL database if it is active.
        """
        if self.connection:
            self.connection.close()
