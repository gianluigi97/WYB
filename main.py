from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import pandas as pd
import os 

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

    @classmethod
    def resetRecords(cls, adminPassword):
        conn=cls.connection()
        cur = conn.cursor()

        if adminPassword == "031097":
            cur.execute("DELETE * FROM records")
            print("records reset")

        else: print("Admin password incorrect")

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


@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

@app.route('/sw.js')
def serve_sw():
    return send_file('sw.js', mimetype='application/javascript')

#if __name__ == "__main__":
    #app.run(host="192.168.1.15", port="5000", debug=True)
    #app.run(debug=True)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

