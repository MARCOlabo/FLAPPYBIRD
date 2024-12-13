import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class UserDashboard:
    def __init__(self, root, username, db_manager):
        self.root = root
        self.root.title("Pigeon Selling")
        self.root.geometry('1200x800')
        self.username = username
        self.db_manager = DatabaseManager()

        self.create_widgets()

    def create_widgets(self):
        # Header
        self.header_frame = tk.Frame(self.root, bg="#006666", height=100)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)

        self.header_label = tk.Label(
            self.header_frame,
            text="Welcome mga Kalapatids",
            font=("Segoe UI", 28, "bold"),
            fg="white",
            bg="#006666"
        )
        self.header_label.pack(pady=20)

        # Menu (Sidebar)
        self.menu_frame = tk.Frame(self.root, bg="white", width=200)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.user_label = tk.Label(
            self.menu_frame,
            text=f"Welcome, {self.username}",
            font=("Segoe UI", 18, "bold")
        )
        self.user_label.pack(pady=20)

        self.view_pigeons_button = self.create_menu_button("View Pigeons", self.view_pigeons)
        self.register_pigeon_button = self.create_menu_button("Sell Pigeon", self.register_pigeon)
        self.account_settings_button = self.create_menu_button("Account Settings", self.account_settings)
        self.logout_button = self.create_menu_button("Logout", self.logout)

        # Content panel (dynamically changing)
        self.content_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.content_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

        self.content_label = tk.Label(
            self.content_frame,
            text="Welcome to User Dashboard",
            font=("Segoe UI", 20)
        )
        self.content_label.pack(pady=50)

    def create_menu_button(self, text, command):
        button = tk.Button(self.menu_frame, text=text, font=("Segoe UI", 16), bg="#006666", fg="white", width=20, command=command)
        button.pack(pady=10)
        return button

    def account_settings(self):
        self.clear_content_frame()

        # Frame for account settings
        settings_frame = tk.Frame(self.content_frame, bg="#ffffff", padx=20, pady=20)
        settings_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        settings_label = tk.Label(settings_frame, text="Account Settings", font=("Segoe UI", 24, "bold"), bg="#ffffff")
        settings_label.pack(pady=10)

        # Information
        user_info = self.db_manager.get_user_info(self.username)

        tk.Label(settings_frame, text=f"Username: {user_info['username']}", font=("Segoe UI", 14), bg="#ffffff").pack(pady=5)
        tk.Label(settings_frame, text=f"Email: {user_info['email']}", font=("Segoe UI", 14), bg="#ffffff").pack(pady=5)

        # Change email
        email_frame = tk.Frame(settings_frame, bg="#ffffff")
        email_frame.pack(pady=10)
        tk.Label(email_frame, text="Update Email:", font=("Segoe UI", 14), bg="#ffffff").pack(side=tk.LEFT, padx=5)
        self.email_entry = tk.Entry(email_frame, font=("Segoe UI", 14))
        self.email_entry.insert(0, user_info['email'])
        self.email_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(email_frame, text="Update", font=("Segoe UI", 12), command=self.update_email).pack(side=tk.LEFT, padx=5)

        # Change password
        password_frame = tk.Frame(settings_frame, bg="#ffffff")
        password_frame.pack(pady=10)
        tk.Label(password_frame, text="New Password:", font=("Segoe UI", 14), bg="#ffffff").pack(side=tk.LEFT, padx=5)
        self.password_entry = tk.Entry(password_frame, font=("Segoe UI", 14), show="*")
        self.password_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(password_frame, text="Update", font=("Segoe UI", 12), command=self.update_password).pack(side=tk.LEFT, padx=5)

    def update_email(self):
        new_email = self.email_entry.get()
        if not new_email:
            messagebox.showerror("Error", "Email cannot be empty.")
            return
        self.db_manager.update_email(self.username, new_email)
        messagebox.showinfo("Success", "Email updated successfully.")

    def update_password(self):
        new_password = self.password_entry.get()
        if not new_password:
            messagebox.showerror("Error", "Password cannot be empty.")
            return
        self.db_manager.update_password(self.username, new_password)
        messagebox.showinfo("Success", "Password updated successfully.")

    def view_pigeons(self):
        self.clear_content_frame()

        # Frame for pigeon management
        pigeon_frame = tk.Frame(self.content_frame)
        pigeon_frame.pack(fill=tk.BOTH, expand=True)

        pigeon_label = tk.Label(pigeon_frame, text="Available Pigeons", font=("Segoe UI", 20))
        pigeon_label.pack(pady=10)

        # Table for pigeons
        self.pigeon_treeview = ttk.Treeview(pigeon_frame, columns=("ID", "Color", "RingBand", "BloodLine", "Price", "Gender", "RegisteredBy"), show="headings",height=15)
        self.pigeon_treeview.heading("ID", text="ID")
        self.pigeon_treeview.heading("Color", text="Color")
        self.pigeon_treeview.heading("RingBand", text="RingBand")
        self.pigeon_treeview.heading("BloodLine", text="BloodLine")
        self.pigeon_treeview.heading("Price", text="Price")
        self.pigeon_treeview.heading("Gender", text="Gender")
        self.pigeon_treeview.heading("RegisteredBy", text="Registered By")
        
        self.pigeon_treeview.column("ID", width=50, anchor=tk.CENTER, stretch=tk.YES)
        self.pigeon_treeview.column("Color", width=120, anchor=tk.W, stretch=tk.YES)
        self.pigeon_treeview.column("RingBand", width=120, anchor=tk.W, stretch=tk.YES)
        self.pigeon_treeview.column("BloodLine", width=150, anchor=tk.W, stretch=tk.YES)
        self.pigeon_treeview.column("Price", width=100, anchor=tk.CENTER, stretch=tk.YES)
        self.pigeon_treeview.column("Gender", width=100, anchor=tk.CENTER, stretch=tk.YES)
        self.pigeon_treeview.column("RegisteredBy", width=100, anchor=tk.CENTER, stretch=tk.YES)
        
        self.pigeon_treeview.pack(fill=tk.BOTH, expand=True, pady=10)

        # Button to buy pigeon
        self.buy_button = tk.Button(
            pigeon_frame, text="Buy Selected Pigeon", font=("Segoe UI", 16), bg="#006666", fg="white", command=self.buy_pigeon
        )
        self.buy_button.pack(pady=20)

        self.load_pigeons()

    def buy_pigeon(self):
        # Get selected pigeon
        selected_item = self.pigeon_treeview.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a pigeon to buy.")
            return

        pigeon_data = self.pigeon_treeview.item(selected_item, "values")
        pigeon_id = pigeon_data[0]

        # Confirm purchase
        confirm = messagebox.askyesno("Confirm Purchase", f"Are you sure you want to buy pigeon ID {pigeon_id}?")
        if confirm:
            # Remove pigeon from database
            self.db_manager.delete_pigeon(pigeon_id)
            # Refresh the pigeon list
            self.load_pigeons()
            messagebox.showinfo("Success", "Pigeon purchased successfully.")

    def load_pigeons(self):
        # Clear previous data
        for row in self.pigeon_treeview.get_children():
            self.pigeon_treeview.delete(row)

        # Fetch and display pigeons
        pigeons = self.db_manager.get_all_pigeons()
        for pigeon in pigeons:
            self.pigeon_treeview.insert("", "end", values=pigeon)

    def register_pigeon(self):
        self.clear_content_frame()

        # Frame for registering a pigeon
        register_frame = tk.Frame(self.content_frame, bg="#ffffff", padx=20, pady=20)
        register_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        register_label = tk.Label(register_frame, text="Sell a New Pigeon", font=("Segoe UI", 24, "bold"), bg="#ffffff")
        register_label.pack(pady=10)

        # Input Fields
        input_fields_frame = tk.Frame(register_frame, bg="#ffffff")
        input_fields_frame.pack(pady=10)

        def create_input_field(frame, label_text):
            field_frame = tk.Frame(frame, bg="#ffffff")
            field_frame.pack(fill=tk.X, pady=5)
            tk.Label(field_frame, text=label_text, font=("Segoe UI", 14), bg="#ffffff").pack(side=tk.LEFT, padx=5)
            entry = tk.Entry(field_frame, font=("Segoe UI", 14))
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            return entry

        self.color_entry = create_input_field(input_fields_frame, "Color:")
        self.ringband_entry = create_input_field(input_fields_frame, "Ring Band:")
        self.bloodline_entry = create_input_field(input_fields_frame, "Blood Line:")
        self.price_entry = create_input_field(input_fields_frame, "Price:")
        self.gender_entry = create_input_field(input_fields_frame, "Gender:")

        # Register Button
        self.register_button = tk.Button(
            register_frame,
            text="Sell Pigeon",
            font=("Segoe UI", 16, "bold"),
            bg="#006666",
            fg="white",
            command=self.save_pigeon
        )
        self.register_button.pack(pady=20)

    def save_pigeon(self):
        color = self.color_entry.get()
        ringband = self.ringband_entry.get()
        bloodline = self.bloodline_entry.get()
        price = self.price_entry.get()
        gender = self.gender_entry.get()
        registeredby = self.username  # Use the current username for registration
        
        if self.username == "admin":
            registeredby = "admin"
        else:
            registeredby = self.username

        # Add pigeon to the database
        self.db_manager.add_pigeon(color, ringband, bloodline, price, gender, registeredby)

        # Clear the input fields
        self.color_entry.delete(0, tk.END)
        self.ringband_entry.delete(0, tk.END)
        self.bloodline_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.gender_entry.delete(0, tk.END)

        # Refresh the pigeon list
        self.view_pigeons()
        

    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm: 
            self.root.destroy()  
        from Login import Login  # Ensure Login is correctly imported
        login = Login(self.db_manager)  # Pass only db_manager
        self.destroy()  # Close the current SignUpView window (optional)
        login.mainloop()


    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()  # Clear the current content in the content frame

class DatabaseManager:
    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_pigeons_table()
        self.create_users_table()

    def create_pigeons_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pigeons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                color TEXT NOT NULL,
                ringband TEXT NULL,
                bloodline TEXT NULL,
                price TEXT NOT NULL,
                gender TEXT NOT NULL,
                registeredby TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def create_users_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def get_all_pigeons(self):
        self.cursor.execute("SELECT * FROM pigeons")
        pigeons = self.cursor.fetchall()
        return pigeons

    def add_pigeon(self, color, ringband, bloodline, price, gender, registeredby):
        self.cursor.execute("INSERT INTO pigeons (color, ringband, bloodline, price, gender, registeredby) VALUES (?, ?, ?, ?, ?, ?)", (color, ringband, bloodline, price, gender, registeredby))
        self.conn.commit()

    def delete_pigeon(self, pigeon_id):
        self.cursor.execute("DELETE FROM pigeons WHERE id = ?", (pigeon_id,))
        self.conn.commit()

    def update_email(self, username, new_email):
        self.cursor.execute("UPDATE users SET email = ? WHERE username = ?", (new_email, username))
        self.conn.commit()

    def update_password(self, username, new_password):
        self.cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
        self.conn.commit()

    def get_user_info(self, username):
        self.cursor.execute("SELECT username, email FROM users WHERE username = ?", (username,))
        user = self.cursor.fetchone()
        return {"username": user[0], "email": user[1]} if user else {}

    def close(self):
        self.conn.close()
