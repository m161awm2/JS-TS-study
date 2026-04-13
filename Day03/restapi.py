from flask import Flask,request,jsonify,session
import pymysql

app = Flask(__name__)
app.secret_key = "레스트api겁나어렵네"
def mk_db():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        passwd="Zdzdsmsm44!"
    )
    c = conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS restapi")
    conn.commit()
    conn.close()

def get_conn():
    return pymysql.connect(
        host="localhost",
        user="root",
        passwd="Zdzdsmsm44!",
        database="restapi",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS posts(
              id INT AUTO_INCREMENT PRIMARY KEY,
              username TEXT,
              title VARCHAR(50),
              content TEXT
              )
              """)
    c.execute("""CREATE TABLE IF NOT EXISTS users(
              id INT AUTO_INCREMENT PRIMARY KEY,
              username VARCHAR(39),
              password VARCHAR(255)
              )
              """)
    conn.commit()
    conn.close()

@app.route("/posts", methods=["GET","POST"])
def posts():
    if request.method == "GET":
        conn = get_conn()
        c = conn.cursor()
        c.execute("SELECT * FROM posts ORDER BY id DESC")
        posts = c.fetchall()
        conn.close()
        return jsonify(posts)
    username = session.get("username")
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    conn = get_conn()
    c = conn.cursor()
    if not username:
        return jsonify({"message": "Fail(로그인을 먼저 하세요!)"}), 401
    c.execute("INSERT INTO posts (username, title, content) VALUES (%s,%s,%s)",(username,title,content))
    conn.close()
    return jsonify({"message": "Post created successfully"})

@app.route("/login",methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = %s AND password = %s",(username,password))
    login = c.fetchone()
    if login:
        session["username"] = username
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Login failed"}), 401

@app.route("/signup",methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = %s",(username,))
    is_exists = c.fetchone()
    if is_exists:
        return jsonify({"message" : "signup fail (exists username)"}), 401
    c.execute("INSERT INTO users (username,password) VALUES (%s,%s)",(username,password))
    conn.commit()
    conn.close()
    return jsonify({"message" : "signup successful"})
if __name__ == "__main__":
    mk_db()
    init_db()
    app.run(host="localhost",port=5000,debug=True)