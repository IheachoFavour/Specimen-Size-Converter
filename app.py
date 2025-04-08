from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from dotenv import load_dotenv
import os
load_dotenv()


app = Flask(__name__)
app.secret_key = 'your_secret_key'

def drop_table():
    try:
        conn = sqlite3.connect('specimen_data.db')
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS specimens')
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def create_table():
    conn = sqlite3.connect('specimen_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS specimens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            actual_size REAL NOT NULL,
            converted_size REAL NOT NULL,
            magnification REAL NOT NULL,
            from_unit TEXT NOT NULL,
            to_unit TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def convert_size(size, from_unit, to_unit, magnification=1):
    conversion_factors = {
        'mm': 1,
        'cm': 10,
        'm': 1000,
        'inches': 25.4,
        'feet': 304.8,
        'um': 0.001  # Micrometers to mm
    }
    
    if from_unit not in conversion_factors or to_unit not in conversion_factors:
        return None
    
    size_in_mm = size * conversion_factors[from_unit]
    magnified_size_in_mm = size_in_mm / magnification
    converted_size = magnified_size_in_mm / conversion_factors[to_unit]
    
    return converted_size

def save_to_database(username, actual_size, converted_size, magnification, from_unit, to_unit):
    conn = sqlite3.connect('specimen_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO specimens (username, actual_size, converted_size, magnification, from_unit, to_unit) VALUES (?, ?, ?, ?, ?, ?)',
                   (username, actual_size, converted_size, magnification, from_unit, to_unit))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('specimen_data.db')
    cursor = conn.cursor()
    
    # Fetch existing records
    cursor.execute('SELECT * FROM specimens')
    records = cursor.fetchall()
    conn.close()
    
    if request.method == 'POST':
        username = request.form['username']
        size = float(request.form['size'])
        from_unit = request.form['from_unit']
        to_unit = request.form['to_unit']
        magnification = float(request.form['magnification']) if request.form['magnification'] else 1
        
        result = convert_size(size, from_unit, to_unit, magnification)
        
        if result is not None:
            # Save to the database, including magnification
            save_to_database(username, size, result, magnification, from_unit, to_unit)
            flash(f"{username}, the real life size is: {result:.2f} {to_unit}", "success")
        else:
            flash("Invalid unit provided.", "error")
        
        return redirect(url_for('index'))
    
    return render_template('index.html', records=records)

if __name__ == '__main__':
    create_table()
    port = os.environ.get('PORT') or 4000
    app.run(debug=True, host="0.0.0.0", port=port)
