import mysql.connector  # Importing MySQL connector module

def get_connection():
    """
    Function to establish a connection to the MySQL database.
    Returns:mysql.connector.connection.MySQLConnection: A connection object to the MySQL database.
    """
    conn = mysql.connector.connect(
        host="localhost",  # MySQL server hostname
        port="3306",  # Port number for MySQL server
        user="root",  # Username for database access
        password="root",  # Password for database access
        database="bookstore",  # Name of the database to connect to
    )
    return conn  # Returning the connection object

def setup_database():
    # Function to set up the necessary database tables if they don't exist

    conn = get_connection()  # Establishing a database connection

    if conn is None:
        return

    cursor = conn.cursor()

    # Creating 'users' table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(100) PRIMARY KEY,
            password VARCHAR(100) NOT NULL,
            role VARCHAR(100) NOT NULL
        )
    """
    )

    # Creating 'books' table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            author VARCHAR(100) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            quantity INT NOT NULL,
            category VARCHAR(100) NOT NULL
            )
        """
    )

    # Creating 'orders' table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        total DECIMAL(10,2) NOT NULL,
        order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (username) REFERENCES users(username)
            )
        """
    )

    # Creating 'order_items' table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS order_items (
        order_id INT,
        book_id INT,
        quantity INT,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (book_id) REFERENCES books(id)
            )
        """
    )

    # Creating 'cart_items' table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cart_items (
        username VARCHAR(100) NOT NULL,
        book_id INT,
        quantity INT,
        PRIMARY KEY (username, book_id),
        FOREIGN KEY (username) REFERENCES users(username),
        FOREIGN KEY (book_id) REFERENCES books(id)
            )
        """
    )

    conn.commit()  # Committing the transaction
    conn.close()  # Closing the database connection

setup_database()  # Calling the setup_database function to initialize the database tables