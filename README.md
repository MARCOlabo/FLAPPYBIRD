# FLAPPYBIRD


# Pigeon Selling Management System
  -The Pigeon Selling Management System is a multi-functional application designed for user registration, sales tracking, inventory management, and administrative control, with functionalities spanning both the customer and administrator levels.

 Key Components
#  User Registration
  -A sign-up interface ensures secure registration of users with validation for username, email, age, and password.
  -User data is stored in an SQLite database (users.db).
  -Admin Dashboard
  -A robust interface for managing users and inventory (pigeons).
  -Administrators can add, edit, or delete users and pigeons with dynamic updates reflected in the system.
  
#  Login System
  -A secure login system validates credentials and grants access to either the Admin Dashboard or the User Dashboard.
#  Admin Login:
  -Predefined credentials: admin/admin123.
  -Grants access to administrative functionalities.
  
#  User Login:
  -Authenticates credentials from the database.
  -Provides access to user-specific dashboards.
  
#  Features Overview
#  User Management
 -Add new users with unique usernames and emails.
  -View and edit user information, including age and password.
  -Delete user accounts.
  -Inventory (Pigeon) Management
  -Add pigeons with attributes like color, ring band, bloodline, price, and gender.
  -Edit or delete pigeon entries.
  -View pigeon inventory in a tabular format.
  
#  Authentication
  -A secure login system allows only registered users and administrators to access their respective dashboards.
  -Sign-up functionality for creating new user accounts.

#  Prerequisites
  -Python 3.x
  -SQLite (bundled with Python)
#  Required Libraries
'pip install tkinter sqlite3'

#  How to Run
  -Clone Repository
git clone <https://github.com/MARCOlabo/FLAPPYBIRD/tree/main>
cd <PROJECT_PYTHON>

#  Run the User Interfaces:
  -User Sign-up:
python SignUpView.py

  -Login System:
python Login.py
  -Admin Dashboard (accessible via admin login):
python AdminDashboard.py

#  Database Structure
  -users Table
Column	Type	Description
id	INTEGER	Primary key, auto-increment.
username	TEXT	Unique, stores the user's username.
email	TEXT	Unique, stores the user's email.
age	INTEGER	Stores the user's age.
password	TEXT	Stores the user's password.
  -pigeons Table
Column	Type	Description
id	INTEGER	Primary key, auto-increment.
color	TEXT	Color of the pigeon.
ringband	TEXT	Ring band ID (optional).
bloodline	TEXT	Bloodline of the pigeon (optional).
price	INTEGER	Price of the pigeon.
gender	TEXT	Gender of the pigeon.
registeredby	TEXT	Registered by (e.g., admin).

#  Directory Structure
| Project/
|-- SignUpView.py # User sign-up interface
|-- Login.py # Login system
|-- AdminDashboard.py # Admin management interface
|-- MainView.py # User-specific dashboard (required for full functionality)
|-- users.db # SQLite database
|-- README.md # Documentation
