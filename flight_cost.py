#Tämän funktion on tarkoitus laskea kaikki lennosta aiheutuvat kulut

import mysql.connector
from geopy import distance
#hinta_per_km on kätevämpi muuttaa, jos se on globaali muuttuja
hinta_per_km = 0.4
yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='osku',
         password='1230',
         autocommit=True
         )
player_id=3
seuraava_kentta = "'00AA'"

def flight_cost(seuraava_kentta):
    kursori = yhteys.cursor()
    sql = f"SELECT latitude_deg, longitude_deg, type FROM airport WHERE ident = (SELECT location FROM game WHERE id = {player_id})OR ident = {seuraava_kentta}"
    kursori.execute(sql)
    tulos = kursori.fetchall()
    lentokenttä_etäisyys = {}
    lista_avain = 0
    for number in tulos:
        lentokenttä_etäisyys[lista_avain] = number[0], number[1]
        lista_avain += 1
    #.km lopussa jättää vastauksesta km pois, milloin saadaan muunnettua muuttuja int-muotoon
    laskettu_matka = int(distance.distance(lentokenttä_etäisyys[0], lentokenttä_etäisyys[1]).km)
    #Haen seuraavan kentän [-1] tuplesta viimeisen arvon [-1]
    airport_type = tulos[-1][-1]
    if airport_type == "small_airport": 
        landing = 400
    elif airport_type == "medium_airport":
        landing = 600
    elif airport_type == "large_airport":
        landing = 800
    cost = laskettu_matka * hinta_per_km + landing
    return cost
#Testaus
tuotto=1000
print(f"{flight_cost(seuraava_kentta)+tuotto:.0f}")