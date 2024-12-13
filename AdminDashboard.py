import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard - Pigeon Selling Management")
        self.root.geometry('1200x800')

        self.db_manager = DatabaseManager()  # Connect to the database
        self.create_widgets()

    def create_widgets(self):
        # Header
        self.header_frame = tk.Frame(self.root, bg="#006666", height=100)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)

        self.header_label = tk.Label(
            self.header_frame,
            text="Admin Dashboard",
            font=("Segoe UI", 28, "bold"),
            fg="white",
            bg="#006666"
        )
        self.header_label.pack(pady=20)

        # Menu (Sidebar)
        self.menu_frame = tk.Frame(self.root, bg="white", width=200)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.admin_label = tk.Label(
            self.menu_frame,
            text="Welcome, Admin",
            font=("Segoe UI", 18, "bold")
        )
        self.admin_label.pack(pady=20)

        self.manage_users_button = self.create_menu_button("Manage Users", self.manage_users)
        self.manage_pigeons_button = self.create_menu_button("Manage Pigeons", self.manage_pigeons)
        self.logout_button = self.create_menu_button("Logout", self.logout)

        # Content panel (dynamically changing)
        self.content_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.content_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

        self.content_label = tk.Label(
            self.content_frame,
            text="Welcome Kalapatids",
            font=("Segoe UI", 20)
        )
        self.content_label.pack(pady=50)

    def create_menu_button(self, text, command):
        button = tk.Button(self.menu_frame, text=text, font=("Segoe UI", 16), bg="#006666", fg="white", width=20, command=command)
        button.pack(pady=10)
        return button

    def manage_users(self):
        self.clear_content_frame()

        # Frame for user management
        user_frame = tk.Frame(self.content_frame)
        user_frame.pack(fill=tk.BOTH, expand=True)

        user_label = tk.Label(user_frame, text="Manage Users", font=("Segoe UI", 20))
        user_label.pack(pady=10)

        # Table for users
        self.treeview = ttk.Treeview(
        user_frame, 
        columns=("ID", "Username", "Email", "Age", "Password"), 
        show="headings"
    )
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("Username", text="Username")
        self.treeview.heading("Email", text="Email")
        self.treeview.heading("Age", text="Age")
        self.treeview.heading("Password", text="Password")

    # Adjusting column widths and enabling stretch
        self.treeview.column("ID", width=50, anchor=tk.CENTER, stretch=tk.YES)
        self.treeview.column("Username", width=150, anchor=tk.W, stretch=tk.YES)
        self.treeview.column("Email", width=200, anchor=tk.W, stretch=tk.YES)
        self.treeview.column("Age", width=80, anchor=tk.CENTER, stretch=tk.YES)
        self.treeview.column("Password", width=150, anchor=tk.W, stretch=tk.YES)

        self.treeview.pack(fill=tk.BOTH, expand=True, pady=10)

        self.load_users()

        # Buttons for user management
        button_frame = tk.Frame(user_frame)
        button_frame.pack(pady=10)

        add_button = tk.Button(button_frame, text="Add User", command=lambda: self.open_form("Add User", "User"))
        add_button.pack(side=tk.LEFT, padx=5)

        edit_button = tk.Button(button_frame, text="Edit User", command=self.edit_user)
        edit_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(button_frame, text="Delete User", command=self.delete_user)
        delete_button.pack(side=tk.LEFT, padx=5)

    def load_users(self):
        # Clear previous data
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        # Fetch and display users
        users = self.db_manager.get_all_users()
        for user in users:
            self.treeview.insert("", "end", values=user)

    def edit_user(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a user to edit.")
            return

        # Get the selected user's data
        user_data = self.treeview.item(selected_item, "values")
        self.open_form("Edit User", "User", data=user_data)

    def manage_pigeons(self):
        self.clear_content_frame()

        # Frame for pigeon management
        pigeon_frame = tk.Frame(self.content_frame)
        pigeon_frame.pack(fill=tk.BOTH, expand=True)

        pigeon_label = tk.Label(pigeon_frame, text="Manage Pigeons", font=("Segoe UI", 20))
        pigeon_label.pack(pady=10)

        # Table for pigeons
        self.pigeon_treeview = ttk.Treeview(
    pigeon_frame, 
    columns=("ID", "Color", "RingBand", "BloodLine", "Price", "Gender"), 
    show="headings",
    height=15
)
        self.pigeon_treeview.heading("ID", text="ID")
        self.pigeon_treeview.heading("Color", text="Color")
        self.pigeon_treeview.heading("RingBand", text="RingBand")
        self.pigeon_treeview.heading("BloodLine", text="BloodLine")
        self.pigeon_treeview.heading("Price", text="Price")
        self.pigeon_treeview.heading("Gender", text="Gender")

        # Adjusting column widths and enabling stretch
        self.pigeon_treeview.column("ID", width=50, anchor=tk.CENTER, stretch=tk.YES)
        self.pigeon_treeview.column("Color", width=120, anchor=tk.W, stretch=tk.YES)
        self.pigeon_treeview.column("RingBand", width=120, anchor=tk.W, stretch=tk.YES)
        self.pigeon_treeview.column("BloodLine", width=150, anchor=tk.W, stretch=tk.YES)
        self.pigeon_treeview.column("Price", width=100, anchor=tk.CENTER, stretch=tk.YES)
        self.pigeon_treeview.column("Gender", width=100, anchor=tk.CENTER, stretch=tk.YES)

        self.pigeon_treeview.pack(fill=tk.BOTH, expand=True, pady=10)
        self.load_pigeons()

        # Buttons for pigeon management
        button_frame = tk.Frame(pigeon_frame)
        button_frame.pack(pady=10)

        add_button = tk.Button(button_frame, text="Add Pigeon", command=lambda: self.open_form("Add Pigeon", "Pigeon"))
        add_button.pack(side=tk.LEFT, padx=5)


        edit_button = tk.Button(button_frame, text="Edit Pigeon", command=self.edit_pigeon)
        edit_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(button_frame, text="Delete Pigeon", command=self.delete_pigeon)
        delete_button.pack(side=tk.LEFT, padx=5)

    def load_pigeons(self):
        # Clear previous data
        for row in self.pigeon_treeview.get_children():
            self.pigeon_treeview.delete(row)

        # Fetch and display pigeons
        pigeons = self.db_manager.get_all_pigeons()
        for pigeon in pigeons:
            self.pigeon_treeview.insert("", "end", values=pigeon)

     # New edit_pigeon method
    def edit_pigeon(self):
        selected_item = self.pigeon_treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a pigeon to edit.")
            return

        # Get the selected pigeon's data
        pigeon_data = self.pigeon_treeview.item(selected_item, "values")
        self.open_form("Edit Pigeon", "Pigeon", data=pigeon_data)

    def open_form(self, action, entity, data=None):
        form = tk.Toplevel(self.root)
        form.title(f"{action} {entity}")

        if entity == "User":
            tk.Label(form, text="Username:").grid(row=0, column=0, padx=10, pady=5)
            username_entry = tk.Entry(form)
            username_entry.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(form, text="Email:").grid(row=1, column=0, padx=10, pady=5)
            email_entry = tk.Entry(form)
            email_entry.grid(row=1, column=1, padx=10, pady=5)

            tk.Label(form, text="Age:").grid(row=2, column=0, padx=10, pady=5)
            age_entry = tk.Entry(form)
            age_entry.grid(row=2, column=1, padx=10, pady=5)

            tk.Label(form, text="Password:").grid(row=3, column=0, padx=10, pady=5)
            password_entry = tk.Entry(form)
            password_entry.grid(row=3, column=1, padx=10, pady=5)

            if data:
                username_entry.insert(0, data[1])
                email_entry.insert(0, data[2])
                age_entry.insert(0, data[3])
                password_entry.insert(0, data[4])

        elif entity == "Pigeon":
            tk.Label(form, text="Color:").grid(row=0, column=0, padx=10, pady=5)
            color_entry = tk.Entry(form)
            color_entry.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(form, text="RingBand:").grid(row=1, column=0, padx=10, pady=5)
            ringband_entry = tk.Entry(form)
            ringband_entry.grid(row=1, column=1, padx=10, pady=5)

            tk.Label(form, text="BloodLine:").grid(row=2, column=0, padx=10, pady=5)
            bloodline_entry = tk.Entry(form)
            bloodline_entry.grid(row=2, column=1, padx=10, pady=5)

            tk.Label(form, text="Price:").grid(row=3, column=0, padx=10, pady=5)
            price_entry = tk.Entry(form)
            price_entry.grid(row=3, column=1, padx=10, pady=5)

            tk.Label(form, text="Gender:").grid(row=4, column=0, padx=10, pady=5)
            gender_var = tk.StringVar()
            gender_dropdown = ttk.Combobox(form, textvariable=gender_var, values=["Male", "Female"])
            gender_dropdown.grid(row=4, column=1, padx=10, pady=5)

            if data:
                color_entry.insert(0, data[1])
                ringband_entry.insert(0, data[2])
                bloodline_entry.insert(0, data[3])
                price_entry.insert(0, data[4])
                gender_var.set(data[5])

        tk.Button(
            form, text="Save", command=lambda: self.save(action, entity, form, data)
        ).grid(row=5, column=0, columnspan=2, pady=10)

    def save(self, action, entity, form, data=None):
        if entity == "User":
            username = form.winfo_children()[1].get()
            email = form.winfo_children()[3].get()
            age = form.winfo_children()[5].get()
            password = form.winfo_children()[7].get()

            if action == "Add User":
                self.db_manager.add_user(username, email, age, password)
            elif action == "Edit User":
                user_id = data[0]
                self.db_manager.update_user(user_id, username, email, age, password)

            form.destroy()
            self.load_users()
            messagebox.showinfo("Success", f"User {action.lower()}ed successfully.")

        elif entity == "Pigeon":
            color = form.winfo_children()[1].get()
            ringband = form.winfo_children()[3].get()
            bloodline = form.winfo_children()[5].get()
            price = form.winfo_children()[7].get()
            gender = form.winfo_children()[9].get()

            registeredby = "admin"
            if action == "Add Pigeon":
                self.db_manager.add_pigeon(color, ringband, bloodline, price, gender, registeredby)
            elif action == "Edit Pigeon":
                pigeon_id = data[0]
                self.db_manager.update_pigeon(pigeon_id, color, ringband, bloodline, price, gender)

            form.destroy()
            self.load_pigeons()
            messagebox.showinfo("Success", f"Pigeon {action.lower()}ed successfully.")

    def delete_user(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a user to delete.")
            return

        user_id = self.treeview.item(selected_item, "values")[0]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?")
        if confirm:
            self.db_manager.delete_user(user_id)
            self.load_users()
            messagebox.showinfo("Success", "User deleted successfully.")

    def edit_user(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a user to edit.")
            return

            # Get the selected user's data
        user_data = self.treeview.item(selected_item, "values")
        self.open_form("Edit User", "User", data=user_data)

    def delete_pigeon(self):
        selected_item = self.pigeon_treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a pigeon to delete.")
            return

        pigeon_id = self.pigeon_treeview.item(selected_item, "values")[0]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this pigeon?")
        if confirm:
            self.db_manager.delete_pigeon(pigeon_id)
            self.load_pigeons()
            messagebox.showinfo("Success", "Pigeon deleted successfully.")

    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.root.destroy()
            

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()  # Clear the current content in the content frame


class DatabaseManager:
    def __init__(self):
        # SQLite connection setup (assuming the database exists)
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        self.create_pigeons_table()
        
    def create_pigeons_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pigeons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                color TEXT NOT NULL,
                ringband TEXT NULL,
                bloodline TEXT NULL,
                price INTEGER NOT NULL,
                gender TEXT NOT NULL,
                registeredby TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def get_all_pigeons(self):
        self.cursor.execute("SELECT * FROM pigeons")
        return self.cursor.fetchall()

    def add_user(self, username, email, age, password):
        self.cursor.execute(
            "INSERT INTO users (username, email, age, password) VALUES (?, ?, ?, ?)",
            (username, email, age, password)
        )
        self.conn.commit()

    def update_user(self, user_id, username, email, age, password):
        self.cursor.execute(
            "UPDATE users SET username=?, email=?, age=?, password=? WHERE id=?",
            (username, email, age, password, user_id)
        )
        self.conn.commit()

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        self.conn.commit()

    def add_pigeon(self, color, ringband, bloodline, price, gender, registeredby):
        self.cursor.execute(
        "INSERT INTO pigeons (color, ringband, bloodline, price, gender, registeredby) VALUES (?, ?, ?, ?, ?, ?)",
        (color, ringband, bloodline, price, gender, registeredby)
    )
        self.conn.commit()

    def update_pigeon(self, pigeon_id, color, ringband, bloodline, price, gender):
        self.cursor.execute(
            "UPDATE pigeons SET color=?, ringband=?, bloodline=?, price=?, gender=? WHERE id=?",
            (color, ringband, bloodline, price, gender, pigeon_id)
        )
        self.conn.commit()

    def delete_pigeon(self, pigeon_id):
        self.cursor.execute("DELETE FROM pigeons WHERE id=?", (pigeon_id,))
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()

