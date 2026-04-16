from flask import Flask,request,session,jsonify
import pymysql
app = Flask(__name__)
app.secret_key = "123"

def mkdb():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        passwd=""
    )
    c = conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS restapi02")
    conn.commit()
    conn.close()

def get_conn():
    return pymysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="restapi02",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS posts(
              id INT AUTO_INCREMENT PRIMARY KEY,
              nickname TEXT,
              title VARCHAR(30),
              content TEXT
              )
              """)
    c.execute("""CREATE TABLE IF NOT EXISTS users(
              id INT AUTO_INCREMENT PRIMARY KEY,
              nickname VARCHAR(20),
              password TEXT
              )
              """)
    c.execute("""CREATE TABLE IF NOT EXISTS comments(
              id INT AUTO_INCREMENT PRIMARY KEY,
              nickname TEXT,
              content TEXT,
              post_id INT
              )
              """)
    conn.commit()
    conn.close()

@app.route('/posts',methods=["GET","POST"])
def write():
    if request.method == "GET":
        conn = get_conn()
        c = conn.cursor()
        c.execute("SELECT * FROM posts ORDER BY id DESC")
        posts = c.fetchall()
        conn.commit()
        conn.close()
        return jsonify(posts),200
    nickname = session.get("user")
    if not nickname:
        return jsonify({"message" : "fail, need login!"}),401 # 401 : 로그인 필요 
    
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")

    if title.replace(" ","") == "" or content.replace(" ","") == "":
        return jsonify({"message" : "wrong title or content, rewrite pls"}),400 # 잘못된 값

    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO posts (nickname,title,content) VALUES (%s,%s,%s)",(nickname,title,content))
    conn.commit()
    conn.close()
    return jsonify({"message" : "Success write"}),201 # 201 DB 성공

@app.route("/signup",methods=["POST"])
def signup():
    conn = get_conn()
    c = conn.cursor()
    data = request.get_json()
    nickname = data.get("nickname")
    password = data.get("password")
    c.execute("SELECT * FROM users WHERE nickname = %s",(nickname,))
    is_exists = c.fetchone()
    if is_exists:
        return jsonify({"message" : "fail signup exists!"}), 409 # 중복될때 409
    c.execute("INSERT INTO users (nickname,password) VALUES (%s,%s)",(nickname,password))
    conn.close()
    session["user"] = nickname
    return jsonify({"message" : "success signup and login!"}), 201 # DB 성공

@app.route("/login",methods=["POST"])
def login():
    conn = get_conn()
    c = conn.cursor()
    data = request.get_json()
    nickname = data.get("nickname")
    password = data.get("password")
    c.execute("SELECT * FROM users WHERE nickname = %s AND password = %s",(nickname,password))
    is_login = c.fetchone()
    if not is_login:
        return jsonify({"message" : "wrong! rewrite"}),401
    session["user"] = nickname
    return jsonify({"message" : "success login!"}), 200

@app.route()

@app.route("/comments/<int:post_id>",methods=["GET","POST"])
def comments(post_id):
    if request.method == "GET":
        conn = get_conn()
        c = conn.cursor()
        c.execute("SELECT * FROM comments WHERE post_id = %s",(post_id,))
        comments = c.fetchall()
        conn.close()
        return jsonify(comments)
    nickname = session.get("user")
    if not nickname:
        return jsonify({"message" : "login pls"}),401
    data = request.get_json()
    content = data.get("content")
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO comments (nickname,content,post_id) VALUES (%s,%s,%s)",(nickname,content,post_id))
    conn.close()
    return jsonify({"message" : "success writed!"}),201

if __name__ == "__main__":
    mkdb()
    init_db()
    app.run(host="localhost",port=5000,debug=True)