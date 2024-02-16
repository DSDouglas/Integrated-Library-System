import pymysql
import csv
from patron import Patron
from admin import Admin
from book import Book
from librarian import Librarian


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
            self.connection = pymysql.connect(
                host='localhost',
                user='root',
                password='N',
                database='librarysystem'
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
                id INT AUTO_INCREMENT PRIMARY KEY,
                firstname VARCHAR(255),
                lastname VARCHAR(255),
                email VARCHAR(255),
                user_id VARCHAR(255),
                password VARCHAR(255)
            )""",
            """CREATE TABLE IF NOT EXISTS Librarian (
                id INT AUTO_INCREMENT PRIMARY KEY,
                firstname VARCHAR(255),
                lastname VARCHAR(255),
                email VARCHAR(255),
                user_id VARCHAR(255),
                password VARCHAR(255)
            )""",
            """CREATE TABLE IF NOT EXISTS Patron (
                id INT AUTO_INCREMENT PRIMARY KEY,
                firstname VARCHAR(255),
                lastname VARCHAR(255),
                email VARCHAR(255),
                user_id VARCHAR(255),
                password VARCHAR(255)
            )""",
            """CREATE TABLE IF NOT EXISTS Book (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                author VARCHAR(255),
                pub_year YEAR,
                publisher VARCHAR(255),
                genre VARCHAR(255),
                isbn BIGINT,
                user_id VARCHAR(255),
                on_hold BOOLEAN,
                checkout_date DATE,
                due_date DATE,
                fee BOOLEAN,
                fee_amount DECIMAL(10, 2)
            )"""
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
            # Get the names of the attributes (columns) of the instance
            columns = ', '.join(instance.__dict__.keys())
            # Convert attribute values to strings for the SQL query
            values = ', '.join(
                f"'{value}'" if isinstance(value, str) else str(value) for value in instance.__dict__.values())
            # Construct the SQL insert query
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
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
        with open(csv_file_path, mode='a', newline='') as file:
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
        try:
            # Check if there is an active connection
            if self.connection:
                # Use a cursor to execute SQL queries
                with self.connection.cursor() as cursor:
                    # Query the database to find the user by user_id
                    cursor.execute(f"SELECT * FROM {role} WHERE user_id = %s AND password = %s", (user_id, password))
                    result = cursor.fetchone()

                # If a result is found, authentication is successful
                if result:
                    return True

        except pymysql.MySQLError as error:
            # Handle the case where the connection to the database fails
            print(f"Failed to connect to the database: {error}")

        # If not found in the database or connection failed, check the CSV file
        csv_file_path = f"{role}_failed_connections.csv"
        try:
            with open(csv_file_path, mode='r') as file:
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
                with open(csv_file_path, mode='r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) >= 3 and row[1] == user_id:
                            print("User ID already exists in the failed connections. Please try again.")
                            return
            except FileNotFoundError:
                pass  # Continue if the file doesn't exist

            # If user_id not found in the failed connections, add a new row
            with open(csv_file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Patron"] + [first_name, last_name, email, user_id, password])

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
                with open(csv_file_path, mode='r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) >= 3 and row[1] == user_id:
                            print("User ID already exists in the failed connections. Please try again.")
                            return
            except FileNotFoundError:
                pass  # Continue if the file doesn't exist

            # If user_id not found in the failed connections, add a new row
            with open(csv_file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Librarian"] + [first_name, last_name, email, user_id, password])

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
                with open(csv_file_path, mode='r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) >= 3 and row[1] == user_id:
                            print("User ID already exists in the failed connections. Please try again.")
                            return
            except FileNotFoundError:
                pass  # Continue if the file doesn't exist

            # If user_id not found in the failed connections, add a new row
            with open(csv_file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Admin"] + [first_name, last_name, email, user_id, password])

            print("Admin created successfully! (Added to failed connections)")

    def check_out_book(self, isbn):
        """
        Check out a book in the database.

        Args:
        - isbn: The ISBN of the book to check out.
        """
        try:

            # Connect to the database and change the status
            self.connect_to_database()

            with self.connection.cursor() as cursor:
                cursor.execute(f"UPDATE Book SET checkout = TRUE WHERE isbn = {isbn}")
                self.connection.commit()

            print("Book checked out successfully!")

        except (pymysql.MySQLError, AttributeError) as error:
            print(f"Failed to connect to the database: {error}")

            # Check the Book_failed_connections.csv file
            csv_file_path = "Book_failed_connections.csv"
            try:
                with open(csv_file_path, mode='r') as file:
                    reader = csv.reader(file)
                    updated_rows = []
                    for row in reader:
                        if len(row) >= 7 and row[6] == isbn:
                            row[7] = "True"
                        updated_rows.append(row)

                # Write updated rows back to the CSV file
                with open(csv_file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(updated_rows)

                print("Book checked out successfully! (Updated in failed connections)")

            except FileNotFoundError:
                print("Book checked out successfully! (Added to failed connections)")

    def check_in_book(self, isbn):
        """
        Check in a book in the database.

        Args:
        - isbn: The ISBN of the book to check in.
        """
        try:
            # Connect to the database and change the status
            self.connect_to_database()

            with self.connection.cursor() as cursor:
                cursor.execute(f"UPDATE Book SET checkout = FALSE WHERE isbn = {isbn}")
                self.connection.commit()

            print("Book checked in successfully!")

        except (pymysql.MySQLError, AttributeError) as error:
            print(f"Failed to connect to the database: {error}")

            # Check the Book_failed_connections.csv file
            csv_file_path = "Book_failed_connections.csv"
            try:
                with open(csv_file_path, mode='r') as file:
                    reader = csv.reader(file)
                    updated_rows = []
                    for row in reader:
                        if len(row) >= 8 and row[6] == isbn:
                            row[7] = "False"
                        updated_rows.append(row)

                # Write updated rows back to the CSV file
                with open(csv_file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(updated_rows)

                print("Book checked in successfully! (Updated in failed connections)")

            except FileNotFoundError:
                print("Book checked in successfully! (Added to failed connections)")

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
            return books

        except pymysql.MySQLError as error:
            print(f"Failed to connect to the database: {error}")
            return []

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
            return books

        except pymysql.MySQLError as error:
            print(f"Failed to connect to the database: {error}")
            return []

    def search_user_id(self, user_id):
        """
        Search books by user ID in the database.

        Args:
        - user_id: The user ID to search for.

        Returns:
        - A list of books associated with the user ID.
        """
        try:
            # Connect to the database and execute the query
            self.connect_to_database()
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM Book WHERE user_id = '{user_id}'")
                books = cursor.fetchall()
            return books

        except pymysql.MySQLError as error:
            print(f"Failed to connect to the database: {error}")
            return []

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
            return books

        except pymysql.MySQLError as error:
            print(f"Failed to connect to the database: {error}")
            return []

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
            return books

        except pymysql.MySQLError as error:
            print(f"Failed to connect to the database: {error}")
            return []

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
            return books

        except pymysql.MySQLError as error:
            print(f"Failed to connect to the database: {error}")
            return []

    def put_book_on_hold(self, isbn):
        """
        Put a book on hold in the database.

        Args:
        - isbn: The ISBN of the book to put on hold.
        """
        try:
            # Connect to the database
            self.connect_to_database()

            # Search for the book with the given ISBN
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM Book WHERE isbn = '{isbn}'")
                book_data = cursor.fetchone()

            # If the book is found, create a Book instance and put it on hold
            if book_data:
                book = Book(*book_data)
                book.on_hold(book)
                print("Book put on hold successfully!")
            else:
                print("Book not found in the database.")

        except pymysql.MySQLError as error:
            print(f"Failed to connect to the database: {error}")
        finally:
            # Close the database connection
            self.close_connection()

    def close_connection(self):
        """
        Close the connection to the MySQL database if it is active.
        """
        if self.connection:
            self.connection.close()
