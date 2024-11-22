from flask import Flask, jsonify, render_template, request,session, redirect, url_for
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
CORS(app)

def init_db():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    logged_in = session.get('logged_in', False)
    return render_template("index.html",logged_in=logged_in)

@app.route("/books")
def get_books():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, author, price FROM books")
    books = [{"title": row[0], "author": row[1], "price": row[2]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(books)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        data = request.get_json()  # Parse JSON data from the request body
        email = data.get("email")
        password = data.get("password")
        
        conn = sqlite3.connect("books.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['logged_in'] = True
            return jsonify({"success": True, "redirect": "/"})  # Send JSON response
        return jsonify({"success": False, "message": "Invalid email or password"})

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        conn = sqlite3.connect("books.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        conn.close()
        return redirect(url_for("login"))
    except sqlite3.IntegrityError:
        return render_template("register.html", error="Email already registered")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route("/check_login")
def check_login():
    logged_in = session.get('logged_in', False)
    return jsonify({"logged_in": logged_in})

if __name__ == "__main__":
    init_db()  # Initialize the database
    app.run(debug=True)
