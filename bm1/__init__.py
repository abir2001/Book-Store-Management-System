# Importing necessary classes from respective modules
from .book import Book  # Importing Book class from book module
from .user import User  # Importing User class from user module
from .cart import Cart  # Importing Cart class from cart module
from .order import Order  # Importing Order class from order module
from .report import Report  # Importing Report class from report module
from .bookstore import Bookstore  # Importing Bookstore class from bookstore module

from db import setup_database  # Importing setup_database function from db module

setup_database()  # Setting up the database