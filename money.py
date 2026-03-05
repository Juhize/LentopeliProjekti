#Funktioon tarvitaan rakenne, joka mittaa etäisyyttä lentokenttien välillä, minkä mukaan lisätään menoihin lennon pituudesta riippuva elementti 
# -Varmaan pienennän kiinteitä lentokenttämaksuja tämän jälkeen
#Tehdään vielä uusi funktio, mikä laskee lentokenttien etäisyyden 
#ja ilmoittaa pelaajalle lennon kokonaiskustannuksen
#Uutta funktiota käytetään tämän funktion laskutoimituksessa


import random
import mysql.connector
#Pääohjelma hakee player_id:n ja voisi hakea myös Flight_counterin
player_id = 1
Flight_counter = 0
#Pääohjelmassa aiemmin toteutettava funktio palauttaa 3 eri kokoista lentokenttää
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
#Mysteeri syystä ilman pyöristystä luvusta saadaan enemmän desimaaleja, kun pitäisi.
    CO2Tax = round(1 - (Flight_counter // 3 * 0.2), 1)
    CO2Tax = max(0.2, CO2Tax)
    kursori = yhteys.cursor()
    kursori.execute(f"SELECT balance FROM game WHERE id = {player_id}")
    tulos = kursori.fetchone()
    if lentokentta == 1:
        tuotto = tulos[0] + random.randint(200,1000) * CO2Tax - 400
    elif lentokentta == 2:
        tuotto = tulos[0] + random.randint(300,1500) * CO2Tax - 600
    elif lentokentta == 3:
        tuotto = tulos[0] + random.randint(400,2000) * CO2Tax - 800
    Flight_counter += 1
    kursori.execute(f'UPDATE game SET balance = {int(tuotto)}, flights = {int(Flight_counter)} WHERE id={player_id}')
    return int(tuotto), Flight_counter

#Seuraava on testausta varten
while Flight_counter < 17:
    tuotto, Flight_counter = money(lentokentta, Flight_counter)

    print(f"Kierroksen tuotto: {tuotto, Flight_counter}")