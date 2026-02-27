import mysql.connector

def tallenna_sijainti(game_id, airport_id):
    sql = f"UPDATE game SET location = '{airport_id}' WHERE id = {game_id}"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    yhteys.commit()

def lento_kentät(nimi):
    tulos = []

    sql1 = f"SELECT airport.ident, airport.name, airport.type FROM airport JOIN country ON country.iso_country = airport.iso_country WHERE country.name = '{nimi}' and airport.type = 'small_airport' order by rand() limit 1"
    kenttä1 = yhteys.cursor()
    kenttä1.execute(sql1)
    pieni = kenttä1.fetchall()

    sql2 = f"SELECT airport.ident, airport.name, airport.type FROM airport JOIN country ON country.iso_country = airport.iso_country WHERE country.name = '{nimi}' and airport.type = 'medium_airport' order by rand() limit 1"
    kenttä2 = yhteys.cursor()
    kenttä2.execute(sql2)
    keski = kenttä2.fetchall()

    sql3 = f"SELECT airport.ident, airport.name, airport.type FROM airport JOIN country ON country.iso_country = airport.iso_country WHERE country.name = '{nimi}' and airport.type = 'large_airport' order by rand() limit 1"
    kenttä3 = yhteys.cursor()
    kenttä3.execute(sql3)
    iso = kenttä3.fetchall()

    tulos = pieni + keski + iso

    for i in range(len(tulos)):
        print(f"{i + 1}. {tulos[i][1]}: {tulos[i][0]}")

    return tulos

def valitse(tulos, numero, game_id):
    if numero < 1 or numero > len(tulos):
        print("Virheellinen valinta.")
        return None
    valittu_kenttä = tulos[numero - 1]
    tallenna_sijainti(game_id, valittu_kenttä[0])
    print(f"\nTervetuloa lentokentälle: {valittu_kenttä[0]}!")
    return valittu_kenttä

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='',
         autocommit=True
         )

maan_nimi = ""
tulos = []

while not tulos:
    maan_nimi = input("Anna maan nimi: ")
    tulos = lento_kentät(maan_nimi)
    if not tulos:
        print("Maata ei löydy")

if tulos:
    lentokentta = int(input("Mille lentokentälle haluat mennä? (1-3): "))
    #seuraavan rivin lopussa numero "1" on game_id ja sen voi muuttaa käyttäjän muuttuvaksi game_id
    kentta = valitse(tulos, lentokentta, 1)

