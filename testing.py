import pymysql
from data_loader import DataMover
from user import User
from admin import Admin
from patron import Patron
from book import Book


def load_data_for_testing(data_mover):
    # Create instances for testing
    from librarian import Librarian
    user1 = User("John Doe", 1, "password123")
    admin1 = Admin("AdminUser", 2, "adminpass", 5)
    librarian1 = Librarian("LibrarianUser", 3, "librarianpass")
    patron1 = Patron("PatronUser", 4, "Gold")
    book1 = Book("BookTitle", "BookAuthor", 2022, "BookPublisher", "Fiction", 1234567890)

    # Establish a connection to the database
    data_mover.connect_to_database()

    try:
        # Make sure the connection is established successfully
        if data_mover.connection:
            # Create a cursor object to execute SQL queries
            with data_mover.connection.cursor() as cursor:
                # Create tables
                data_mover.create_tables(cursor)

                # Insert data into tables
                data_mover.insert_data(cursor, [user1, admin1, librarian1, patron1, book1])

                # Commit the changes
                data_mover.connection.commit()
        else:
            print("Failed to establish a database connection.")

    except pymysql.MySQLError as error:
        print(f"Failed to execute SQL queries: {error}")

        # Save information to CSV file for testing
        data_mover.save_to_csv('User', user1)
        data_mover.save_to_csv('Admin', admin1)
        data_mover.save_to_csv('Librarian', librarian1)
        data_mover.save_to_csv('Patron', patron1)
        data_mover.save_to_csv('Book', book1)

    finally:
        # Close the connection
        data_mover.close_connection()


def main():
    from librarian import Librarian
    print("Welcome to the Raleigh Community Library !")

    # Create an instance of DataMover
    data_mover = DataMover()

    # Load data for testing
    load_data_for_testing(data_mover)

    while True:
        role = input("Select your role (Librarian, Admin, Patron): ").lower()

        if role == "librarian" or role == "admin" or role == "patron":
            name = str(input("Enter your name"))
            user_id = str(input("Enter your user ID: "))
            password = input("Enter your password: ")

            if data_mover.validate_user_credentials(user_id, password, role):
                print("Authentication successful!")

                if role == "librarian":
                    librarian = Librarian(name, user_id, password)

                    while True:
                        print("\nLibrarian Menu:")
                        print("1. Create a new patron")
                        print("2. Check out a book")
                        print("3. Check in a book")
                        print("4. Exit")

                        action = input("Select an action (1-4): ")

                        if action == "1":
                            librarian.create_patron()
                        elif action == "2":
                            librarian.check_out_book()
                        elif action == "3":
                            librarian.check_in_book()
                        elif action == "4":
                            break
                        else:
                            print("Invalid choice. Please enter a number between 1 and 4.")
                elif role == "admin":
                    print("\nAdmin Menu:")
                    break
                else:
                    print("\nPatron Menu:")
                    break

            else:
                print("Invalid user ID or password. Please try again.")
                retry = input("Do you want to try again? (yes/no): ").lower()
                if retry != "yes":
                    break
        else:
            print("Invalid role. Please enter Librarian, Admin, or Patron.")


if __name__ == "__main__":
    main()
