from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

class Database:

    dbname = "utenti_db"

    @classmethod
    def connection(cls):
        return sqlite3.connect(cls.dbname)

    @classmethod
    def addRecord(cls, nome, litri):

        conn = cls.connection()
        cur = conn.cursor()

        cur.execute("""INSERT INTO record(nome, litri) VALUES (?, ?)""", (nome, litri))
        conn.commit()

        return 
    


@app.route("/")
def index():
    conn = Database.connection()
    cur = conn.cursor()

    results = cur.execute("""SELECT nome FROM users""")
    nomi = [row[0] for row in cur.fetchall()]

    start = 2025
    actual = cur.execute("""Select sum(litri) from record""").fetchone()[0]
    totale = start - actual

    return render_template("homepage.html", nomi=nomi, totale=totale)
   
    
@app.route("/")
def record():
    conn = Database.connection()
    
    if request.method == "POST":
        nome = request.form['nome']
        litri = request.form['litri']

        Database.addRecord(nome, litri)

    return render_template("homepage.html")






if __name__ == "__main__":

    app.run(debug=True)

    