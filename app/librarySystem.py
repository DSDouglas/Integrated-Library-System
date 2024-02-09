from data_loader import DataMover
from librarian import Librarian
from admin import Admin
from patron import Patron
from book import Book


def main():
    print("Welcome to the Library Management System!")

    while True:
        role = input("Select your role (Librarian, Admin, Patron): ").lower()

        if role == "librarian" or role == "admin" or role == "patron":
            user_id = int(input("Enter your user ID: "))
            password = input("Enter your password: ")

            if DataMover.validate_user_credentials(user_id, password):
                print("Authentication successful!")

                if role == "librarian":
                    handle_librarian_actions(user_id)
                elif role == "admin":
                    handle_admin_actions(user_id)
                else:
                    handle_patron_actions(user_id)

            else:
                print("Invalid user ID or password. Please try again.")
                retry = input("Do you want to try again? (yes/no): ").lower()
                if retry != "yes":
                    break
        else:
            print("Invalid role. Please enter Librarian, Admin, or Patron.")


def handle_librarian_actions(user_id):
    while True:
        print("\nLibrarian Actions:")
        print("1. Create new patron logins")
        print("2. Check in or check out books")
        print("3. Exit")

        choice = input("Enter your choice (1, 2, 3): ")

        if choice == "1":
            create_patron_logins()
        elif choice == "2":
            checkin_checkout_books()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def handle_admin_actions(user_id):
    while True:
        print("\nAdmin Actions:")
        print("1. Change checkout limit")
        print("2. Create librarian users")
        print("3. Exit")

        choice = input("Enter your choice (1, 2, 3): ")

        if choice == "1":
            change_checkout_limit()
        elif choice == "2":
            create_librarian_users()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def handle_patron_actions(user_id):
    print("\nPatron Actions:")
    # patron actions


def create_patron_logins():
    print("Creating new patron logins...")
    # create new patron logins


def checkin_checkout_books():
    print("Checking in or checking out books...")
    # librarian to check in or check out books


def change_checkout_limit():
    print("Changing checkout limit...")
    # admin to change checkout limit


def create_librarian_users():
    print("Creating librarian users...")
    # admin to create librarian users


if __name__ == "__main__":
    main()
