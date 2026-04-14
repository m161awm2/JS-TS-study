from flask import Flask,request,session,jsonify
import pymysql
app = Flask(__name__)
app.secret_key = "123"

def mkdb():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        passwd="Zdzdsmsm44!"
    )
    c = conn.cursor()
    c.execute("CREATE DATABASE IF NOT EXIST restapi02")
    conn.commit()
    conn.close()