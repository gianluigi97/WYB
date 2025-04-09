from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import pandas as pd
import os 
from connectionDB import Database

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def homepage():
    conn = Database.connection()
    cur = conn.cursor()

    if request.method == "POST":
        nome = request.form['user']
        litri = request.form['quantity']
        Database.addRecord(nome, litri)
        conn.close()  
        return redirect(url_for("homepage"))  

    cur.execute("SELECT nome FROM players")
    nomi = [row[0] for row in cur.fetchall()]

    start = 2025
    cur.execute("SELECT COALESCE(SUM(quantity), 0) FROM records")
    actual = cur.fetchone()
    totale = start - actual[0]  

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



@app.route("/storico", methods=["GET"])
def show_history():
    conn = Database.connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM records ORDER BY date desc")

    history = pd.DataFrame(data=cur.fetchall())
    history.columns = ["id", "nome", "qty", "time"]
    history['time'] = [row.strftime("%Y-%m-%d %H:%M:%S") for row in history['time']]
    history = history.to_dict(orient="records")

    return render_template('history.html', history=history)


@app.route("/storico/<int:record_id>")
def delete_record(record_id):

    Database.deleteRecord(record_id=record_id)

    return redirect(url_for("show_history"))  


@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

@app.route('/sw.js')
def serve_sw():
    return send_file('sw.js', mimetype='application/javascript')


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    # app.run(debug=True)

