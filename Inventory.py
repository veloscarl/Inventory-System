import csv  # Add this line to import the CSV module

class Inventory:
    def __init__(self, filename):
        self.filename = filename
        self.items = []
        self.load_inventory()

    def load_inventory(self):
        try:
            with open(self.filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                self.items = [row for row in reader]
        except FileNotFoundError:
            self.items = []

    def save_inventory(self):
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.items)

    def add_product(self, product_name, product_id, quantity, price):
        self.items.append([product_name, product_id, quantity, price])
        self.save_inventory()
        return f"{product_name} added to inventory."

    def update_quantity(self, product_id, quantity):
        for item in self.items:
            if item[1] == product_id:
                item[2] = str(int(item[2]) + quantity)
                self.save_inventory()
                return f"Updated {item[0]} quantity to {item[2]}."
        return f"Product with ID {product_id} not found."

    def remove_product(self, product_id):
        self.items = [item for item in self.items if item[1] != product_id]
        self.save_inventory()
        return f"Product with ID {product_id} removed from inventory."

    def display_inventory(self):
        return self.items
