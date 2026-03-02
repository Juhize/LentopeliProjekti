def peli_valikko():

    # Tehdään muuttuja nimellä "silmukka" sitä varten, jos tietokannassa ei ole käyttäjiä ja pelaaja koittaa
    # jatkaa käyttäjänimellä peliä jolloin ohjelma kutsuu tätä samaa funktioo uudelleen ja saadaan silmukka aikaiseksi
    silmukka = True
    valinta = input("\n1. Aloita uusi peli\n2. Jatka tallenettua peli\n3. Poistu\n")
    creation = yhteys_sql.cursor()

    # Tässä if lausekkeessa varmistamme, että pelaaja antaa 1, 2 tai 3 komennon ja muuttaa merkkijonosta numeroksi, jos näin on
    if valinta in ["1", "2", "3"]:
        valinta = int(valinta)

    # Tässä tehdään while loop jos aikaisempi if lause ei täyty ja annettu input ei ole valikossa
    # Tällä while loppilla voimme vällttää ohelman kaatumisen, jos pelaaja antaa väärän komennon ja kysyy uudelleen komentoa
    while valinta not in [1, 2, 3]:
         valinta = input("Tuntematon komento anna uusi komento\n1. Aloita uusi peli\n2. Jatka tallenettua peli\n3. Poistu\n")
         if valinta in ["1", "2", "3"]:
             valinta = int(valinta)

    if valinta == 1:
         # Valinta 1 teemme olio ohjelman, joka suorittaa SQL lausekkeen, jossa se lisää uuden pelaajan tietokantaan
         annettu_player_name = input ("Anna käyttäjälle nimi: ")
         # Tässä teemme SQL testin ja luomme listan jossa tarkistamme onko käyttäjänimi jo olemassa
         sql_testi = ("select screen_name from game")
         creation.execute(sql_testi)
         player_lista = creation.fetchall()

         # Tässä luomme uuden listan, koska SQL palaava lista on tuple eikä merkkijono
         player_tarkistus = [names[0] for names in player_lista]
         if creation.rowcount > 0:
             # Tässä luotu player_tarkistus lista tarkistetaan onko olevassa olevaa nimeä jo relaatiokannassa
             while annettu_player_name in player_tarkistus:
                 print("Pelaaja nimi on jo käytössä")
                 annettu_player_name = input("Anna toinen nimi: ")

         # Käytetään commit() lauseketta, koska käytämme INSERT:tiä ja haluamme tallentaa pelaajan, joka on luotu
         sql = (f"insert into game(screen_name) VALUES ('{annettu_player_name}');")
         print (f"Pelaaja luotu nimellä: {annettu_player_name}")
         creation.execute(sql)
         yhteys_sql.commit()

    elif valinta == 2:
          # Tässä tulostamme listan pelaajista ja pelaaja voi valita käyttäjän
          sql_lista = ("select screen_name from game")
          creation.execute(sql_lista)
          player_lista = creation.fetchall()
          player_lista_siisti = [names[0] for names in player_lista]
          listassa_pelaajia = False
          if creation.rowcount > 0:
              print ("Valitse käyttäjä vastaavalla numerolla listassa:")
              # Tässä luomme listan pelaajista relaatiokannassa ja jokaiselle valinalle annamme ideksin len tulolla
              pelaaja_lista_numeroina = []
              for numero in range (len(player_lista_siisti)):
                  print (f"{numero + 1}. {player_lista_siisti[numero]}")
                  pelaaja_lista_numeroina.append (numero + 1)
                  listassa_pelaajia = True
              pelaajan_valinta = int(input(""))
              while pelaajan_valinta not in pelaaja_lista_numeroina:
                  pelaajan_valinta = int(input("Käyttäjä numeroa ei ole anna uusi:\n"))

              if pelaajan_valinta in pelaaja_lista_numeroina:
                  annettu_player_name = (player_lista_siisti[pelaajan_valinta - 1])
          if not listassa_pelaajia:
              print("Ei tallennettuja käyttäjiä")
              silmukka = False

    elif valinta == 3:
          print ("Peli suljettu, Hei hei")
          annettu_player_name = ""
    if not silmukka:
        # Tällä funktion kutsulla vältämme, jos pelaaja koittaa jatkaa peliä
        # vaikka relaatiokannassa ei ole käyttäjiä
        peli_valikko()
    return annettu_player_name


def tallenna_sijainti(player_name, airport_id):
    sql = f"UPDATE game SET location = '{airport_id}' where screen_name = '{player_name}'"
    kursori = yhteys_sql.cursor()
    kursori.execute(sql)
    yhteys_sql.commit()

def lento_kentät(nimi):
    tulos = []

    sql1 = f"SELECT airport.ident, airport.name, airport.type FROM airport JOIN country ON country.iso_country = airport.iso_country WHERE country.name = '{nimi}' and airport.type = 'small_airport' order by rand() limit 1"
    kenttä1 = yhteys_sql.cursor()
    kenttä1.execute(sql1)
    pieni = kenttä1.fetchall()

    sql2 = f"SELECT airport.ident, airport.name, airport.type FROM airport JOIN country ON country.iso_country = airport.iso_country WHERE country.name = '{nimi}' and airport.type = 'medium_airport' order by rand() limit 1"
    kenttä2 = yhteys_sql.cursor()
    kenttä2.execute(sql2)
    keski = kenttä2.fetchall()

    sql3 = f"SELECT airport.ident, airport.name, airport.type FROM airport JOIN country ON country.iso_country = airport.iso_country WHERE country.name = '{nimi}' and airport.type = 'large_airport' order by rand() limit 1"
    kenttä3 = yhteys_sql.cursor()
    kenttä3.execute(sql3)
    iso = kenttä3.fetchall()

    tulos = pieni + keski + iso

    for i in range(len(tulos)):
        print(f"{i + 1}. {tulos[i][1]} {tulos[i][0]}")

    return tulos

def valitse(tulos, numero, player_name):
    if numero < 1 or numero > len(tulos):
        print("Virheellinen valinta.")
        return None
    valittu_kenttä = tulos[numero - 1]
    tallenna_sijainti(player_name, valittu_kenttä[0])
    lentokenttä_1 = yhteys_sql.cursor()
    sql_kentän_nimi = (f"select airport.name from airport inner join game on location = ident where screen_name = '{player_name}'")
    lentokenttä_1.execute(sql_kentän_nimi)
    lentokenttä_sijainti = lentokenttä_1.fetchall()
    sijainti_siisti = [names[0] for names in lentokenttä_sijainti]
    print(f"\nTervetuloa lentokentälle: {sijainti_siisti[0]}!")
    return valittu_kenttä

import mysql.connector

yhteys_sql = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='',
         autocommit=True
         )

maan_nimi = ""
tulos = []
player_name = peli_valikko()
print (f"Pelaat nyt käyttäjällä: {player_name}")

while not tulos:
    maan_nimi = input("Anna maan nimi: ")
    tulos = lento_kentät(maan_nimi)
    if not tulos:
        print("Maata ei löydy")

if tulos:
    lentokentta = int(input("Mille lentokentälle haluat mennä? (1 = Pieni, 2 = Keskikokoinen, 3 = Iso): "))
    kentta = valitse(tulos, lentokentta, player_name)
