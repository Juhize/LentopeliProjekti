import mysql.connector

yhteys_sql = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='123456789',
         autocommit=True
         )

# Pelin lopetus siten että tarkistetaan onnistuminen maailman ympäri matkan

def tarkista_peli_loppu(player_id, yhteys_sql):

    #Tarkistaa, onko pelaaja käynyt kaikilla mantereilla

    kursori = yhteys_sql.cursor()

    # Haetaan kuinka monella mantereella pelaaja on käynyt
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

    #Hakee pelaajan nimen, tasapainon ja muut tarvittavat tiedot

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

    # Näyttää onnistumisen ruudun kun pelaaja on voittanut pelin

    print("\n" + "=" * 60)
    print("Onneksi olkoon!".center(60))
    print("=" * 60)
    print(f"\nPelaaja: {pelaajan_nimi}")
    print(f"Sinä olet onnistuneesti kiertänyt maailman ympäri!")
    print(f"\n Pelitilastot:")
    print(f"   • Käydyt kontinentit: {kontinentit_kayty}/7")
    print(f"   • Jäljellä oleva saldo: {saldo} CO2")
    print(f"   • Status: Voittaja! ")
    print("\n" + "=" * 60)





    # Hakee ja näyttää top 10 pelaajaa voittajien listasta


def nayta_highscore_lista(yhteys_sql):
    """Näytä highscore taulukko"""
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

    #Kysely siitä että haluaako pelaaja pelata uuden pelin

    valinta = input("\nHaluatko pelata uudelleen? (1 = Kyllä, 2 = Ei): ")

    while valinta not in ["1", "2"]:
        valinta = input("Virheellinen valinta. Anna 1 tai 2: ")

    return valinta == "1"

def pyydä_maa():

    # Pelaajalta kyselty uutta maata ja kirjoittamalla lopeta poistutaan pelistä

    maa = input("\nAnna uuden maan nimi tai ('lopeta' poistuaksesi): ")
    return maa

