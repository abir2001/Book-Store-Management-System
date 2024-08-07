from flask import Flask, jsonify, request
from db import get_connection

app = Flask(__name__)


@app.route("/books", methods=["GET"])
def get_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, price, category FROM books")
    books = cursor.fetchall()
    conn.close()
    return jsonify(books)


@app.route("/book/<int:book_id>", methods=["GET"])
def get_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    conn.close()
    if book:
        return jsonify(book)
    return jsonify({"error": "Book not found"}), 404


if __name__ == "__main__":
    app.run(port=5000)
