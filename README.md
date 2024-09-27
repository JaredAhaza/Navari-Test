# Navari-Test
This ia a library management system that I am doing as a software development test for Navari.

## Features
- User registration and authentication
- Book management system
- Issue and return book management system through admin
- Charge fees for books with fines where applicable and issue invoices
- User roles and permissions management system
- Admin dashboard for managing all the above features

## Technologies used
- Python
- Django
- SQLite
- HTML, CSS, JavaScript, Bootstrap

## User story
- This system allows admin CRUD operations for the management of books in the library. These actions include:
  - Creating user groups.
  - Assigning permissions to user groups.
  - Adding, editing, and deleting customers.
  - Adding, editing, and deleting books.
  - Issuing and returning books.
  - Viewing user activity logs.
  - Issuing Invoices to users returning books.
  - Track debts of customers.

- This sytem also allows customers to perform some limited operations on it which include:
  - Creating user accounts.
  - Logging in to their account.
  - Viewing books in the library.
  - Checking the availability of books.
  - Searching for books by title, category or author.
  - Viewing the pricing of books.

## How to run
- Clone repository using the git clone command
- Create virtualenvironment
- Use pip command to install the requirements.txt file to run the project
- Use the following credentials for superuser or create a new one:
  - Username: tech
  - password: 12345678

## Screenshots

### Homepage
![Homepage screenshot for customer](screenshots/screenshot1.png)
![Homepage screenshot for Search](screenshots/screenshot2.png)
![Homepage screenshot for books list](screenshots/screenshot3.png)

### Customer Accounts
![User Registration screenshot for customer](screenshots/screenshot4.png)
![User Login screenshot for customer](screenshots/screenshot5.png)

### Admin Side
![Admin homepage screenshot](screenshots/screenshot6.png)
![Admin side customer list screenshot](screenshots/screenshot7.png)
![Admin side user list screenshot](screenshots/screenshot8.png)
![Admin side groups list screenshot](screenshots/screenshot9.png)
![Admin side Books list screenshot](screenshots/screenshot10.png)
![Admin side borrowings screenshot](screenshots/screenshot11.png)
![Admin side debts screenshot](screenshots/screenshot12.png)
![Admin side invoices screenshot](screenshots/screenshot13.png)
![Admin side returnings screenshot](screenshots/screenshot14.png)