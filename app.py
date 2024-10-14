import csv
import hashlib
import os
import tkinter as tk
from tkinter import messagebox, ttk

# User Authentication Class
class UserAuth:
    def __init__(self, users_file):
        self.users_file = users_file

    def sign_up(self, username, password):
        # Hash password for security
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Check if username already exists
        if self.check_user_exists(username):
            return False, "Username already exists."

        # Write new user to file
        with open(self.users_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username, hashed_password])
        return True, "Sign up successful."

    def log_in(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Read users file and check credentials
        with open(self.users_file, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username and row[1] == hashed_password:
                    return True, "Login successful."
        return False, "Invalid username or password."

    def check_user_exists(self, username):
        # Check if username already exists in file
        if not os.path.exists(self.users_file):
            return False  # File doesn't exist, so no users exist
        
        with open(self.users_file, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username:
                    return True
        return False

# Inventory Management Class
class Inventory:
    def __init__(self, inventory_file):
        self.inventory_file = inventory_file
        # Create inventory file if it does not exist
        if not os.path.exists(self.inventory_file):
            with open(self.inventory_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "ID", "Quantity", "Cost"])  # Header

    def add_product(self, name, product_id, quantity, cost):
        with open(self.inventory_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, product_id, quantity, cost])
        return f"Product '{name}' added successfully."

    def update_quantity(self, product_id, new_quantity):
        updated = False
        rows = []

        # Read current inventory and update the quantity
        with open(self.inventory_file, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == product_id:
                    row[2] = str(new_quantity)  # Update quantity
                    updated = True
                rows.append(row)

        # Write the updated inventory back to file
        with open(self.inventory_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        if updated:
            return f"Quantity for product ID '{product_id}' updated."
        else:
            return f"Product ID '{product_id}' not found."

    def remove_product(self, product_id):
        removed = False
        rows = []

        # Read current inventory and remove the product
        with open(self.inventory_file, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] != product_id:
                    rows.append(row)
                else:
                    removed = True

        # Write the updated inventory back to file
        with open(self.inventory_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        if removed:
            return f"Product ID '{product_id}' removed."
        else:
            return f"Product ID '{product_id}' not found."

    def view_inventory(self):
        inventory_data = []

        # Read inventory file
        if not os.path.exists(self.inventory_file):
            return inventory_data  # Return empty if file does not exist

        with open(self.inventory_file, mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                product = {
                    "name": row[0],
                    "id": row[1],
                    "quantity": row[2],
                    "cost": row[3]
                }
                inventory_data.append(product)
        return inventory_data

# Main App Class
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.auth = UserAuth("users.csv")
        self.user = None
        self.inventory = None

        # Configure grid for responsive layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Create professional login interface
        self.create_login_ui()

    def create_login_ui(self):
        self.clear_window()

        title_label = tk.Label(self.root, text="Welcome to Inventory Management System", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        form_frame = tk.Frame(self.root, padx=10, pady=10)
        form_frame.grid(row=1, column=0, columnspan=2, pady=10)

        tk.Label(form_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.username_entry = tk.Entry(form_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.password_entry = tk.Entry(form_frame, show='*')
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        button_frame = tk.Frame(self.root, padx=10, pady=10)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="Log In", command=self.login, width=12, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Sign Up", command=self.sign_up, width=12, bg="#2196F3", fg="white").grid(row=0, column=1, padx=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message = self.auth.log_in(username, password)
        if success:
            self.user = username
            self.inventory = Inventory(f'{username}_inventory.csv')
            messagebox.showinfo("Login Successful", message)
            self.create_inventory_ui()
        else:
            messagebox.showerror("Login Failed", message)

    def sign_up(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message = self.auth.sign_up(username, password)
        if success:
            messagebox.showinfo("Sign Up Successful", message)
        else:
            messagebox.showerror("Sign Up Failed", message)

    def create_inventory_ui(self):
        self.clear_window()

        # Inventory management layout
        title_label = tk.Label(self.root, text="Inventory Management", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=10)

        tk.Button(self.root, text="Add Product", command=self.add_product_ui, width=12, bg="#FFC107").grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Update Quantity", command=self.update_quantity_ui, width=12, bg="#FFC107").grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Remove Product", command=self.remove_product_ui, width=12, bg="#F44336", fg="white").grid(row=1, column=2, padx=10, pady=10)
        tk.Button(self.root, text="View Inventory", command=self.view_inventory_ui, width=12, bg="#03A9F4", fg="white").grid(row=1, column=3, padx=10, pady=10)

    def add_product_ui(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Product")

        form_frame = tk.Frame(add_window, padx=20, pady=20)
        form_frame.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(form_frame, text="Product Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        product_name_entry = tk.Entry(form_frame)
        product_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Product ID:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        product_id_entry = tk.Entry(form_frame)
        product_id_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Quantity:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        quantity_entry = tk.Entry(form_frame)
        quantity_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Cost:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        cost_entry = tk.Entry(form_frame)
        cost_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(add_window, text="Add Product", command=lambda: self.add_product(product_name_entry.get(), product_id_entry.get(), quantity_entry.get(), cost_entry.get()), bg="#4CAF50", fg="white").grid(row=1, column=0, padx=10, pady=10)

    def add_product(self, name, product_id, quantity, cost):
        if quantity.isdigit() and cost.replace('.', '', 1).isdigit():  # Check for numeric values
            message = self.inventory.add_product(name, product_id, int(quantity), float(cost))
            messagebox.showinfo("Add Product", message)
        else:
            messagebox.showerror("Input Error", "Please enter valid numeric values for quantity and cost.")

    def update_quantity_ui(self):
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Quantity")

        form_frame = tk.Frame(update_window, padx=20, pady=20)
        form_frame.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(form_frame, text="Product ID:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        product_id_entry = tk.Entry(form_frame)
        product_id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="New Quantity:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        new_quantity_entry = tk.Entry(form_frame)
        new_quantity_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(update_window, text="Update Quantity", command=lambda: self.update_quantity(product_id_entry.get(), new_quantity_entry.get()), bg="#FFC107").grid(row=2, column=0, padx=10, pady=10)

    def update_quantity(self, product_id, new_quantity):
        if new_quantity.isdigit():
            message = self.inventory.update_quantity(product_id, int(new_quantity))
            messagebox.showinfo("Update Quantity", message)
        else:
            messagebox.showerror("Input Error", "Please enter a valid numeric value for quantity.")

    def remove_product_ui(self):
        remove_window = tk.Toplevel(self.root)
        remove_window.title("Remove Product")

        form_frame = tk.Frame(remove_window, padx=20, pady=20)
        form_frame.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(form_frame, text="Product ID:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        product_id_entry = tk.Entry(form_frame)
        product_id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(remove_window, text="Remove Product", command=lambda: self.remove_product(product_id_entry.get()), bg="#F44336", fg="white").grid(row=1, column=0, padx=10, pady=10)

    def remove_product(self, product_id):
        message = self.inventory.remove_product(product_id)
        messagebox.showinfo("Remove Product", message)

    def view_inventory_ui(self):
        inventory_window = tk.Toplevel(self.root)
        inventory_window.title("View Inventory")

        inventory_data = self.inventory.view_inventory()

        if not inventory_data:
            messagebox.showinfo("Inventory", "No products in inventory.")
            return

        tree = ttk.Treeview(inventory_window, columns=("Name", "ID", "Quantity", "Cost"), show='headings')
        tree.heading("Name", text="Product Name")
        tree.heading("ID", text="Product ID")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Cost", text="Cost")
        
        # Add data to the tree
        for item in inventory_data:
            tree.insert("", tk.END, values=(item['name'], item['id'], item['quantity'], item['cost']))

        tree.pack(expand=True, fill='both')

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
