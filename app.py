from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'database/library.db'

# Create database if not exists
def init_db():
    if not os.path.exists('database'):
        os.mkdir('database')
    conn = sqlite3.connect(DATABASE)
    conn.execute('''CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT,
                        year INTEGER
                    )''')
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        conn = sqlite3.connect(DATABASE)
        conn.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
        conn.commit()
        conn.close()
        return redirect('/books')
    return render_template('add_book.html')

@app.route('/books')
def books():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    data = cur.fetchall()
    conn.close()
    return render_template('book_list.html', books=data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
