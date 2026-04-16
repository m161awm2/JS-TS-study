from flask import Flask,request,session,render_template,jsonify
import pymysql
app = Flask(__name__)
app.secret_key = "덕테이프"

def mkdb():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        passwd=""
    )
    c = conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS Day04")
    conn.commit()
    conn.close()

def get_conn():
    return pymysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="Day04",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS posts(
              id INT AUTO_INCREMENT PRIMARY KEY,
              nickname TEXT,
              title VARCHAR(60),
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

@app.route("/")
def home():
    return render_template("index.html")
@app.route('/api/board',methods=["GET"])
def board():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    return jsonify(posts)

@app.route('/write-go',methods=["GET"])
def write_get():
    return render_template("write.html")
@app.route('/api/write',methods=["POST"])
def write():
    conn = get_conn()
    c = conn.cursor()
    nickname = session.get("user")
    if not nickname:
        return jsonify({"message" : "fail write! pls login!"}),400
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    c.execute("INSERT INTO posts (nickname,title,content) VALUES (%s,%s,%s)",(nickname,title,content))
    conn.commit()
    conn.close()
    return jsonify({"message" : "Success write!"}),201

@app.route('/signup-go',methods=["GET"])
def signup_get():
    return render_template("signup.html")
@app.route('/api/signup',methods=["POST"])
def signup():
    conn = get_conn()
    c = conn.cursor()
    data = request.get_json()
    nickname = data.get("nickname")
    password = data.get("password")
    c.execute("SELECT * FROM users WHERE nickname = %s",(nickname,))
    is_exists = c.fetchone()
    if is_exists:
        return jsonify({"message" : "이미존재하는회원이름입니다"}),401
    c.execute("INSERT INTO users (nickname,password) VALUES (%s,%s)",(nickname,password))
    conn.commit()
    conn.close()
    return jsonify({"message": "Success signup!"}), 201

@app.route('/login-go',methods=["GET"])
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
    conn.commit()
    conn.close()
    if not is_login:
        return jsonify({"message" : "fail login! wrong name or pw"}),400
    session["user"] = nickname
    return jsonify({"message" : "Success login!"}),200

@app.route('/detail/<int:post_id>')
def detail_get(post_id):
    return render_template("detail.html",post_id=post_id)
@app.route('/api/detail/<int:post_id>',methods=["GET"])
def detail(post_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM comments WHERE post_id = %s",(post_id,))
    comments = c.fetchall()
    c.execute("SELECT * FROM posts WHERE id = %s",(post_id,))
    post = c.fetchone()
    conn.close()
    return jsonify({
        "post": post,
        "comments": comments
    })

if __name__ == "__main__":
    mkdb()
    init_db()
    app.run(host="0.0.0.0",port=5000,debug=True)