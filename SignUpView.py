import tkinter as tk
from tkinter import messagebox
import re
import sqlite3

class DatabaseManager:
    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_users_table()

    def create_users_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER NOT NULL,
                password TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def add_user(self, username, email, age, password):
        try:
            self.cursor.execute(
                "INSERT INTO users (username, email, age, password) VALUES (?, ?, ?, ?)",
                (username, email, age, password),
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def authenticate_user(self, username, password):
        self.cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?", (username, password)
        )
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()


class SignUpView(tk.Tk):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager

        # Window Setup
        self.title("Sign Up")
        self.geometry("900x600")
        self.resizable(False, False)

        # Main Panel
        self.main_panel = tk.Frame(self)
        self.main_panel.pack(fill=tk.BOTH, expand=True)

        # Left Panel (Decorative Side)
        self.left_panel = tk.Frame(self.main_panel, bg="#006666", width=350, height=600)
        self.left_panel.grid(row=0, column=0, sticky="nsew")

        # Company Label
        company_label = tk.Label(self.left_panel, text="Pigeon Selling Management", font=("Showcard Gothic", 14, "bold"), fg="white", bg="#006666")
        company_label.place(x=30, y=200)

        # Right Panel (Form)
        self.right_panel = tk.Frame(self.main_panel, bg="white", width=550, height=600)
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        # Title
        title_label = tk.Label(self.right_panel, text="SIGN UP", font=("Segoe UI", 30, "bold"), fg="#006666", bg="white")
        title_label.place(x=200, y=30)

        # Username
        username_label = tk.Label(self.right_panel, text="Username:", font=("Segoe UI", 12), bg="white")
        username_label.place(x=50, y=100)
        self.username_field = tk.Entry(self.right_panel, font=("Segoe UI", 12))
        self.username_field.place(x=200, y=100, width=300, height=30)

        # Email
        email_label = tk.Label(self.right_panel, text="Email:", font=("Segoe UI", 12), bg="white")
        email_label.place(x=50, y=150)
        self.email_field = tk.Entry(self.right_panel, font=("Segoe UI", 12))
        self.email_field.place(x=200, y=150, width=300, height=30)

        # Age
        age_label = tk.Label(self.right_panel, text="Age:", font=("Segoe UI", 12), bg="white")
        age_label.place(x=50, y=200)
        self.age_field = tk.Entry(self.right_panel, font=("Segoe UI", 12))
        self.age_field.place(x=200, y=200, width=300, height=30)

        # Password
        password_label = tk.Label(self.right_panel, text="Password:", font=("Segoe UI", 12), bg="white")
        password_label.place(x=50, y=250)
        self.password_field = tk.Entry(self.right_panel, font=("Segoe UI", 12), show="*")
        self.password_field.place(x=200, y=250, width=300, height=30)

        # Confirm Password
        confirm_password_label = tk.Label(self.right_panel, text="Confirm Password:", font=("Segoe UI", 12), bg="white")
        confirm_password_label.place(x=50, y=300)
        self.confirm_password_field = tk.Entry(self.right_panel, font=("Segoe UI", 12), show="*")
        self.confirm_password_field.place(x=200, y=300, width=300, height=30)

        # Buttons
        self.sign_up_button = tk.Button(self.right_panel, text="Sign Up", bg="#006666", fg="white", font=("Segoe UI", 12), command=self.handle_sign_up)
        self.sign_up_button.place(x=150, y=400, width=100, height=30)

        self.login_button = tk.Button(self.right_panel, text="Already have an account?", bg="white", fg="red", font=("Segoe UI", 12), command=self.open_login)
        self.login_button.place(x=300, y=400, width=200, height=30)

    def handle_sign_up(self):
        # Get input values
        username = self.username_field.get()
        email = self.email_field.get()
        age_text = self.age_field.get()
        password = self.password_field.get()
        confirm_password = self.confirm_password_field.get()

        # Validate input
        if not username or not email or not age_text or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required.")
            return

        # Validate email
        if not self.is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format.")
            return

        # Validate age
        try:
            age = int(age_text)
            if age < 18:
                messagebox.showerror("Error", "You must be at least 18 years old.")
                return
        except ValueError:
            messagebox.showerror("Error", "Age must be a number.")
            return

        # Validate password strength
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long.")
            return

        # Confirm password match
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Register user in the database
        registered = self.db_manager.add_user(username, email, age, password)
        if registered:
            messagebox.showinfo("Success", "Sign-up successful!")
            self.open_login()
        else:
            messagebox.showerror("Error", "Username or email already exists.")

    def is_valid_email(self, email):
        # Simple and effective email regex pattern
        return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))

    def open_login(self):
        # Logic to open the login view
        from Login import Login  # Ensure Login is correctly imported
        login = Login(self.db_manager)  # Pass only db_manager
        self.destroy()  # Close the current SignUpView window (optional)
        login.mainloop()


if __name__ == "__main__":
    db_manager = DatabaseManager()
    app = SignUpView(db_manager)
    app.mainloop()