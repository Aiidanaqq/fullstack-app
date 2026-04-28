from flask import Flask, request, jsonify

app = Flask(__name__)

data = []

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def add_data():
    item = request.json
    data.append(item)
    return jsonify({"message": "added"}), 201

@app.route('/api/data/<int:index>', methods=['DELETE'])
def delete_data(index):
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import psycopg2

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def home():
    return '<h1>Backend работает</h1><p>Open /api/data</p>'

@app.route('/api/data', methods=['GET'])
def get_data():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, text FROM items ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": r[0], "text": r[1]} for r in rows])

@app.route('/api/data', methods=['POST'])
def add_data():
    text = request.json.get("text")
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO items (text) VALUES (%s) RETURNING id, text;", (text,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": row[0], "text": row[1]})

@app.route('/api/data/<int:item_id>', methods=['DELETE'])
def delete_data(item_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE id = %s;", (item_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "deleted"})

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
