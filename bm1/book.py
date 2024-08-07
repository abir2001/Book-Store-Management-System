from db import get_connection  # Importing get_connection function from db module

class Book:
    def __init__(self, id, title, author, price, quantity, category):
        # Constructor to initialize a Book object with provided attributes
        self.id = id  # Unique identifier for the book
        self.title = title  # Title of the book
        self.author = author  # Author of the book
        self.price = price  # Price of the book
        self.quantity = quantity  # Quantity of the book available in stock
        self.category = category  # Category of the book

    def __str__(self):
        # String representation of the Book object
        return f"{self.id} : {self.title} by {self.author} - Rs{self.price} ({self.quantity} in stock, Category: {self.category})"

    def update(self, title=None, author=None, price=None, quantity=None, category=None):
        # Method to update the attributes of the book
        if title:
            self.title = title  # Update title if provided
        if author:
            self.author = author  # Update author if provided
        if price:
            self.price = float(price)  # Update price if provided
        if quantity:
            self.quantity = int(quantity)  # Update quantity if provided
        if category:
            self.category = category  # Update category if provided

    def save(self):
        # Method to save the book to the database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, price, quantity, category) VALUES (%s, %s, %s, %s, %s)", (self.title, self.author, self.price, self.quantity, self.category))
        conn.commit()
        conn.close()