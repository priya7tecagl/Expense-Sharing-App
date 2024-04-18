from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite database initialization
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 description TEXT,
                 amount REAL,
                 paid_by TEXT,
                 split_with TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Home route
@app.route('/')
def home():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()
    conn.close()
    return render_template('index.html', expenses=expenses)

# Add expense route
@app.route('/add', methods=['POST'])
def add_expense():
    description = request.form['description']
    amount = float(request.form['amount'])
    paid_by = request.form['paid_by']
    split_with = request.form['split_with']

    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (description, amount, paid_by, split_with) VALUES (?, ?, ?, ?)",
              (description, amount, paid_by, split_with))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

# Delete expense route
@app.route('/delete_expense/<int:expense_id>', methods=['GET'])
def delete_expense(expense_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
