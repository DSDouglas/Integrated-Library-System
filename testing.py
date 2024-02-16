import pymysql
from data_loader import DataMover
from admin import Admin
from patron import Patron
from book import Book


def load_data_for_testing(data_mover):
    # Create instances for testing
    from librarian import Librarian

    admin1 = Admin("Admin1", "User", "admin1@example.com", "1", "adminpass1")
    admin2 = Admin("Admin2", "User", "admin2@example.com", "2", "adminpass2")
    admin3 = Admin("Admin3", "User", "admin3@example.com", "3", "adminpass3")
    admin4 = Admin("Admin4", "User", "admin4@example.com", "4", "adminpass4")
    admin5 = Admin("Admin5", "User", "admin5@example.com", "5", "adminpass5")

    librarian1 = Librarian("Librarian1", "User", "librarian1@example.com", "6", "librarianpass1")
    librarian2 = Librarian("Librarian2", "User", "librarian2@example.com", "7", "librarianpass2")
    librarian3 = Librarian("Librarian3", "User", "librarian3@example.com", "8", "librarianpass3")
    librarian4 = Librarian("Librarian4", "User", "librarian4@example.com", "9", "librarianpass4")
    librarian5 = Librarian("Librarian5", "User", "librarian5@example.com", "10", "librarianpass5")

    patron1 = Patron("Patron1", "User", "patron1@example.com", "11", "Silver")
    patron2 = Patron("Patron2", "User", "patron2@example.com", "12", "Bronze")
    patron3 = Patron("Patron3", "User", "patron3@example.com", "13", "Gold")
    patron4 = Patron("Patron4", "User", "patron4@example.com", "14", "Platinum")
    patron5 = Patron("Patron5", "User", "patron5@example.com", "15", "Diamond")

    book1 = Book("BookTitle1", "BookAuthor1", 2023, "BookPublisher1", "Science Fiction", 2345678901)
    book2 = Book("BookTitle2", "BookAuthor2", 2024, "BookPublisher2", "Mystery", 3456789012)
    book3 = Book("BookTitle3", "BookAuthor3", 2025, "BookPublisher3", "Thriller", 4567890123)
    book4 = Book("BookTitle4", "BookAuthor4", 2026, "BookPublisher4", "Romance", 5678901234)
    book5 = Book("BookTitle5", "BookAuthor5", 2027, "BookPublisher5", "Non-Fiction", 6789012345)

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
                data_mover.insert_data(cursor,
                                       [admin1, admin2, admin3, admin4, admin5, librarian1, librarian2, librarian3,
                                        librarian4, librarian5, patron1, patron2, patron3, patron4, patron5, book1,
                                        book2, book3, book4, book5])

                # Commit the changes
                data_mover.connection.commit()
        else:
            print("Failed to establish a database connection.")

    except pymysql.MySQLError as error:
        print(f"Failed to execute SQL queries: {error}")

        # Save information to CSV file for testing
        data_mover.save_to_csv('Admin', admin1)
        data_mover.save_to_csv('Admin', admin2)
        data_mover.save_to_csv('Admin', admin3)
        data_mover.save_to_csv('Admin', admin4)
        data_mover.save_to_csv('Admin', admin5)
        data_mover.save_to_csv('Librarian', librarian1)
        data_mover.save_to_csv('Librarian', librarian2)
        data_mover.save_to_csv('Librarian', librarian3)
        data_mover.save_to_csv('Librarian', librarian4)
        data_mover.save_to_csv('Librarian', librarian5)
        data_mover.save_to_csv('Patron', patron1)
        data_mover.save_to_csv('Patron', patron2)
        data_mover.save_to_csv('Patron', patron3)
        data_mover.save_to_csv('Patron', patron4)
        data_mover.save_to_csv('Patron', patron5)
        data_mover.save_to_csv('Book', book1)
        data_mover.save_to_csv('Book', book2)
        data_mover.save_to_csv('Book', book3)
        data_mover.save_to_csv('Book', book4)
        data_mover.save_to_csv('Book', book5)

    finally:
        # Close the connection
        data_mover.close_connection()


def main():
    print("Welcome to the Raleigh Community Library !")

    # Create an instance of DataMover
    data_mover = DataMover()

    # Load data for testing
    load_data_for_testing(data_mover)

    while True:
        role = input("Select your role (Librarian, Admin, Patron): ").lower()

        if role == "librarian" or role == "admin" or role == "patron":
            user_id = str(input("Enter your user ID: "))
            password = input("Enter your password: ")

            if data_mover.validate_user_credentials(user_id, password, role):
                print("Authentication successful!")

                if role == "librarian":

                    while True:
                        print("\nLibrarian Menu:")
                        print("1. Create a new patron")
                        print("2. Check out a book")
                        print("3. Check in a book")
                        print("4. Exit")

                        action = input("Select an action (1-4): ")

                        if action == "1":
                            first_name = input("Enter patron's first name: ")
                            last_name = input(" Enter patron's last name: ")
                            email = input("Enter patron's email: ")
                            user_id = input("Enter patron's user ID: ")
                            password = input("Enter patron's password: ")
                            data_mover.create_patron(first_name, last_name, email, user_id, password)
                        elif action == "2":
                            isbn = input("Enter the ISBN of the book to check out: ")
                            data_mover.check_out_book(isbn)
                        elif action == "3":
                            isbn = input("Enter the ISBN of the book to check in: ")
                            data_mover.check_in_book(isbn)
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
