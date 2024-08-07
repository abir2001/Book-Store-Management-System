from db import get_connection  # Importing the function to establish a database connection

class Order:
    def __init__(self, username, cart, total):
        # Constructor to initialize an Order object with username, cart, and total amount.
        """
        Parameters: username (str): The username associated with the order.
            cart (list): A list of tuples containing book ID and quantity for each item in the cart.
            total (float): The total amount of the order.
        """

        self.username = username
        self.cart = cart
        self.total = total

    def place_order(self):
        # Method to place an order
        conn = get_connection()  # Establishing a database connection
        cursor = conn.cursor()

        # Inserting the order into the 'orders' table and retrieving the order ID
        cursor.execute("INSERT INTO orders (username, total) VALUES (%s, %s)", (self.username, self.total),)
        order_id = cursor.lastrowid

        # Inserting each item from the cart into the 'order_items' table
        # Updating the quantity of each book in the 'books' table
        for book_id, quantity in self.cart:
            cursor.execute("INSERT INTO order_items (order_id, book_id, quantity) VALUES (%s, %s, %s)", (order_id, book_id, quantity),)
            cursor.execute("UPDATE books SET quantity = quantity - %s WHERE id = %s", (quantity, book_id),)

        # Deleting the items from the cart and ordered items list once the order is placed
        cursor.execute("DELETE FROM cart_items WHERE username = %s", (self.username,))
        cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))
        conn.commit()  # Committing the transaction
        conn.close()  # Closing the database connection