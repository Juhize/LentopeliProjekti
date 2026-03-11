def player_id_finder(player_name):
    creation = yhteys_sql.cursor()
    # Tällä koodilla saamme koko ohjelmalle globaalin player_id, jotta peli voi hakea sitä jatkossa, jos on tarve
    player_id = f"select game.id from game where screen_name = ('{player_name}')"
    creation.execute(player_id)
    playerid = creation.fetchall()
    player_id = [id[0] for id in playerid]
    player_id = player_id[0]
    return player_id

def peli_valikko():
    creation = yhteys_sql.cursor()
    # Tehdään muuttuja nimellä "silmukka" sitä varten, jos tietokannassa ei ole käyttäjiä ja pelaaja koittaa
    # jatkaa käyttäjänimellä peliä jolloin ohjelma kutsuu tätä samaa funktioo uudelleen ja saadaan silmukka aikaiseksi
    silmukka = True
    tehty_käyttäjä = False
    valinta = input("\n1. Aloita uusi peli\n2. Jatka tallenettua peli\n3. Poistu\n")

    # Tällä while loppilla voimme vällttää ohelman kaatumisen, jos pelaaja antaa väärän komennon ja kysyy uudelleen komentoa
    while valinta not in ["1", "2", "3"]:
        valinta = input(
            "Tuntematon komento anna uusi komento\n1. Aloita uusi peli\n2. Jatka tallenettua peli\n3. Poistu\n")

    if valinta == "1":
        # Valinta 1 teemme olio ohjelman, joka suorittaa SQL lausekkeen, jossa se lisää uuden pelaajan tietokantaan
        annettu_player_name = input("Anna käyttäjälle nimi: ")
        while annettu_player_name == "":
            annettu_player_name = input("Tyhjä nimi ei käy\nAnna käyttäjälle nimi: ")
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
        print(f"Pelaaja luotu nimellä: {annettu_player_name}\n")
        creation.execute(sql)

        # Tässä kohdassa haemme valmiiksi pelaajan game_id, jonka relaatiokanta loi automaattisesti screen_name luotua tulevaa toimia varten
        player_id = player_id_finder(annettu_player_name)

        aloitus_maa = input(
            "Valitse aloitus maa vastaavalla numerolla:\n1. Brazilia\n2. USA\n3. Japani\n4. Egypti\n5. Suomi\n")

        # Tällä while loopilla vältämme pelaajan väärät inputit ja pelaaja pääsee antamaan uudelleen inputin
        while aloitus_maa not in ["1", "2", "3", "4", "5"]:
            aloitus_maa = input("Virheellinen valinta anna uudelleen: ")

        # Tässä kohdassa luomme sanakirjan, jossa sanakirjan numero "avain" vastaa lentokenttä koodia ja manteretta
        # Aloitus lentokentät ja mantereet ovat jo tiedossa
        maat = {
            "1": ("SBGR", "SA"),
            "2": ("KDFW", "NA"),
            "3": ("RJTT", "AS"),
            "4": ("HECA", "AF"),
            "5": ("EFHK", "EU")
        }
        # Tässä luomme muuttujat aikaisemmasta sanakirjasta tehdystä valinnasta. Muutetaan monikko lista osat 2 eri muuttujaan tällä
        location, continent = maat[aloitus_maa]
        # Tämän jälkeen voimme updatee pelaajan sijainnin ja lisää goal_reached tauluun mantere, josta pelaaja aloittaa
        sql_aloitus_maa = f"UPDATE game SET location = '{location}' WHERE screen_name = '{annettu_player_name}'"
        sql_aloitus_manner = f"INSERT INTO goal_reached(game_id, continent_id) VALUES('{player_id}', '{continent}')"
        tehty_käyttäjä = True

    elif valinta == "2":
        # Tässä tulostamme listan pelaajista ja pelaaja voi valita käyttäjän
        sql_lista = ("select screen_name from game")
        creation.execute(sql_lista)
        player_lista = creation.fetchall()
        listassa_pelaajia = False
        if creation.rowcount > 0:
            print("Valitse käyttäjä vastaavalla numerolla listassa:")
            # Tässä luomme listan pelaajista relaatiokannassa ja jokaiselle valinalle annamme ideksin len tulolla
            pelaaja_lista_numeroina = []
            for numero in range(len(player_lista)):
                print(f"{numero + 1}. {player_lista[numero][0]}")
                pelaaja_lista_numeroina.append(numero + 1)

            # Tämän listan luomisella voimme vältää, jos pelaaja antaa väärän inputin
            pelaaja_lista_numeroina_str = [str(nimi) for nimi in pelaaja_lista_numeroina]
            pelaajan_valinta = input("")
            while pelaajan_valinta not in pelaaja_lista_numeroina_str:
                pelaajan_valinta = input("Käyttäjä numeroa ei ole anna uusi:\n")
            if pelaajan_valinta in pelaaja_lista_numeroina_str:
                pelaajan_valinta = int(pelaajan_valinta)
                listassa_pelaajia = True
                annettu_player_name = (player_lista[pelaajan_valinta - 1][0])
        if not listassa_pelaajia:
            print("Ei tallennettuja käyttäjiä")
            silmukka = False

    elif valinta == "3":
        annettu_player_name = ""
    if not silmukka:
        # Tällä funktion kutsulla vältämme, jos pelaaja koittaa jatkaa peliä
        # vaikka relaatiokannassa ei ole käyttäjiä
        annettu_player_name = ""
        peli_valikko()
    if tehty_käyttäjä == True:
        creation.execute(sql_aloitus_maa)
        creation.execute(sql_aloitus_manner)
        print('Pelissä lennetään rahtia ympäri maailmaa, minkä avulla on tarkoitus rahoittaa pelaajan matka viidelle eri mantereelle.' \
                    '\nPeli arpoo jokaisella kierroksella pelaajan valittavaksi 3 eri kokoista lentokenttää. Pelaaja saa rahaa vietyään rahtia lentokentälle lentokentän koon mukaan:\n1.Pieni kenttä:\nLaskeutuminen -400€\nTuotto: 200€ - 1000€\n2.Keskikokoinen kenttä:\nLaskeutuminen: -600€\nTuotto: 300€ - 1500€\n3.Suuri kenttä:\nLaskeutuminen -800€\nTuotto: 400€ - 2000€' \
                    '\nPelissä on kolmen lennon välein kutistuva päästökerroin 1 - 0.2, mikä vähentää pelaajalle kertyvää tuottoa kertoimen verran.' \
                    '\nMaavalinnassa maan nimi on ilmoitettava englanniksi.\n')
    return annettu_player_name

def uusi_pelin_aloitus(annettu_player_name):
    creation = yhteys_sql.cursor()
    player_id = player_id_finder(annettu_player_name)
    aloitus_maa = input(
        "Valitse aloitus maa vastaavalla numerolla:\n1. Brazilia\n2. USA\n3. Japani\n4. Egypti\n5. Suomi\n")
    while aloitus_maa not in ["1", "2", "3", "4", "5"]:
        aloitus_maa = input("Virheellinen valinta anna uudelleen: ")

    maat = {
        "1": ("SBGR", "SA"),
        "2": ("KDFW", "NA"),
        "3": ("RJTT", "AS"),
        "4": ("HECA", "AF"),
        "5": ("EFHK", "EU")
    }
    location, continent = maat[aloitus_maa]
    continent_id_delete = f"delete from goal_reached where game_id = '{player_id}'"
    sql_raha_reset = f"update game set balance = 2000 where screen_name = '{annettu_player_name}'"
    sql_flight_reset = f"update game set flights = 0 where screen_name = '{annettu_player_name}'"
    sql_aloitus_maa = f"UPDATE game SET location = '{location}' WHERE screen_name = '{annettu_player_name}'"
    sql_aloitus_manner = f"INSERT INTO goal_reached(game_id, continent_id) VALUES('{player_id}', '{continent}')"
    for suoritus in (continent_id_delete, sql_raha_reset, sql_flight_reset, sql_aloitus_maa, sql_aloitus_manner):
        creation.execute(suoritus)

import mysql.connector

yhteys_sql = mysql.connector.connect(
        host='127.0.0.1',
        port= 3306,
        database='flight_game',
        user='osku',
        password='1230',
        autocommit=True
        )
