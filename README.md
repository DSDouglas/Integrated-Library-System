 
<!-- PROJECT SHIELDS -->  
[![Contributors][contributors-shield]][contributors-url]  
![Commits][commit-shield]  
![Database]  
![pypi-shield]  



<br />  
<div align="center">  
    <h1 align="center">Integrated Library System 
</div>  
  

<!-- TABLE OF CONTENTS -->

## Table of Contents
- [Introduction](#introduction)
- [Contributors](#contributors)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Install Dependencies](#dependencies)
- [Launch Software](#launch)
- [Deploy](#deploy)
- [Usage](#usage)
- [Deployed Software](https://group7.teacake.dev/)

## Introduction

The Library Management System is a Python-based project designed to handle various tasks related to a library, including managing books, patrons, librarians, and administrators. The system uses a MySQL database to store information. This software has been deployed and can be accessed via the "Deployed Software" link in the table of contents above. 

The installation guide expects a Linux OS and explains the necessary software and tools needed to start locally hosting the Integrated Library System. It also covers installing a MariaDB or MySQL database to pair with the management system. 


## Contributors

- Denitri Dougals - Project Manager, Developer
- Connor Nelson - Developer 
- Phoebe Andrews - Database Administrator 

## Software Requirements
- Python 3.9+
- Django
- Pymysql
- Requests
- MariaDB/MySQL
- Nginx
- Gunicorn

## Installation

To run the Library Management System, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/library-management-system.git
   ```  

## Database Setup
2. Please install a working MariaDB/MySQL database with a user that has permissions to operate on the chosen DB. 

This can be done using the MariaDB or MySQL secure installation script provided with the package. 

If you wish to set up an Amazon RDS DB instance for your Integrated Library System, the official Amazon User Guide can be found at: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Tutorials.WebServerDB.CreateDBInstance.html  

## Dependencies

3. Install Nginx
  ```bash
  “sudo yum install nginx python3” (or your OS’s equivalent) 
  ```
4. Install software requirements
  ```bash
   pip install -r requirements.txt
  ```
6.  Add your IP to the allowed hosts and modify the databases variable in config.json file to correctly connect to your database. 

## Launch

To run locally: (From the project root directory) 
  ```bash
  “python manage.py runserver <ip:port>”
  ```

## Deploy

Follow the Nginx and gunicorn quickstart documentation to create a gunicorn.service and gunicorn.socket to serve your app to the nginx service https://docs.gunicorn.org/en/latest/deploy.html  
 

Modify the nginx config to support TLS and provide it with the certificate files to enable https and set the proper hostname. 

Followed by: 

```base
“systemctl start gunicorn.service”
```

```bash
“systemctl start nginx”
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
[pypi-shield]: https://img.shields.io/badge/python-3.9%2B-purple
[Database]: https://img.shields.io/badge/database-MariaDB-darkblue

```

