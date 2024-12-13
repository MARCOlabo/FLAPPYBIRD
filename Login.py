from AdminDashboard import AdminDashboard
from MainView import UserDashboard
import tkinter as tk
from tkinter import messagebox


class Login(tk.Tk):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager

        # Window Setup
        self.title("Login")
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

        # Welcome Message
        welcome_label = tk.Label(self.left_panel, text="Welcome Kalapatids!", font=("Segoe UI", 16), fg="white", bg="#006666")
        welcome_label.place(x=30, y=250)

        # Right Panel (Form)
        self.right_panel = tk.Frame(self.main_panel, bg="white", width=550, height=600)
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        # Title
        title_label = tk.Label(self.right_panel, text="LOGIN", font=("Segoe UI", 30, "bold"), fg="#006666", bg="white")
        title_label.place(x=200, y=30)

        # Username
        username_label = tk.Label(self.right_panel, text="Username:", font=("Segoe UI", 12), bg="white")
        username_label.place(x=50, y=150)
        self.username_field = tk.Entry(self.right_panel, font=("Segoe UI", 12))
        self.username_field.place(x=200, y=150, width=300, height=30)

        # Password
        password_label = tk.Label(self.right_panel, text="Password:", font=("Segoe UI", 12), bg="white")
        password_label.place(x=50, y=200)
        self.password_field = tk.Entry(self.right_panel, font=("Segoe UI", 12), show="*")
        self.password_field.place(x=200, y=200, width=300, height=30)

        # Buttons
        self.login_button = tk.Button(self.right_panel, text="Login", bg="#006666", fg="white", font=("Segoe UI", 12), command=self.handle_login)
        self.login_button.place(x=150, y=300, width=100, height=30)

        self.signup_button = tk.Button(self.right_panel, text="Create a new account", bg="white", fg="red", font=("Segoe UI", 12), command=self.open_signup)
        self.signup_button.place(x=300, y=300, width=200, height=30)

    def handle_login(self):
        # Get input values
        username = self.username_field.get()
        password = self.password_field.get()

        # Predefined admin credentials
        admin_username = "admin"
        admin_password = "admin123"

        # Validate input
        if not username or not password:
            messagebox.showerror("Error", "Both fields are required.")
            return

        # Check if the login is for the admin
        if username == admin_username and password == admin_password:
            messagebox.showinfo("Success", f"Welcome, Admin!")
            self.destroy()  # Close login window after successful login
            root = tk.Tk()  # Create the admin dashboard window
            AdminDashboard(root)
            root.mainloop()
            return

        # Authenticate user for regular user login
        user = self.db_manager.authenticate_user(username, password)
        if user:
            messagebox.showinfo("Success", f"Welcome, {user[1]}!")
            self.destroy()  # Close login window after successful login
            main_view = tk.Tk()
            UserDashboard(main_view, username=user[1], db_manager=self.db_manager)
            main_view.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password.")


    def open_signup(self):
        # Logic to open the signup view
        self.destroy()
        from SignUpView import SignUpView  # Ensure SignUpView is correctly imported
        signup_app = SignUpView(self.db_manager)
        signup_app.mainloop()


if __name__ == "__main__":
    from SignUpView import DatabaseManager  # Use the same DatabaseManager class

    db_manager = DatabaseManager()
    app = Login(db_manager)
    app.mainloop()