from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

# --- Database setup---
def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def dict_from_row(row):
    """Convert SQLite row to dict"""
    return {"id": row[0], "name": row[1], "email": row[2]}

# --- CREATE ---
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and Email are required"}), 400

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return jsonify({"message": "User created", "id": new_id}), 201

# --- READ ALL ---
@app.route('/users', methods=['GET'])
def get_all_users():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    conn.close()

    return jsonify([dict_from_row(u) for u in users])

# --- READ ONE ---
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (id,))
    user = cur.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(dict_from_row(user))

# --- UPDATE ---
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and Email are required"}), 400

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("UPDATE users SET name=?, email=? WHERE id=?", (name, email, id))
    conn.commit()
    updated = cur.rowcount
    conn.close()

    if updated == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User updated successfully"})

# --- DELETE ---
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()
    deleted = cur.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User deleted successfully"})

# --- MAIN ---
if __name__ == '__main__':
    init_db()
    app.run(debug=True)

