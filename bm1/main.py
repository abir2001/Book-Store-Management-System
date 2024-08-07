from bookstore import Bookstore  # Importing the Bookstore class from the bookstore module
import re  # Regular expression module

def main():
    """Function to run the main program."""
    # Creating a Bookstore object
    bookstore = Bookstore()

    # User Authenticat1ion
    while True:
        print("1. Login")
        print("2. Sign Up")
        choice = input("\nChoose an action : ").upper()

        if choice == "1":
            # Logging in the user
            if bookstore.login():
                break
        elif choice == "2":
            # Signing up a new user
            bookstore.signup()
        else:
            print("Invalid choice")

    # Main Menu
    while True:
        if bookstore.current_user and bookstore.current_user.role == "user":
            print("\nMain Menu :")
            print("U1. Browse Books")
            print("U2. Search Books")
            print("U3. Filter Books By Price")
            print("U4. Add To Cart")
            print("U5. View Cart")
            print("U6. Clear Cart")
            print("U7. Checkout")
 
        # Additional options for admin users
        if bookstore.current_user and bookstore.current_user.role == "admin":
            print("A1. Add Book")
            print("A2. Update Book")
            print("A3. Delete Book")
            print("A4. Generate Report")

        print("0. Logout")

        choice = input("\nChoose an action : ").upper()

        if choice == "0":
            # Logging out the user
            bookstore.logout()
            break
        elif choice == "U1":
            # Browsing available books
            bookstore.browse_books()
        elif choice == "U2":
            # Searching for books
            bookstore.search_books()
        elif choice == "U3":
            # Filtering books by price range
            bookstore.filter_books()
        elif choice == "U4":
            # Adding a book to the cart
            bookstore.add_to_cart()
        elif choice == "U5":
            # Viewing the cart
            bookstore.view_cart()
        elif choice == "U6":
            # Clearing the cart
            bookstore.clear_cart()
        elif choice == "U7":
            # Proceeding to checkout
            bookstore.checkout()
        elif (choice == "A1" and bookstore.current_user and bookstore.current_user.role == "admin"):
            # Adding a new book (admin only)
            bookstore.add_book()
        elif (choice == "A2" and bookstore.current_user and bookstore.current_user.role == "admin"):
            # Updating an existing book (admin only)
            bookstore.update_book()
        elif (choice == "A3" and bookstore.current_user and bookstore.current_user.role == "admin"):
            # Deleting a book (admin only)
            bookstore.delete_book()
        elif (choice == "A4" and bookstore.current_user and bookstore.current_user.role == "admin"):
            # Generating reports (admin only)
            bookstore.generate_reports()
        else:
            print("Invalid choice. Please select a valid action")

if __name__ == "__main__":
    main()