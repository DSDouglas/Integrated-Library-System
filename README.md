 
<!-- PROJECT SHIELDS -->  
[![Contributors][contributors-shield]][contributors-url]  
![Commits][commit-shield]  
![pypi-shield]  

<br />  
<div align="center">  
    <h1 align="center">Integrated Library System 
</div>  
  

<!-- TABLE OF CONTENTS -->

## Table of Contents:
- [Introduction](#introduction)
- [Contributors](#contributors)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Usage](#usage)

## Introduction

The Library Management System is a Python-based project designed to handle various tasks related to a library, including managing books, patrons, librarians, and administrators. The system uses a MySQL database to store information.

Deployed Software: [Link to Deployed Software](http://18.204.180.15:8000/)

### Contributors
- Denitri Douglas
- Phoebe Andrews
- Connor Nelson

### Software Requirements
- Python 3.9+
- Django
- Pymysql
- Requests
- mod_wsgi
- httpd
- MariaDB/MySQL

## Installation

To run the Library Management System, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/library-management-system.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Database Setup
3. Please install a working MariaDB/MySQL database with a user that has permissions to operate on the chosen DB.
4. Add your IP to the allowed hosts and modify the `databases` variable in the `settings.py` file to correctly connect to your database.

```bash
python manage.py runmodwsgi --working-directory .
```

(From the project root directory)
- Deploy the server with:

```bash
python manage.py runmodwsgi --log-to-terminal --startup-log --port 8000 --setup-only --server-name <server name or IP> --server-root <an empty directory>
```

Followed by:

```bash
<server-root directory>/apachectl start
```

## Usage

- **Home**: This page features a book of the day included in the library catalogue along with descriptions. 
- **Create Account**: Follow the prompts on the screen to create an account taking head of the password requirements, and username restrictions.
- **Login**: Login to this page with your created username and password
- **Catalog**: Once logged in you can browse the inventory by searching for books in the search field or navigating via the numeric links at the bottom or the page.
- **Reservations**: place a book on hold by selecting the “place hold” button to the right of the book. You will then see the hold expiration date.
- **Check-out**: Check out a book by selecting the radio to the left of the book cover and selecting check out at the bottom of the page.
- **User – Checked out books**: use this page to view your checked out books, check in books, and pay fees.
- **User – Logout**: Logout of your account.

<!-- MARKDOWN LINKS & IMAGES  -->

[contributors-shield]: https://img.shields.io/github/contributors/DSDouglas/Integrated-Library-System
[contributors-url]: https://github.com/DSDouglas/Integrated-Library-System/graphs/contributors
[commit-shield]: https://img.shields.io/github/last-commit/DSDouglas/Integrated-Library-System
[pypi-shield]: https://img.shields.io/badge/Python-3.9%2B-purple
```

