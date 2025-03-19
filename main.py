from flask import Flask, render_template
import sqlite3
import pandas as pd 

app = Flask(__name__)

class Database:

    dbname = "utenti_db"

    @classmethod
    def connection(cls):
        return sqlite3.connect(cls.dbname)

    

@app.route("/")
def index():

    conn = Database.connection()
    cur = conn.cursor()
    results = cur.execute("""SELECT nome FROM users""")
    nomi = [row[0] for row in cur.fetchall()]

    return render_template("homepage.html", nomi=nomi)
    

if __name__ == "__main__":

    app.run(debug=True)

    # conn = Database.connection()
    # cur = conn.cursor()
    # cur.execute("""SELECT * FROM users""")
    # print(cur.fetchall())