#Tämän funktion on tarkoitus laskea kaikki lennosta aiheutuvat kulut

import mysql.connector
from geopy import distance

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='osku',
         password='1230',
         autocommit=True
         )
player_id=3
seuraava_kentta = "'EFHK'"

def matka_laskin(seuraava_kentta):
    kursori = yhteys.cursor()
    sql = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident = (SELECT location FROM game WHERE id = {player_id})OR ident = {seuraava_kentta}"
    kursori.execute(sql)
    tulos = kursori.fetchall()
    lentokenttä_etäisyys = {}
    lista_avain = 0
    for number in tulos:
        lentokenttä_etäisyys[lista_avain] = number[0], number[1]
        lista_avain += 1
    #.km lopussa jättää vastauksesta km pois, milloin saadaan muunnettua muuttuja int-muotoon
    laskettu_matka = int(distance.distance(lentokenttä_etäisyys[0], lentokenttä_etäisyys[1]).km)
    print(f"Lentokentien etäisyys on {laskettu_matka:.0f}")

matka_laskin(seuraava_kentta)