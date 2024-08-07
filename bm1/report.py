import mysql.connector  # Importing MySQL connector module
from db import get_connection  # Importing the function to establish a database connection
from prettytable import PrettyTable  # Importing PrettyTable for generating tabular reports

class Report:
    def __init__(self):
        # Constructor for the Report class
        pass

    def generate_sales_report(self):
        # Method to generate a sales report

        try:
            conn = get_connection()  # Establishing a database connection
            cursor = conn.cursor()

            # Fetching orders data from the 'orders' table
            cursor.execute("SELECT orders.id, users.username, orders.total, orders.order_date FROM orders JOIN users ON orders.username = users.username")
            orders = cursor.fetchall()

            # Query to fetch the number of ordersand their total value per day
            cursor.execute("""SELECT DATE(order_date) as order_date, COUNT(*) as total_orders, SUM(total) as total_value FROM orders GROUP BY DATE(order_date)""")
            daily_summary = cursor.fetchall()

            conn.close()  # Closing the database connection

            if not orders:
                print("No sales data available\n")
                return

            # Creating a PrettyTable for displaying the sales report
            table = PrettyTable()
            table.field_names = ["Orders ID", "Username", "Total Price", "Order Date"]

            # Adding each order to the table
            for order in orders:
                table.add_row(order[:4])

            # Printing the sales report
            print("\nSales Report :")
            print(table)

            # Create the table for daily summary
            summary_table = PrettyTable()
            summary_table.field_names = ["Orders Date", "Total Orders", "Total Value"]

            for summary in daily_summary:
                summary_table.add_row(summary)

            print("\nDaily Summary Report :")
            print(summary_table)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def generate_inventory_report(self):
        # Method to generate an inventory report
        try:
            conn = get_connection()  # Establishing a database connection
            cursor = conn.cursor()

            # Fetching books data from the 'books' table
            cursor.execute("SELECT books.id, books.title, books.author, books.price, books.quantity, books.category FROM books")
            books = cursor.fetchall()

            cursor.execute("SELECT SUM(price * quantity) FROM books")
            total_value = cursor.fetchone()[0]

            conn.close()  # Closing the database connection

            if not books:
                print("No inventory data available\n")
                return

            # Creating a PrettyTable for displaying the inventory report
            table = PrettyTable()
            table.field_names = ["Books ID", "Title", "Author", "Price", "Quantity", "Category",]

            # Adding each book to the table
            for book in books:
                table.add_row(book)

            # Printing the inventory report
            print("\nInventory Report :")
            print(table)

            print(f"\nTotal Inventory Value : Rs {total_value:.2f}")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def generate_user_report(self):
        # Method to generate a user report
        try:
            conn = get_connection()  # Establishing a database connection
            cursor = conn.cursor()

            # Fetching users data from the 'users' table
            cursor.execute("SELECT users.username, COUNT(orders.id) as order_count FROM users LEFT JOIN orders ON users.username = orders.username GROUP BY users.username")
            activities = cursor.fetchall()
            conn.close()  # Closing the database connection

            if not activities:
                print("No user activity data available\n")
                return

            # Creating a PrettyTable for displaying the user report
            table = PrettyTable()
            table.field_names = ["Username", "Orders Placed"]

            # Adding each user to the table
            for activity in activities:
                table.add_row(activity)

            # Printing the user report
            print("\nUsers Report :")
            print(table)

        except mysql.connector.Error as err:
            print(f"Error: {err}")