from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute('SELECT username, password FROM users WHERE email = ?', (email,))
        user = cur.fetchone()
        conn.close()
        if user and user[1] == password:
            session['user'] = {'username': user[0]}
            return redirect(url_for('home'))
        error = 'Incorrect email or password.'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        if password != confirm:
            error = 'Passwords do not match.'
        else:
            try:
                conn = sqlite3.connect('users.db')
                conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                             (username, email, password))
                conn.commit()
                conn.close()
                session['user'] = {'username': username}
                return redirect(url_for('home'))
            except:
                error = 'Email is already registered.'
    return render_template('register.html', error=error)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        query = request.form['query']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pc_parts WHERE name LIKE ?', ('%' + query + '%',))
        results = cursor.fetchall()
        conn.close()
    return render_template('search.html', results=results)

@app.route('/add_part', methods=['GET', 'POST'])
def add_part():
    message = None
    if request.method == 'POST':
        try:
            name = request.form['name']
            category = request.form['category']
            brand = request.form['brand']
            model = request.form['model']
            price = request.form['price']
            conn = sqlite3.connect('database.db')
            conn.execute('INSERT INTO pc_parts (name, category, brand, model, price) VALUES (?, ?, ?, ?, ?)',
                         (name, category, brand, model, price))
            conn.commit()
            conn.close()
            message = 'PC Part added successfully!'
        except Exception as e:
            message = str(e)
    return render_template('add_part.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
