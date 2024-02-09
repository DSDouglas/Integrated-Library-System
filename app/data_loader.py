import pymysql
import csv


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
                host='db_host',
                user='db_user',
                password='db_password',
                database='db_name'
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
            """CREATE TABLE IF NOT EXISTS User (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                user_id VARCHAR (255),
                password VARCHAR(255)
            )""",
            """CREATE TABLE IF NOT EXISTS Admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                user_id VARCHAR(255),
                password VARCHAR(255),
                checkout_limit INT
            )""",
            """CREATE TABLE IF NOT EXISTS Librarian (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                user_id VARCHAR(255),
                password VARCHAR(255),
            )""",
            """CREATE TABLE IF NOT EXISTS Patron (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                user_id INT,
            )""",
            """CREATE TABLE IF NOT EXISTS Book (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                author VARCHAR(255),
                date_published INT,
                publisher VARCHAR(255),
                genre VARCHAR(255),
                isbn INT,
                userid INT,
                onhold BOOLEAN,
                checkout BOOLEAN
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
            # Get table name, columns, and values for the insert query
            table_name = instance.__class__.__name__
            columns = ', '.join(instance.__dict__.keys())
            values = ', '.join(
                f"'{value}'" if isinstance(value, str) else str(value) for value in instance.__dict__.values())
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
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
                with self.connection.cursor() as cursors:
                    # Query the database to find the user by user_id
                    cursors.execute(f"SELECT * FROM {role} WHERE user_id = {user_id}")
                    result = cursors.fetchone()

                # If a result is found and the user_id and password match
                if result and result[2] == str(user_id) and result[3] == password:
                    return True

        except pymysql.MySQLError as error:
            # Handle the case where the connection to the database fails
            print(f"Failed to connect to the database: {error}")

        # If not found in the database or connection failed, check the CSV file
        csv_file_path = f"{role}_failed_connections.csv"
        with open(csv_file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Check if the row has enough elements and the username matches
                if len(row) >= 4 and row[1] == str(user_id) and row[3] == password:
                    return True

        # Return False if no match is found
        return False

    def close_connection(self):
        """
        Close the connection to the MySQL database if it is active.
        """
        if self.connection:
            self.connection.commit()
            self.connection.close()
