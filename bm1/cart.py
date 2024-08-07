from db import get_connection  # Importing the function to establish a database connection

class Cart:
    def __init__(self, username):
        # Constructor to initialize a Cart object with a username.
        # Parameters: username (str): The username associated with the cart.
        self.username = username

    def add_item(self, book_id, quantity):
        # Method to add an item to the cart or update its quantity if it already exists.
        """
        Parameters:
            book_id (int): The ID of the book to be added to the cart.
            quantity (int): The quantity of the book to be added to the cart.
        """
        conn = get_connection()  # Establishing a database connection
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cart_items (username, book_id, quantity) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity)", (self.username, book_id, quantity),)  # Executing SQL query to add or update the item in the cart
        conn.commit()  # Committing the transaction
        conn.close()  # Closing the database connection

    def view_cart(self):
        # Method to retrieve the items in the cart
        # Returns: list: A list of tuples containing book ID and quantity of each item in the cart

        conn = get_connection()  # Establishing a database connection
        cursor = conn.cursor()
        cursor.execute("SELECT book_id, quantity FROM cart_items WHERE username = %s", (self.username,),)  # Retrieving items from the cart for the specified username
        items = cursor.fetchall()  # Fetching all items from the cart
        conn.close()  # Closing the database connection
        return items  # Returning the list of items in the cart

    def clear_cart(self):
        # Method to clear the items in the cart.
        conn = get_connection()  # Establishing a database connection
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart_items WHERE username = %s", (self.username,))  # Deleting all items from the cart for the specified username
        conn.commit()  # Committing the transaction
        conn.close()  # Closing the database connection