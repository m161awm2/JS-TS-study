from flask import Flask,request,session,render_template,jsonify
import pymysql
from db_password import DB_PASSWORD
import datetime

app = Flask(__name__)
app.secret_key = DB_PASSWORD

def mkdb():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        passwd=DB_PASSWORD
    )
    c = conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS Day07")
    conn.commit()
    conn.close()

def get_conn():
    return pymysql.connect(
        host="localhost",
        user="root",
        passwd=DB_PASSWORD,
        database="Day07",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS posts(
              id INT AUTO_INCREMENT PRIMARY KEY,
              nickname TEXT,
              title VARCHAR(40),
              content TEXT
              )
              """)
    c.execute("""CREATE TABLE IF NOT EXISTS users(
              id INT AUTO_INCREMENT PRIMARY KEY,
              nickname VARCHAR(22),
              password TEXT
              )
              """)
    c.execute("""CREATE TABLE IF NOT EXISTS comments(
              id INT AUTO_INCREMENT PRIMARY KEY,
              nickname TEXT,
              password TEXT
              )
              """)
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template("index.html")
@app.route('/api/board')
def board():
    nickname = session.get("user")
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    c.close()
    return jsonify({
        posts,
        nickname
    })

@app.route('/login')
def login_get():
    return render_template("login.html")
@app.route('/api/login',methods=["POST"])
def login():
    conn = get_conn()
    c = conn.cursor()
    data = request.get_json()
    nickname = data.get("nickname")
    password = data.get("password")
    c.execute("SELECT * FROM users WHERE nickname = %s AND password = %s",(nickname,password))
    is_login = c.fetchone()
    conn.close()
    if is_login:
        session["user"] = nickname
        return jsonify({"message" : "Success Login!"}), 201
    return jsonify({"message" : "fail Login!"}), 401

@app.route('/register')
def register_get():
    return render_template("register.html")
@app.route('/api/register',methods=["POST"])
def register():
    conn = get_conn()
    c = conn.cursor()
    data = request.get_json()
    nickname = data.get("nickname")
    password = data.get("password")
    c.execute("SELECT * FROM users WHERE nickname = %s",(nickname,))
    is_exists = c.fetchone()
    if is_exists:
        return jsonify({"message" : "fail, ur name is exists"}),401
    c.execute("INSERT INTO users (nickname,password) VALUES (%s,%s)",(nickname,password))
    conn.commit()
    conn.close()
    return jsonify({"message" : "Success register!"}),201

@app.route('/detail')
def detail_get():
    return render_template("detail.html")
@app.route('/api/detail/<post_id>')
def detail(post_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id = %s",(post_id,))
    post = c.fetchone()
    return jsonify(post)

@app.route('/write')
def write_get():
    return render_template("write.html")
@app.route('/api/write',methods=["POST"])
def write():
    nickname = session.get("user")
    if not nickname:
        return jsonify({"message" : "fail login, pls login!"}),400
    conn = get_conn()
    c = conn.cursor()
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    c.execute("INSERT INTO posts (nickname,title,content) VALUES (%s,%s,%s)",(nickname,title,content))
    conn.commit()
    conn.close()
    return jsonify({"message" : "Success write!"}),201
if __name__ == "__main__":
    mkdb()
    init_db()
    app.run(host="0.0.0.0",port=5000,debug=True)