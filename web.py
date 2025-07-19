from flask import Flask, request, send_file, abort
import os
import sqlite3

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
DATABASE = "database.db"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS files (
                            id TEXT PRIMARY KEY,
                            file_name TEXT,
                            file_path TEXT
                        )""")
init_db()

@app.route('/')
def home():
    return "File Server is Running."

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    file_id = request.form.get('file_id')

    if not file or not file_id:
        return "Missing file or file_id", 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    with sqlite3.connect(DATABASE) as conn:
        conn.execute("INSERT INTO files (id, file_name, file_path) VALUES (?, ?, ?)",
                     (file_id, file.filename, path))
    return "Uploaded"

@app.route('/download/<file_id>')
def download(file_id):
    with sqlite3.connect(DATABASE) as conn:
        row = conn.execute("SELECT file_name, file_path FROM files WHERE id=?", (file_id,)).fetchone()

    if not row:
        abort(404)

    return send_file(row[1], as_attachment=True, download_name=row[0])

if __name__ == '__main__':
    app.run()
