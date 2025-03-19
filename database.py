import mysql.connector
from flask import Flask, url_for, request, render_template, redirect



class User:

    def __init__(self, email, nome, password):
        
        self.email = email
        self.nome = nome
        self._password = password
        

    def __repr__(self) -> str:
        return f'User(email={self.email}, nome={self.nome})'

    @classmethod
    def check_user(ins_nome, ins_password):
        conn = mysql.connector.connect(
            host = 'localhost', 
            user = 'root',
            password = 'gianrootluigi',
            database = 'webapp'
        )

        cur = conn.cursor()
        ispresent = cur.execute("""SELECT count(*) FROM users WHERE nome='%s' AND password='%s'""", (ins_nome, ins_password))
        
        return ispresent.fetchone()


    def add_user(self):
        conn = mysql.connector.connect(
            host = 'localhost', 
            user = 'root',
            password = 'gianrootluigi',
            database = 'webapp'
        )

        cur = conn.cursor()
        query = """INSERT INTO users(email, nome, password) VALUES (%s, %s, %s)"""
        try: 
            cur.execute(query, (self.email, self.nome, self._password))
            conn.commit()

            conn.close()
            return print(f'{self.email} signed in')

        except Exception as e:
            return print(f'errore: {e}')
        
class Record(User):
    def __init__(self, litres):
        super().__init__(self.nome)
        self.litres = litres

    def add_record(self):
        conn = mysql.connector.connect(
            host = 'localhost', 
            user = 'root',
            password = 'gianrootluigi',
            database = 'webapp'
        )

        cur = conn.cursor()
        query = """INSERT INTO body(nome, litres) VALUES (%s, %s)"""
        try: 
            cur.execute(query, (self.nome, self.litres))
            conn.commit()

            conn.close()
            return print(f'Record aggiunto!')

        except Exception as e:
            return print(f'errore: {e}')
 

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        name = request.form["nome"]

        ispresent = User().check_user(email, name)
        if ispresent == 1:
            redirect(url_for("homepage"))
        
        else: print("utente non registrato")
    

@app.route("/signIn", methods=["GET", "POST"])
def auth():
    if request.method == "POST":

        email = request.form["email"]
        name = request.form["nome"]
        password = request.form["password"]

        if not email or not name or not password: 
            raise print("Inserire tutti i campi")

        user = User(email, name, password)
        user.add_user()

        # CERCA DI CAPIRE SESSION:

        # session['email'] = email
        # session['name'] = name
        # session['password'] = password

    return render_template("signIn.html")

@app.route("/submit")
def submit():
    return redirect(url_for('homepage'))


@app.route("/homepage", methods=["GET", "POST"])
def homepage():

    if request.method == "POST":

        qt = request.form["quantity"]
        record = Record(qt)
        record.add_record()

    return render_template('homepage.html')



if __name__ == "__main__":
    app.run(debug=True)




