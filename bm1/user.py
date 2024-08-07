from db import get_connection  # Importing the function to establish a database connection

class User:
    def __init__(self, username, password, role):
        # Constructor for the User class.
        """
        Parameters:
            username (str): The username of the user.
            password (str): The password of the user.
            role (str): The role of the user (e.g., 'user' or 'admin').
        """
        self.username = username
        self.password = password
        self.role = role

    def authenticate(self, password):
        # Method to authenticate the user by comparing the provided password with the stored password.
        """
        Parameters:
            password (str): The password to authenticate.
        Returns:
            bool: True if the provided password matches the stored password, False otherwise.
        """
        return self.password == password

    @staticmethod
    def add_user(username, password, role):
        # Static method to add a new user to the database.
        """
        Parameters:
            username (str): The username of the new user.
            password (str): The password of the new user.
            role (str): The role of the new user (e.g., 'user' or 'admin').
        """
        conn = get_connection()  # Establishing a database connection
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role),)
        conn.commit()  # Committing the transaction
        conn.close()  # Closing the database connection

    @staticmethod
    def get_user(username):
        # Static method to retrieve a user from the database based on the username.
        # Parameters: username (str): The username of the user to retrieve.
        # Returns: User or None: The User object if the user is found, None otherwise.

        conn = get_connection()  # Establishing a database connection
        cursor = conn.cursor()
        cursor.execute("SELECT username, password, role FROM users WHERE username = %s", (username,),)
        user_data = cursor.fetchone()
        conn.close()  # Closing the database connection
        if user_data:
            return User(*user_data)  # Returning a User object with user data if found
        return None  # Returning None if user not found