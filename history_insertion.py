import requests
from connectionDB import Database
from dotenv import load_dotenv
import os

load_dotenv()

def get_info():

    conn = Database.connection()
    cur = conn.cursor()
    start = 2025
    cur.execute("SELECT COALESCE(SUM(quantity), 0) FROM records")
    actual = cur.fetchone()
    totale = round(start - actual[0], 0)
    
    api_key = os.getenv("API_KEY")

    api_url = 'https://api.api-ninjas.com/v1/historicalevents?year={}'.format(totale)
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)



if __name__ == "__main__":

    get_info()