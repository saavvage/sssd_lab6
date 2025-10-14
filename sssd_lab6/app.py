from flask import Flask, request, render_template, redirect, url_for, g, jsonify, make_response
import sqlite3, hashlib, os, re
from markupsafe import Markup

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")

app = Flask(__name__)

def get_db():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_db', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    return render_template("index.html")

# VULNERABLE: MD5 hashing without salt
def md5_hash(password: str) -> str:
    return hashlib.md5(password.encode("utf-8")).hexdigest()

@app.post("/register")
def register():
    username = request.form.get("username","").strip()
    password = request.form.get("password","")
    if not username or not password:
        return "Missing fields", 400
    db = get_db()
    db.execute("INSERT INTO users(username, password_hash, algo) VALUES (?, ?, ?)", (username, md5_hash(password), "md5"))
    db.commit()
    return redirect(url_for("index"))

@app.post("/login")
def login():
    username = request.form.get("username","").strip()
    password = request.form.get("password","")
    db = get_db()
    row = db.execute("SELECT id, password_hash, algo FROM users WHERE username = ?", (username,)).fetchone()
    if not row:
        return "Invalid credentials", 401
    if row["password_hash"] == md5_hash(password):
        return "OK", 200
    return "Invalid credentials", 401

# VULNERABLE: SQL injection via f-string & LIKE pattern
@app.get("/search")
def search():
    q = request.args.get("q","")
    db = get_db()
    # intentionally vulnerable
    sql = f"SELECT id, name, price FROM products WHERE name LIKE '%{q}%' ORDER BY id DESC"
    rows = db.execute(sql).fetchall()
    return jsonify([dict(r) for r in rows])

# VULNERABLE: no validation; unsafe rendering of comments (possible XSS)
@app.get("/comments")
def get_comments():
    db = get_db()
    rows = db.execute("SELECT author, body FROM comments ORDER BY id DESC").fetchall()
    # explicitly mark as safe -> XSS
    rendered = [Markup(f"<p><b>{r['author']}</b>: {r['body']}</p>") for r in rows]
    return render_template("comments.html", comments=rendered)

@app.post("/comments")
def post_comment():
    author = request.form.get("author","anonymous")
    body = request.form.get("body","")
    db = get_db()
    db.execute("INSERT INTO comments(author, body) VALUES (?, ?)", (author, body))
    db.commit()
    return redirect(url_for("get_comments"))

if __name__ == "__main__":
    app.run(debug=True)
