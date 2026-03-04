import mysql.connector

def lento_kentät(nimi):

    sql = (f"(SELECT airport.name, airport.type FROM airport JOIN country ON country.iso_country = airport.iso_country WHERE country.name = '{nimi}' and airport.type = 'small_airport' order by rand() limit 1) union all "
           f"(SELECT airport.name, airport.type FROM airport JOIN country ON country.iso_country = airport.iso_country WHERE country.name = '{nimi}' and airport.type = 'medium_airport' order by rand() limit 1) union all "
           f"(SELECT airport.name, airport.type FROM airport JOIN country ON country.iso_country = airport.iso_country WHERE country.name = '{nimi}' and airport.type = 'large_airport' order by rand() limit 1);")

    kenttä = yhteys.cursor()
    kenttä.execute(sql)
    tulos = kenttä.fetchall()
    if kenttä.rowcount >0 :
        for rivi in tulos:
            print(f"{rivi[1]}: {rivi[0]}")
    return tulos
yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='osku',
         password='1230',
         autocommit=True
         )

maan_nimi = input("Anna maan nimi: ")
tulos = lento_kentät(maan_nimi)
print(tulos)
