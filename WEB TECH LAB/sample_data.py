import sqlite3

def add_sample_data():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    books = [
        ("The Great Gatsby", "F. Scott Fitzgerald", 10.99),
        ("To Kill a Mockingbird", "Harper Lee", 8.99),
        ("1984", "George Orwell", 6.99),
        ("Pride and Prejudice", "Jane Austen", 12.99)
    ]
    cursor.executemany("INSERT INTO books (title, author, price) VALUES (?, ?, ?)", books)
    conn.commit()
    conn.close()

add_sample_data()
