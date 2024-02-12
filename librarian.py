import csv
import pymysql
from user import User
from patron import Patron
from data_loader import DataMover


class Librarian(User):
    def __init__(self, name, user_id, password):
        super().__init__(name, user_id, password)
        self.data_mover = DataMover()

    def create_patron(self):
        # Prompt the user to enter patron credentials
        name = input("Enter patron's name: ")
        user_id = input("Enter patron's user ID: ")
        password = input("Enter patron's password: ")
        try:

            # Connect to the database and check if user_id exists
            self.data_mover.connect_to_database()

            with self.data_mover.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM Patron WHERE user_id = '{user_id}'")
                result = cursor.fetchone()

            if result:
                print("User ID already exists. Please try again.")
                return

            # If user_id doesn't exist, create a new Patron instance and update the database
            new_patron = Patron(name, user_id, password)

            with self.data_mover.connection.cursor() as cursor:
                self.data_mover.insert_data(cursor, [new_patron])
                self.data_mover.connection.commit()

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
                writer.writerow(["Patron"] + [name, user_id, password])

            print("Patron created successfully! (Added to failed connections)")

    def check_out_book(self):
        isbn = input("Enter the ISBN of the book to check out: ")
        try:

            # Connect to the database and change the status
            self.data_mover.connect_to_database()

            with self.data_mover.connection.cursor() as cursor:
                cursor.execute(f"UPDATE Book SET checkout = TRUE WHERE isbn = {isbn}")
                self.data_mover.connection.commit()

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

    def check_in_book(self):
        isbn = input("Enter the ISBN of the book to check in: ")
        try:
            # Connect to the database and change the status
            self.data_mover.connect_to_database()

            with self.data_mover.connection.cursor() as cursor:
                cursor.execute(f"UPDATE Book SET checkout = FALSE WHERE isbn = {isbn}")
                self.data_mover.connection.commit()

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





    def __str__(self):
        return f"Librarian(name={self.get_name()}, user_id={self.get_user_id()}, password={self.get_password()})"
