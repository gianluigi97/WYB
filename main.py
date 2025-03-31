from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import pandas as pd

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

        try:
            cur.execute("INSERT INTO records(nome, litri) VALUES (?, ?)", (nome, litri))
            conn.commit()
        except sqlite3.IntegrityError as e:
            print("Errore di integrità:", e)
        finally:
            conn.close()  

@app.route("/", methods=["GET", "POST"])
def homepage():
    conn = Database.connection()
    cur = conn.cursor()

    
    if request.method == "POST":
        nome = request.form['user']
        litri = request.form['quantity']
        Database.addRecord(nome, litri)
        conn.close()  
        return redirect(url_for("homepage")) # EVITA CHE LA RICHIESTA POST SI RIPETI OGNI VOLTA CHE SI RICARICA LA PAGINA

    
    cur.execute("SELECT nome FROM users")
    nomi = [row[0] for row in cur.fetchall()]

    
    start = 2025
    actual = cur.execute("SELECT COALESCE(SUM(litri), 0) FROM records").fetchone()[0]
    totale = start - actual

    conn.close()  

    return render_template("homepage.html", nomi=nomi, totale=totale)

@app.route("/classifica", methods=["GET"])
def show_rankings():
    conn = Database.connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ranking ORDER BY totale DESC")

    ranking = pd.DataFrame(data=cur.fetchall())
    ranking.columns = ['nome', 'totale']
    nome = ranking['nome']
    totale = ranking['totale']

    conn.close()

    dati_accoppiati = zip(nome, totale)

    return render_template('ranking.html', nomi=nome, totale=dati_accoppiati)



if __name__ == "__main__":
    app.run(debug=True)

