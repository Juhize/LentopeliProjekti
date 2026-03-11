def continent_tarkistus(player_name):
    creation = yhteys_sql.cursor()
    # Tässä funktiossa käymme ensin etsimässä pelaajan nykyisen mantereen, jossa hän on ja muutamme sen listasta yksitäiseksi merkkijonoksi
    sql_continent_player = (
    f"select country.continent from country inner join airport on airport.iso_country = country.iso_country inner join game on location = ident where screen_name = '{player_name}';")
    creation.execute(sql_continent_player)
    player_continent_1 = creation.fetchall()
    player_continent = [continent[0] for continent in player_continent_1]
    player_continent = player_continent[0]

    # Tässä seuraavasti etsimme goal_reached listasta kaikki continentit, joissa pelaaja on käynyt tallentamallamme player_id muuttujalla
    player_id = luonti_player_id.player_id_finder(player_name)
    sql_continent_tarkistus = (f"select continent_id from goal_reached where game_id = '{player_id}';")
    creation.execute(sql_continent_tarkistus)
    sql_player_continent = creation.fetchall()
    sql_continent_lista = [continent[0] for continent in sql_player_continent]
    # Jos pelaajan nykyinen continent missä hän on ei ole tallenettu vielä goal_reachediin niin se lisätään sinne, jos se on jo tämä koko if lause ohitetaan
    if player_continent not in sql_continent_lista:
        sql_continent_lisäys = f"insert into goal_reached(game_id, continent_id) values('{player_id}', '{player_continent}');"
        creation.execute(sql_continent_lisäys)
        print("Saavuit mantereelle, jossa et ole käynyt aikaisemmin!\n")
    else:
        print("")

def continent_lista(player_id):
    creation = yhteys_sql.cursor()
    sql_haku = (f"select continent_id from goal_reached where game_id = '{player_id}';")
    creation.execute(sql_haku)
    continent_lista_1 = creation.fetchall()
    print("Mantereet joissa olet käynyt: ")
    # Teemme muutokset printatuille mantereille tässä sanakirjalla, jotta se olisi peleejalle selkeämpää
    # Tässä voisi myös käyttää if/elif lauseena mutta sanakirjalla saadaan tiivimmäksi ja lyhyemmäksi
    continent_names = {
        "EU": "Eurooppa",
        "AF": "Afrikka",
        "AS": "Aasia",
        "NA": "Pohjois-Amerikka",
        "SA": "Etelä-Amerikka",
        "AN": "Antarktis",
        "OC": "Australia ja Oseania",
    }
    for name in continent_lista_1:
        print(continent_names[name[0]])
    print("")

import luonti_player_id
import mysql.connector

yhteys_sql = mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    database='flight_game',
    user='osku',
    password='1230',
    autocommit=True
    )
