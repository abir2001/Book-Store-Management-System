import unittest  # Importing the unittest module for creating and running tests
from book import Book  # Importing the Book class from the book module
from cart import Cart  # Importing the Cart class from the cart module
from order import Order  # Importing the Order class from the order module
from user import User  # Importing the User class from the user module
from bookstore import Bookstore  # Importing the Bookstore class from the bookstore module
from db import get_connection, setup_database  # Importing database connection and setup functions
 
class TestBook(unittest.TestCase):
    """Test case for the Book class"""
 
    def test_book_creation(self):
        """Test the creation of a Book object and its attributes"""
        # Creating a Book object with sample data
        book = Book(1, "Test Title", "Test Author", 100.0, 10, "Test Category")
       
        # Asserting that the book attributes match the expected values
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "Test Title")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.price, 100.0)
        self.assertEqual(book.quantity, 10)
        self.assertEqual(book.category, "Test Category")
 
class TestCart(unittest.TestCase):
    """Test case for the Cart class"""
 
    def setUp(self):
        """Set up the database and create a test cart and test data"""
        setup_database()  # Setting up the database tables
        self.cart = Cart("testuser")  # Creating a Cart object for the test user
 
        # Connecting to the database
        conn = get_connection()
        cursor = conn.cursor()
 
        # Inserting a test user into the users table
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", ("testuser", "password", "user"),)
        # Inserting a test book into the books table
        cursor.execute("INSERT INTO books (id, title, author, price, quantity, category) VALUES (%s, %s, %s, %s, %s, %s)", (1, "Test Book", "Test Author", 100.0, 10, "Test Category"),)
        conn.commit()  # Committing the transaction
        conn.close()  # Closing the database connection
 
    def tearDown(self):
        """Clean up the test data from the database after each test"""
        # Connecting to the database
        conn = get_connection()
        cursor = conn.cursor()
 
        # Deleting the test data from the cart_items, books, and users tables
        cursor.execute("DELETE FROM cart_items WHERE username = %s", ("testuser",))
        cursor.execute("DELETE FROM books WHERE title = %s", ("Test Book",))
        cursor.execute("DELETE FROM users WHERE username = %s", ("testuser",))
        conn.commit()  # Committing the transaction
        conn.close()  # Closing the database connection
 
    def test_add_item(self):
        """Test adding an item to the cart and viewing the cart items"""
        # Adding an item to the cart
        self.cart.add_item(1, 2)
       
        # Viewing the cart items
        items = self.cart.view_cart()
       
        # Asserting that the cart contains the added item with the correct quantity
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0][0], 1)
        self.assertEqual(items[0][1], 2)
 
class TestUser(unittest.TestCase):
    """Test case for the User class"""
 
    def setUp(self):
        """Set up the database and add a test user"""
        setup_database()  # Setting up the database tables
        User.add_user("testuser", "password", "user")  # Adding a test user
 
    def tearDown(self):
        """Clean up the test data from the database after each test"""
        # Connecting to the database
        conn = get_connection()
        cursor = conn.cursor()
 
        # Deleting the test user from the users table
        cursor.execute("DELETE FROM users WHERE username = %s", ("testuser",))
        conn.commit()  # Committing the transaction
        conn.close()  # Closing the database connection
 
    def test_authenticate(self):
        """Test user authentication with correct and incorrect passwords"""
        # Retrieving the test user from the database
        user = User.get_user("testuser")
       
        # Asserting that the user can be authenticated with the correct password
        self.assertTrue(user.authenticate("password"))
       
        # Asserting that the user cannot be authenticated with an incorrect password
        self.assertFalse(user.authenticate("wrongpassword"))
 
class TestBookstore(unittest.TestCase):
    """Test case for the Bookstore class"""
 
    def setUp(self):
        """Set up the database and add test users"""
        setup_database()  # Setting up the database tables
        self.bookstore = Bookstore()  # Creating a Bookstore object
 
        # Adding test users
        User.add_user("testadmin", "password", "admin")
        User.add_user("testuser", "password", "user")
 
    def tearDown(self):
        """Clean up the test data from the database after each test"""
        # Connecting to the database
        conn = get_connection()
        cursor = conn.cursor()
 
        # Deleting the test users from the users table
        cursor.execute("DELETE FROM users WHERE username IN (%s, %s)", ("testadmin", "testuser"))
        # Deleting the test book from the books table
        cursor.execute("DELETE FROM books WHERE title = %s", ("Test Book",))
        conn.commit()  # Committing the transaction
        conn.close()  # Closing the database connection
 
    def test_signup(self):
        """Test the signup process of the bookstore"""
        self.bookstore.signup()  # Signing up a new user
       
        # Retrieving the newly signed-up user from the database
        user = User.get_user("newuser")
       
        # Asserting that the new user was successfully added to the database
        self.assertIsNotNone(user)
 
    def test_add_book(self):
        """Test adding a book to the bookstore inventory"""
        self.bookstore.current_user = User.get_user("testadmin")  # Setting the current user as an admin
        self.bookstore.add_book()  # Adding a book to the inventory
       
        # Connecting to the database
        conn = get_connection()
        cursor = conn.cursor()
 
        # Retrieving the added book from the books table
        cursor.execute("SELECT * FROM books WHERE title = %s", ("Test Book",))
        book = cursor.fetchone()
       
        # Asserting that the book was successfully added to the inventory
        self.assertIsNotNone(book)
        conn.close()  # Closing the database connection
 
if __name__ == "__main__":
    unittest.main()  # Running the unit tests