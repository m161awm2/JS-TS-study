from flask import Flask,request,session,url_for,jsonify,render_template
import pymysql
app = Flask(__name__)
app.secret_key = "123"

def mkdb():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        passwd="Zdzdsmsm44!",
    )
    c = conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXISTS Day05")
    conn.commit()
    conn.close()

def get_connect():
    return pymysql.connect(
        host="localhost",
        user="root",
        passwd="Zdzdsmsm44!",
        database="Day05",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def init_db():
    conn = get_connect()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS posts(
              id INT AUTO_INCREMENT PRIMARY KEY,
              nickname VARCHAR(30),
              title VARCHAR(50),
              content TEXT
              )
              """)
    c.execute("""CREATE TABLE IF NOT EXISTS comments(
              id INT AUTO_INCREMENT PRIMARY KEY,
              nickname VARCHAR(30),
              content TEXT,
              post_id INT
              )
              """)
    conn.commit()
    conn.close()

@app.route('/',methods=["GET"])
def home():
    return render_template("index.html")
@app.route('/api/board',methods=["GET"])
def board():
    conn = get_connect()
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    return jsonify(posts), 200

@app.route('/write',methods=["GET"])
def write_get():
    return render_template("write.html")
@app.route('/api/write',methods=["POST"])
def write():
    conn = get_connect()
    c = conn.cursor()
    data = request.get_json()
    nickname = data.get("nickname")
    title = data.get("title")
    content = data.get("content")
    c.execute("INSERT INTO posts (nickname,title,content) VALUES (%s,%s,%s)",(nickname,title,content))
    conn.commit()
    conn.close()
    return jsonify({"message" : "Success write"}),201

@app.route('/detail/<int:post_id>')
def detail(post_id):
    conn = get_connect()
    c = conn.cursor()
    c.execute("SELECT * FROM posts WHERE id = %s",(post_id,))
    post = c.fetchone()
    conn.close()
    return render_template('detail.html',post=post)
if __name__ == "__main__":
    mkdb()
    init_db()
    app.run(host="0.0.0.0",port=5000,debug=True)