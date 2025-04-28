import sqlite3

# Connect to database
def connect_db():
    conn = sqlite3.connect('database/bioseed.db')
    return conn

# Save farmer's input data
def save_farmer_input(soil, rainfall, season, goal):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS farmers_input (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        soil TEXT,
        rainfall TEXT,
        season TEXT,
        goal TEXT
    )
    ''')
    cursor.execute('INSERT INTO farmers_input (soil, rainfall, season, goal) VALUES (?, ?, ?, ?)', (soil, rainfall, season, goal))
    conn.commit()
    conn.close()

# Save final recommendation
def save_recommendation(crop):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recommended_crop TEXT
    )
    ''')
    cursor.execute('INSERT INTO recommendations (recommended_crop) VALUES (?)', (crop,))
    conn.commit()
    conn.close()
