from flask import Flask, request, send_from_directory, jsonify
import os
import sqlite3

app = Flask(__name__)
os.makedirs("uploads", exist_ok=True)

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS files (file_id TEXT PRIMARY KEY, file_name TEXT)")
conn.commit()

@app.route("/save", methods=["POST"])
def save():
    data = request.get_json()
    cursor.execute("INSERT OR REPLACE INTO files (file_id, file_name) VALUES (?, ?)", (data["id"], data["name"]))
    conn.commit()
    return jsonify({"status": "ok"})

@app.route("/download/<file_id>")
def download(file_id):
    cursor.execute("SELECT file_name FROM files WHERE file_id = ?", (file_id,))
    row = cursor.fetchone()
    if row:
        return send_from_directory("uploads", row[0], as_attachment=True)
    return "File not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
