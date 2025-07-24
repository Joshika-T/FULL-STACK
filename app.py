from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'


def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Create tables
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS bookings (
        username TEXT,
        flight TEXT,
        seat TEXT
    )''')

    conn.commit()
    conn.close()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        # Check if user exists
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()

        # If not, register the new user
        if not user:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()

        conn.close()
        session['username'] = username
        return redirect('/booking')

    return render_template('login.html')


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if 'username' not in session:
        return redirect('/login')

    username = session['username']
    flights = ['IndiGo 6E-345', 'Air India AI-202', 'Vistara UK-101', 'SpiceJet SG-550', 'Qatar Airways QR-404']

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    if request.method == 'POST':
        flight = request.form['flight']
        seat = request.form['seat']
        cur.execute("INSERT INTO bookings (username, flight, seat) VALUES (?, ?, ?)", (username, flight, seat))
        conn.commit()
        conn.close()
        return redirect('/booking?booked=1')

    # Get previous bookings
    cur.execute("SELECT flight, seat FROM bookings WHERE username = ?", (username,))
    previous_bookings = cur.fetchall()
    conn.close()

    booked = request.args.get('booked') == '1'

    return render_template('booking.html', username=username, flights=flights, bookings=previous_bookings, booked=booked)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
