def peli_valikko():
    # Tehdään muuttuja nimellä "silmukka" sitä varten, jos tietokannassa ei ole käyttäjiä ja pelaaja koittaa
    # jatkaa käyttäjänimellä peliä jolloin ohjelma kutsuu tätä samaa funktioo uudelleen ja saadaan silmukka aikaiseksi
    silmukka = True
    tehty_käyttäjä = False
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
         # Tässä luotu player_tarkistus lista tarkistetaan onko olevassa olevaa nimeä jo relaatiokannassa
         while annettu_player_name in player_tarkistus:
             print("Pelaaja nimi on jo käytössä")
             annettu_player_name = input("Anna toinen nimi: ")

         sql = (f"insert into game(screen_name) VALUES ('{annettu_player_name}');")
         print (f"Pelaaja luotu nimellä: {annettu_player_name}\n")
         creation.execute(sql)

         player_id = player_id_finder(annettu_player_name)

         aloitus_maa = input ("Valitse aloitus maa vastaavalla numerolla:\n1. Brazilia\n2. USA\n3. Japani\n4. Eqypti\n5. Suomi\n")
         while aloitus_maa not in ["1", "2", "3", "4", "5"]:
             aloitus_maa = input ("Virheellinen valinta anna uudelleen")
         if aloitus_maa in ["1", "2", "3", "4", "5"]:
             aloitus_maa = int(aloitus_maa)
             tehty_käyttäjä = True
         if aloitus_maa == 1:
             sql_aloitus_maa = f"UPDATE game SET location = 'SBGR' where screen_name = '{annettu_player_name}'"
             sql_aloitus_manner = f"insert into goal_reached(game_id, continent_id) values('{player_id}', 'SA')"
             creation.execute(sql_aloitus_maa)
             creation.execute(sql_aloitus_manner)
         elif aloitus_maa == 2:
             sql_aloitus_maa = f"UPDATE game SET location = 'KDFW' where screen_name = '{annettu_player_name}'"
             sql_aloitus_manner = f"insert into goal_reached(game_id, continent_id) values('{player_id}', 'NA')"
             creation.execute(sql_aloitus_maa)
             creation.execute(sql_aloitus_manner)
         elif aloitus_maa == 3:
             sql_aloitus_maa = f"UPDATE game SET location = 'RJTT' where screen_name = '{annettu_player_name}'"
             sql_aloitus_manner = f"insert into goal_reached(game_id, continent_id) values('{player_id}', 'AS')"
             creation.execute(sql_aloitus_maa)
             creation.execute(sql_aloitus_manner)
         elif aloitus_maa == 4:
             sql_aloitus_maa = f"UPDATE game SET location = 'HECA' where screen_name = '{annettu_player_name}'"
             sql_aloitus_manner = f"insert into goal_reached(game_id, continent_id) values('{player_id}', 'AF')"
             creation.execute(sql_aloitus_maa)
             creation.execute(sql_aloitus_manner)
         elif aloitus_maa == 5:
             sql_aloitus_maa = f"UPDATE game SET location = 'EFHK' where screen_name = '{annettu_player_name}'"
             sql_aloitus_manner = f"insert into goal_reached(game_id, continent_id) values('{player_id}', 'EU')"
             creation.execute(sql_aloitus_maa)
             creation.execute(sql_aloitus_manner)

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
                  # Tämän listan luomisella voimme vältää, jos pelaaja antaa väärän inputin
                  pelaaja_lista_numeroina_str = [str(nimi) for nimi in pelaaja_lista_numeroina]
              pelaajan_valinta = input("")
              while pelaajan_valinta not in pelaaja_lista_numeroina_str:
                  pelaajan_valinta = input("Käyttäjä numeroa ei ole anna uusi:\n")

              if pelaajan_valinta in pelaaja_lista_numeroina_str:
                  pelaajan_valinta = int(pelaajan_valinta)
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
        annettu_player_name = ""
        peli_valikko()
    if tehty_käyttäjä == True:
        sql_haku = (f"select balance from game where screen_name = '{annettu_player_name}';")
        creation.execute(sql_haku)
        tilanne = creation.fetchall()
        print(f"Aloitus raha määrä: {tilanne[0][0]}€")
    return annettu_player_name


def tallenna_sijainti(player_name, airport_id):
    sql = f"UPDATE game SET location = '{airport_id}' where screen_name = '{player_name}'"
    kursori = yhteys_sql.cursor()
    kursori.execute(sql)
    yhteys_sql.commit()

def flight_cost(seuraava_kentta):
    #Seuraavassa haetaan erikseen kummankin lentokentän koordinaatit ja kohde lentokentän kokotyyppi
    #Jouduin erittelemään haut, koska alkuperäisessä haun tuloksien järjestys vaihteli
    sql1 = f"SELECT latitude_deg, longitude_deg FROM airport WHERE ident = (SELECT location FROM game WHERE id = {player_id})"
    sql2 = f"SELECT latitude_deg, longitude_deg, type FROM airport WHERE ident = '{seuraava_kentta}'"
    creation.execute(sql1)
    kentta_1 = creation.fetchall()
    creation.execute(sql2)
    kentta_2 = creation.fetchall()
    tulos = kentta_1, kentta_2
    piste = {}
    lista_avain = 0
    for number in tulos:
    #Nyt kun yhdistettiin 2 listaa tarvitaan ensiksi ideksi listaan ja sen jälkeen haettavaan arvoon
        piste[lista_avain] = number[0][0], number[0][1]
        lista_avain += 1
    #.km lopussa jättää vastauksesta km pois, milloin saadaan muunnettua muuttuja int-muotoon
    laskettu_matka = int(distance.distance(piste[0], piste[1]).km)
    airport_type = kentta_2[0][-1]
    if airport_type == "small_airport":
        landing = 400
    elif airport_type == "medium_airport":
        landing = 600
    elif airport_type == "large_airport":
        landing = 800
    cost = laskettu_matka * hinta_per_km + landing
    return int(cost)

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
        print(f"{i + 1}. {tulos[i][1]}. Lennon hinta: {(flight_cost(tulos[i][0]))}€")

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
    print(f"\nTervetuloa lentokentälle: {lentokenttä_sijainti[0][0]}!")
    return valittu_kenttä

def continent_tarkistus(player_name):
    # Tässä funktiossa käymme ensin etsimässä pelaajan nykyisen mantereen, jossa hän on ja muutamme sen listasta yksitäiseksi merkkijonoksi
    sql_continent_player = (f"select country.continent from country inner join airport on airport.iso_country = country.iso_country inner join game on location = ident where screen_name = '{player_name}';")
    creation.execute(sql_continent_player)
    player_continent_1 = creation.fetchall()
    player_continent = [continent[0] for continent in player_continent_1]
    player_continent = player_continent[0]

    # Tässä seuraavasti etsimme goal_reached listasta kaikki continentit, joissa pelaaja on käynyt tallentamallamme player_id muuttujalla
    sql_continent_tarkistus = (f"select continent_id from goal_reached where game_id = '{player_id}';")
    creation.execute(sql_continent_tarkistus)
    sql_player_continent = creation.fetchall()
    sql_continent_lista = [continent[0] for continent in sql_player_continent]
    # Jos pelaajan nykyinen continent missä hän on ei ole tallenettu vielä goal_reachediin niin se lisätään sinne, jos se on jo tämä koko if lause ohitetaan
    if player_continent not in sql_continent_lista:
        sql_continent_lisäys = f"insert into goal_reached(game_id, continent_id) values('{player_id}', '{player_continent}');"
        creation.execute(sql_continent_lisäys)
        print("Saavuit uudelle mantereelle, jossa et ole käynyt aikaisemmin\n")
    else:
        print("")

def nykyinen_pelaajan_lentokenttä():
    # Tässä funktiossa etsimme pelaajan valitsemalla käyttäjänimellä hänen nykyisen sijainti ja ilmoitamme sen, kun hän aloittaa pelaamisen
    # Printtaus tehdään funktion sisällä tässä
    sql_sijainti = f"select country.name, airport.name from country inner join airport on country.iso_country = airport.iso_country inner join game on location = ident where screen_name = '{player_name}';"
    creation.execute(sql_sijainti)
    sql_sijainti_paikat = creation.fetchall()
    for names in sql_sijainti_paikat:
        print (f"Olet tällä hetkellä maassa: {names[0]}\nLentokenttällä: {names[1]}\n")

def player_id_finder(player_name):
    # Tällä koodilla saamme koko ohjelmalle globaalin player_id, jotta peli voi hakea sitä jatkossa, jos on tarve
    player_id = f"select game.id from game where screen_name = ('{player_name}')"
    creation.execute(player_id)
    playerid = creation.fetchall()
    player_id = [id[0] for id in playerid]
    player_id = player_id[0]
    return player_id

def lentokenttä_arpoja():
    maan_nimi = ""
    tulos = []
    while not tulos:
        maan_nimi = input("Anna maan nimi: ")
        tulos = lento_kentät(maan_nimi)
        if not tulos:
            print("Maata ei löydy")
            break
        elif tulos:
            lentokentta = int(input("Mille lentokentälle haluat mennä? (1-3): "))
            kentta = valitse(tulos, lentokentta, player_name)

################

import mysql.connector
import random
from geopy import distance

yhteys_sql = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='123456789',
    autocommit=True
)

peli_käynnissä = True
creation = yhteys_sql.cursor()

player_name = peli_valikko()
hinta_per_km = 0.4

if player_name == "":
    peli_käynnissä = False

if peli_käynnissä == True:
    player_id = player_id_finder(player_name)
    print(f"Pelaat nyt käyttäjällä: {player_name}")
    nykyinen_lentokenttä = nykyinen_pelaajan_lentokenttä()




def tarkista_peli_loppu(player_id, yhteys_sql):

    kursori = yhteys_sql.cursor()

    sql_kontinentit = f"""
        SELECT COUNT(DISTINCT continent_id) 
        FROM goal_reached 
        WHERE game_id = {player_id}
    """
    kursori.execute(sql_kontinentit)
    kaydetyt_kontinentit = kursori.fetchone()[0]

    # Maailmassa on 7 kontinenttia
    if kaydetyt_kontinentit >= 7:
        return True
    return False


def haet_pelaajan_tiedot(player_id, yhteys_sql):

    kursori = yhteys_sql.cursor()

    sql = f"""
        SELECT screen_name, balance, flights 
        FROM game 
        WHERE id = {player_id}
    """
    kursori.execute(sql)
    tulos = kursori.fetchone()

    if tulos:
        return {
            "nimi": tulos[0],
            "saldo": tulos[1],
            "lennot": tulos[2]
        }

    return None


def nayta_voittoruutu(pelaajan_nimi, saldo, kontinentit_kayty, yhteys_sql):

    print("\n" + "=" * 60)
    print("Onneksi olkoon!".center(60))
    print("=" * 60)
    print(f"\nPelaaja: {pelaajan_nimi}")
    print(f"Sinä olet onnistuneesti kiertänyt maailman ympäri!")
    print(f"\nPelitilastot:")
    print(f"   • Käydyt kontinentit: {kontinentit_kayty}/7")
    print(f"   • Jäljellä oleva saldo: {saldo} CO2")
    print(f"   • Status: Voittaja!")
    print("\n" + "=" * 60)


def nayta_highscore_lista(yhteys_sql):

    kursori = yhteys_sql.cursor()

    sql = "SELECT screen_name, balance, flights FROM game ORDER BY balance DESC LIMIT 10"

    try:
        kursori.execute(sql)
        tulokset = kursori.fetchall()

        if tulokset:
            print("\n" + "=" * 60)
            print("HIGHSCORE TAULUKKO".center(60))
            print("=" * 60)
            print("#  Pelaaja                   Saldo      Lennot")
            print("-" * 60)

            for idx, (nimi, saldo, lennot) in enumerate(tulokset, 1):
                print(f"{idx}  {nimi:<25} {saldo}      {lennot}")

            print("=" * 60 + "\n")
        else:
            print("Ei vielä highscores!")

    except Exception as err:
        print(f"Virhe highscoren haussa: {err}")


def kysytaan_uusi_peli():

    valinta = input("\nHaluatko pelata uudelleen? (1 = Kyllä, 2 = Ei): ")

    while valinta not in ["1", "2"]:
        valinta = input("Virheellinen valinta. Anna 1 tai 2: ")

    return valinta == "1"


def tarkista_lopettaminen(player_id, yhteys_sql):
    kursori = yhteys_sql.cursor()

    sql = f"""
        SELECT balance, flights 
        FROM game 
        WHERE id = {player_id}
    """
    kursori.execute(sql)
    tulos = kursori.fetchone()

    if tulos:
        saldo, lennot = tulos

        # Jos saldo on alle 0, peli loppuu
        if saldo < 0:
            return True, "saldo"

        # Jos lennot ovat 0 eikä rahaa lisää, peli loppuu
        if lennot == 0 and saldo < 50:
            return True, "lennot"

    return False, None


def nayta_tappio_ruutu(pelaajan_nimi, syy):
    print("\n" + "=" * 60)
    print("PELI PÄÄTTYI".center(60))
    print("=" * 60)
    print(f"\nPelaaja: {pelaajan_nimi}")

    if syy == "saldo":
        print("Loppuivat CO2-yksiköt! Sinulla ei ole enää rahaa lennoksille.")
    elif syy == "lennot":
        print("Loppuivat lennot! Sinulla ei ole enää rahaa matkalipuille.")

    print("\nEi hätää, yritä uudelleen!")
    print("=" * 60)




while peli_käynnissä == True:
    valinta = input(
        "Valitse toiminto:\n1. Valitse uusi lentokenttä mihin lentää:\n2. Näytä Nykyinen sijainti ja raha tilanne:\n3. Näytä mantereet missä olet käynyt:\n4. Poistu pelistä:\n")
    while valinta not in ["1", "2", "3", "4"]:
        valinta = input("Tuntematon toiminto. Valitse uudelleen\n")
    if valinta in ["1", "2", "3", "4"]:
        valinta = int(valinta)

    if valinta == 1:
        lentokenttä_arpoja()
        continent_tarkistus(player_name)

        try:
            if tarkista_peli_loppu(player_id, yhteys_sql):
                pelaajan_tiedot = haet_pelaajan_tiedot(player_id, yhteys_sql)
                if pelaajan_tiedot:
                    nayta_voittoruutu(
                        pelaajan_tiedot["nimi"],
                        pelaajan_tiedot["saldo"],
                        7,
                        yhteys_sql
                    )
                nayta_highscore_lista(yhteys_sql)

                if kysytaan_uusi_peli():
                    peli_käynnissä = False
                else:
                    peli_käynnissä = False
        except Exception as e:
            print(f"Virhe voitto-tarkistuksessa: {e}")

        # ===== TARKISTA HÄVIÖ (resurssit loppu) =====
        if peli_käynnissä == True:  # Tarkista vain jos peli ei ole vielä loppu
            try:
                pitaa_lopettaa, syy = tarkista_lopettaminen(player_id, yhteys_sql)

                if pitaa_lopettaa:
                    pelaajan_tiedot = haet_pelaajan_tiedot(player_id, yhteys_sql)

                    if pelaajan_tiedot:
                        nayta_tappio_ruutu(pelaajan_tiedot["nimi"], syy)

                    nayta_highscore_lista(yhteys_sql)

                    if kysytaan_uusi_peli():
                        peli_käynnissä = False
                    else:
                        peli_käynnissä = False
            except Exception as e:
                print(f"Virhe häviö-tarkistuksessa: {e}")

    elif valinta == 2:
        sql_sijainti = f"select country.name, airport.name from country inner join airport on country.iso_country = airport.iso_country inner join game on location = ident where screen_name = '{player_name}';"
        creation.execute(sql_sijainti)
        sql_sijainti_paikat = creation.fetchall()
        for names in sql_sijainti_paikat:
            print(f"Olet tällä hetkellä maassa: {names[0]}\nLentokenttällä: {names[1]}")
        sql_haku = (f"select balance from game where screen_name = '{player_name}';")
        creation.execute(sql_haku)
        tilanne = creation.fetchall()
        print(f"Raha tilanne: {tilanne[0][0]}€\n")

    elif valinta == 3:
        sql_haku = (f"select continent_id from goal_reached where game_id = '{player_id}';")
        creation.execute(sql_haku)
        continent_lista_1 = creation.fetchall()
        for name in continent_lista_1:
            print(name[0])
        print("")

    elif valinta == 4:
        peli_käynnissä = False
        nayta_highscore_lista(yhteys_sql)
        print("Peli suljettu. Hei hei")
    else:
        print("Tuntematon toiminto\n")