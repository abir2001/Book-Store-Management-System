import re  # Regular expression module for string matching
import getpass  # Module for securely entering passwords
from book import Book  # Importing Book class from book module
from user import User  # Importing User class from user module
from cart import Cart  # Importing Cart class from cart module
from order import Order  # Importing Order class from order module
from report import Report  # Importing Report class from report module
from db import get_connection  # Importing get_connection function from db module
from prettytable import PrettyTable  # Importing PrettyTable for tabular display

class Bookstore:
    def __init__(self):
        # Initializing Bookstore object
        self.current_user = None  # Initializing current_user attribute to None
        self.cart = Cart(self.current_user)  # Initializing cart attribute with Cart object

    def signup(self):
        # Method for user registration
        while True:
            username = input("Enter username : ")  # Prompting for username input
            if User.get_user(username):  # Checking if username already exists
                print("Username already exists! Please try again with a different username")
            else:
                password = getpass.getpass("Enter password : ")  # Prompting for password input
                role = input("Enter role (user/admin) : ").lower()  # Prompting for role input
                if role == "user":
                    # Registering user
                    print("Role will be registered as a 'user'")
                    role = "user"
                    User.add_user(username, password, role)
                    print(f"User {username} registered successfully!")
                    break
                elif role == "admin":
                    # Registering admin with additional confirmation
                    confedential_code = input("Enter the confidential code to approve the registration as an admin : ")
                    if confedential_code == "admin_access_code":
                        print("Code accepted for the registration as an admin.")
                        print("Role will be registered as an 'admin'")
                        role = "admin"
                        User.add_user(username, password, role)
                        print(f"User {username} registered successfully!")
                        break
                    else:
                        print("Code not accepted for the registration as an admin.")
                        print("Role will be registered as a 'user'")
                        role = "user"
                        User.add_user(username, password, role)
                        print(f"User {username} registered successfully!")
                        break
                elif role not in ["user", "admin"]:
                    # Handling invalid role input
                    print("Invalid role. Assigning default value : 'user'")
                    role = "user"
                    User.add_user(username, password, role)
                    print(f"User {username} registered successfully!")
                    break

    def login(self):
        # Method for user login
        username = input("Enter username : ")  # Prompting for username input
        password = getpass.getpass("Enter password : ")  # Prompting for password input
        conn = get_connection()  # Establishing database connection
        cursor = conn.cursor()
        cursor.execute("SELECT username, password, role FROM users WHERE username = %s", (username,),)
        user_data = cursor.fetchone()  # Fetching user data from database
        conn.close()  # Closing database connection

        if user_data and user_data[1] == password:
            # Validating user credentials
            self.current_user = User(username=user_data[0], password=user_data[1], role=user_data[2])
            print(f"Welcome back, {self.current_user.username}!")
            return True
        else:
            print(f"Invalid username or password. Please try again!")
            return False

    def logout(self):
        # Method for user logout
        self.current_user = None  # Resetting current_user to None
        self.cart = Cart(None)  # Resetting cart to an empty cart
        print("Logged out successfully")

    def browse_books(self):
        # Method to browse available books
        conn = get_connection()  # Establishing database connection
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, price, category FROM books")  # Fetching all books from database
        books = cursor.fetchall()
        conn.close()  # Closing database connection

        table = PrettyTable()
        table.field_names = ["Book ID", "Title", "Author", "Price", "Category",]

        for book in books:
            table.add_row(book)  # Printing book details
 
        print("\nBOOK STORE")
        print(table)

    def search_books(self):
        # Method to search for books by title, author, or category
        try:
            search_term = input("Enter search term (title/author/category) : ").strip()  # Prompting for search term input
            if not search_term:
                print("Search term can not be empty.")
                return

            pattern = re.compile(search_term, re.IGNORECASE)  # Compiling search pattern
            conn = get_connection()  # Establishing database connection
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books")  # Fetching all books from database
            books = cursor.fetchall()

            table = PrettyTable()
            table.field_names = ["Book ID", "Title", "Author", "Price", "Category",]

            for book in books:
                # Searching for books matching the search term
                book_obj = Book(*book)
                if (pattern.search(book_obj.title) or pattern.search(book_obj.author) or pattern.search(book_obj.category)):
                    table.add_row([book_obj.id, book_obj.title, book_obj.author, book_obj.price, book_obj.category])
            
            if table.rows:
                print("\nSearch Results :")
                print(table)
            else:
                print("No matching books found!")

            conn.close()  # Closing database connection
        except Exception as e:
            print(f"An error occurred : {e}")

    def filter_books(self):
        # Method to filter books by price range
        min_price = float(input("Enter minimum price : "))  # Prompting for minimum price input
        max_price = float(input("Enter maximum price : "))  # Prompting for maximum price input
        while True:
            if min_price > max_price:
                print("Minimum price specified is more than the maximum price specified. Please try again.")
            else:
                break
            break
        conn = get_connection()  # Establishing database connection
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE price BETWEEN %s AND %s", (min_price, max_price))  # Fetching books within the specified price range
        books = cursor.fetchall()

        table = PrettyTable()
        table.field_names = ["Book ID", "Title", "Author", "Price", "Category",]

        for book in books:
            book_obj = Book(*book)
            table.add_row([book_obj.id, book_obj.title, book_obj.author, book_obj.price, book_obj.category])

        if table.rows:
            print("\nFiltered Results :")
            print(table)
        else:
            print("No matching books found!")
        conn.close()  # Closing database connection

    def add_to_cart(self):
        # Method to add a book to the cart
        if self.current_user is None:
            print("You need to login first!")
            return
        try:
            book_id = int(input("Enter book ID to add to cart : "))  # Prompting for book ID input
            
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT quantity FROM books WHERE id = %s", (book_id,))
            result = cursor.fetchone()

            if result is None:
                print("Book not found. Please try again!")
                return
            available_quantity = result[0]
            while True:
                quantity = int(input("Enter the quantity : "))
                if quantity > available_quantity:
                    print(f"Only {available_quantity} books available in the stock. Please enter the quantity equal to or less than the available books.")
                else:
                    break
            cart = Cart(self.current_user.username)  # Creating cart object
            cart.add_item(book_id, quantity)
            conn.close()
            print(f"{quantity} books with book ID {book_id} added to the cart.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred : {e}")

    def view_cart(self):
        # Method to view the contents of the cart
        if self.current_user is None:
            print("You need to login first!")
            return
        cart = Cart(self.current_user.username)  # Creating cart object
        items = cart.view_cart()  # Retrieving cart items
        if not items:
            print("Your cart is empty.")
        else:
            for book_id, quantity in items:
                print(f"Book ID -> {book_id} : Quantity -> {quantity}")

    def clear_cart(self):
        Cart.clear_cart(self.current_user)
        print("Your cart has been cleared successfully!")

    def checkout(self):
        # Method to checkout and place an order
        if self.current_user is None:
            print("You need to login first!")
            return
        cart = Cart(self.current_user.username)  # Creating cart object
        items = cart.view_cart()  # Retrieving cart items
        if not items:
            print("Your cart is empty.")
            return
        total = sum(self.get_book_price(book_id) * quantity for book_id, quantity in items)  # Calculating total amount
        order = Order(self.current_user.username, items, total)  # Creating order object
        order.place_order()  # Placing the order
        print(f"Order placed successfully! Total amount : Rs{total}")

    def get_book_price(self, book_id):
        # Method to retrieve the price of a book
        conn = get_connection()  # Establishing database connection
        cursor = conn.cursor()
        cursor.execute("SELECT price FROM books WHERE id = %s", (book_id,))
        price = cursor.fetchone()[0]  # Fetching book price
        conn.close()  # Closing database connection
        return price

    def add_book(self):
        # Method to add a new book to the database
        if self.current_user.role != "admin":
            print("Admin access required")
            return
        title = input("Enter book title : ").title()  # Prompting for book title input
        author = input("Enter book author : ").title()  # Prompting for book author input
        price = input("Enter book price : ")  # Prompting for book price input
        quantity = input("Enter book quantity : ")  # Prompting for book quantity input
        category = input("Enter book category : ").title()  # Prompting for book category input
        conn = get_connection()  # Establishing database connection
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, price, quantity, category) VALUES (%s, %s, %s, %s, %s)", (title, author, price, quantity, category),)  # Inserting new book into the database
        conn.commit()  # Committing changes
        conn.close()  # Closing database connection
        print(f"Book '{title}' added successfully!")

    def update_book(self):
        # Method to update an existing book in the database
        if self.current_user.role != "admin":
            print("Admin access required")
            return
        book_id = int(input("Enter book ID to update : "))  # Prompting for book ID input
        conn = get_connection()  # Establishing database connection
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()
        if not book:
            print("Invalid book ID")
            conn.close()
            return
        book_obj = Book(*book)
        title = (input("Enter new title (Leave this field blank to keep the value same) : ") or book_obj.title).title()  # Prompting for new title input
        author = (input("Enter new author (Leave this field blank to keep the value same) : ") or book_obj.author).title()  # Prompting for new author input
        price = (input("Enter new price (Leave this field blank to keep the value same) : ") or book_obj.price)  # Prompting for new price input
        quantity = (input("Enter new quantity (Leave this field blank to keep the value same) : ") or book_obj.quantity)  # Prompting for new quantity input
        category = (input("Enter new category (Leave this field blank to keep the value same) : ") or book_obj.category).title()  # Prompting for new category input
        cursor.execute("UPDATE books SET title = %s, author = %s, price = %s, quantity = %s, category = %s WHERE id = %s", (title, author, price, quantity, category, book_id),)  # Updating book in the database
        conn.commit()  # Committing changes
        conn.close()  # Closing database connection
        print("Book updated successfully!")

    def delete_book(self):
        # Method to delete a book from the database
        if self.current_user.role != "admin":
            print("Admin access required")
            return
        book_id = int(input("Enter the book ID to delete : "))  # Prompting for book ID input
        conn = get_connection()  # Establishing database connection
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
        if cursor.rowcount == 0:
            print("No book found with the provided ID")
        else:
            conn.commit()  # Committing changes
            print("Book deleted successfully!")
        conn.close()  # Closing database connection

    def generate_reports(self):
        # Method to generate various types of reports
        if self.current_user.role != "admin":
            print("Admin access required")
            return
        report_type = input("Enter report type (sales/inventory/user) : ")  # Prompting for report type input
        report = Report()
        if report_type == "sales":
            report.generate_sales_report()  # Generating sales report
        elif report_type == "inventory":
            report.generate_inventory_report()  # Generating inventory report
        elif report_type == "user":
            report.generate_user_report()  # Generating user report
        else:
            print("Invalid report type")

    def login_user(self, username, password):
        user = User.get_user(username)
        if user and user.authenticate(password):
            self.current_user = user
            return True
        return False