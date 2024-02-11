import mariadb
import sys

from flask import current_app, g

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="",
        password="",
        host"localhost",
        port=3306,
        database="test",
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()
