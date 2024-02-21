 
<!-- PROJECT SHIELDS -->  
[![Contributors][contributors-shield]][contributors-url]  
![Commits][commit-shield]  
![pypi-shield]  

<br />  
<div align="center">  
    <h1 align="center">Integrated Library System 
</div>  
  
  
<!-- TABLE OF CONTENTS -->  
  
# Table of Contents:  
- [Introduction](#introduction)  
- [Contributors](#contributors)
- [Installation](#installation)
- [Usage](#usage)
- [Database Setup](#database-setup)
- [Functionalities](#functionalities)
- [File Structure](#file-structure)



  ## Introduction

The Library Management System is a Python-based project designed to handle various tasks related to a library, including managing books, patrons, librarians, and administrators. The system uses a MySQL database to store information.


### Contributors  
- Denitri Douglas
- Pheobe Andrews
- Connor Nelson



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

## Usage

1. Run the `testing.py` file to start the Library Management System:

   ```bash
   python testing.py
   ```

2. Follow the on-screen prompts to interact with the system.

## Database Setup

Ensure that you have MySQL installed and set up on your machine. Modify the `data_loader.py`, and `the book.py` file with your database configuration:

```python

# Change these values based on your MySQL setup
host = 'localhost'
user = 'your_username'
password = 'your_password'
database = 'librarysystem'
```

## Functionalities

The Library Management System provides the following functionalities:

- User creation 
- User authentication (Patron, Librarian, Admin)
- Book checkout and check-in
- Search for books by ISBN, genre, user ID, author, publisher, or title
- Putting books on hold


## File Structure

- `testing.py`: Main script to run the Library Management System.
- `data_loader.py`: Handles database operations and data loading.
- `book.py`: Defines the Book class.
- `patron.py`: Defines the Patron class.
- `librarian.py`: Defines the Librarian class.
- `admin.py`: Defines the Admin class.
- `requirements.txt`: Contains the required Python packages.



<!-- MARKDOWN LINKS & IMAGES  -->  
  
[contributors-shield]: https://img.shields.io/github/contributors/DSDouglas/Integrated-Library-System 
[contributors-url]: https://github.com/DSDouglas/Integrated-Library-System/graphs/contributors  
[commit-shield]: https://img.shields.io/github/last-commit/DSDouglas/Integrated-Library-System 
[pypi-shield]: https://img.shields.io/pypi/pyversions/iconsdk
