import psycopg2
from dotenv import load_dotenv
import os

class Database: 

    load_dotenv()

    USER = os.getenv("DB_USER")
    PASSWORD = os.getenv("DB_PASSWORD")
    HOST = os.getenv("DB_HOST")
    PORT = os.getenv("DB_PORT")
    DBNAME = os.getenv("DB_NAME")

    @classmethod
    def connection(cls):
        try:
            conn = psycopg2.connect(
                user=cls.USER,
                password=cls.PASSWORD,
                host=cls.HOST,
                port=cls.PORT,
                dbname=cls.DBNAME
            )
            return conn
        except Exception as e:
            print(f"Failed to connect: {e}")
            return None  # Restituisci None se la connessione fallisce

    @classmethod
    def addRecord(cls, nome, litri):
        conn = cls.connection()
        
        if conn is None:
            print("Connessione al database fallita.")
            return  # Interrompe l'esecuzione se la connessione fallisce

        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO records(nome, quantity) VALUES (%s, %s)", (nome, litri))
            conn.commit()
        except Exception as e:
            print("Errore:", e)
        finally:
            conn.close()


# if __name__ == "__main__": 

#     Database.connection()
#     Database.addRecord('gian', '2')
