from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import psycopg2

app = Flask(__name__)
CORS(app)

# 🔗 Подключение к БД (Railway)
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# 📦 Создание таблицы
def init_db():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS data (
            id SERIAL PRIMARY KEY,
            text TEXT
        )
    """)
    conn.commit()

# 📥 Получить данные
@app.route("/api/data", methods=["GET"])
def get_data():
    cur.execute("SELECT id, text FROM data")
    rows = cur.fetchall()
    result = [{"id": row[0], "text": row[1]} for row in rows]
    return jsonify(result)

# ➕ Добавить данные
@app.route("/api/data", methods=["POST"])
def add_data():
    data = request.get_json()
    text = data.get("text")

    cur.execute("INSERT INTO data (text) VALUES (%s) RETURNING id", (text,))
    new_id = cur.fetchone()[0]
    conn.commit()

    return jsonify({"id": new_id, "text": text})

@app.route("/api/data/<int:id>", methods=["DELETE"])
def delete_data(id):
    cur.execute("DELETE FROM data WHERE id = %s", (id,))
    conn.commit()
    return jsonify({"message": "Deleted"})

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
