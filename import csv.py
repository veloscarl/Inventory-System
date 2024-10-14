import csv  # Add this line
import hashlib
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

class UserAuth:
    def __init__(self, user_file):
        self.user_file = user_file
        self.users = self.load_users()

    def load_users(self):
        try:
            with open(self.user_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                return {rows[0]: rows[1] for rows in reader}  # username: hashed password
        except FileNotFoundError:
            return {}

    def save_users(self):
        with open(self.user_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            for username, password in self.users.items():
                writer.writerow([username, password])

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def sign_up(self, username, password):
        if username in self.users:
            return False, "Username already exists."
        self.users[username] = self.hash_password(password)
        self.save_users()
        return True, "Sign-up successful."

    def log_in(self, username, password):
        hashed_password = self.hash_password(password)
        if username in self.users and self.users[username] == hashed_password:
            return True, f"Welcome, {username}!"
        return False, "Invalid username or password."
