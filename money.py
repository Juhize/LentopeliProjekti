#Puuttuu lennettyjen lentojen määrän haku tietokannasta
#Funktioon tarvitaan rakenne, joka mittaa etäisyyttä lentokenttien välillä, minkä mukaan lisätään menoihin lennon pituudesta riippuva elementti 
# -Varmaan pienennän kiinteitä lentokenttämaksuja tämän jälkeen
#Puuttuu lentojen määrän päivitys tietokantaan

import random
import mysql.connector
#Seuraavat 2 riviä on testausta varten
#   -current_id olisi kyllä hyvä globaaliksi muuttujaksi, sehän ei muutu kesken pelin
current_id = 1
lentokentta = 2
yhteys = mysql.connector.connect(
host='127.0.0.1',
port= 3306,
database='flight_game',
user='osku',
password='1230',
autocommit=True
)

def money(lentokentta, Flight_counter):
    CO2Tax = 1 - (Flight_counter //3*0.2)
    sql = f"SELECT balance FROM game WHERE id = {current_id}"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchone()
    if lentokentta == 1:
        tuotto = tulos[0] + random.randint(200,1000) * CO2Tax - 400
    elif lentokentta == 2:
        tuotto = tulos[0] + random.randint(300,1500) * CO2Tax - 600
    elif lentokentta == 3:
        tuotto = tulos[0] + random.randint(400,2000) * CO2Tax - 800
    Flight_counter +=1
    kursori.execute(f'UPDATE game SET balance = {tuotto} WHERE id={current_id}')
    return int(tuotto), Flight_counter
#Seuraava on testausta varten
Flight_counter= 0
while Flight_counter < 12:
    tuotto, Flight_counter = money(lentokentta, Flight_counter)

    print(f"Kierroksen tuotto: {tuotto, Flight_counter}")