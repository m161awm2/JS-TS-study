from flask import Flask,request,render_template,jsonify
import pymysql
from db_password import DB_PASSWORD
import datetime

app = Flask(__name__)

def make_db():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password=DB_PASSWORD
    )
    c = conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS day06")
    conn.commit()
    conn.close()

def get_conn():
    return pymysql.connect(
        host="localhost",
        user="root",
        password=DB_PASSWORD,
        database="day06",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS posts(
              id INT AUTO_INCREMENT PRIMARY KEY,
              nickname VARCHAR(30),
              password TEXT,
              title VARCHAR(100),
              content TEXT,
              time TEXT
              )
              """)
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template("index.html")
@app.route('/api/board',methods=["GET"])
def board():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    return jsonify(posts), 200
@app.route('/api/write',methods=["POST"])
def write():
    data = request.get_json()
    nickname = data.get("nickname")
    password = data.get("password")
    title = data.get("title")
    content = data.get("content")
    time = datetime.datetime.now()
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO posts (nickname,password,title,content,time) VALUES (%s,%s,%s,%s,%s)",(nickname,password,title,content,time))
    conn.commit()
    conn.close()
    return jsonify({"message" : "Success write"})

if __name__ == "__main__":
    make_db()
    init_db()
    app.run(host="0.0.0.0",port=5000,debug=True)