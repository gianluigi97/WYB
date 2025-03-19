from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

@app.route("/")
def homepage():

    conn = mysql.connector.connect(
            host = 'localhost', 
            user = 'root',
            password = 'gianrootluigi',
            database = 'webapp'
        )

    cur = conn.cursor()
    nomi = cur.execute("""SELECT name FROM users""")
        
    nomi = nomi.fetchall()


    return render_template("homepage.html", nomi=nomi)

if __name__ == "__main__":

    app.run(debug=True)