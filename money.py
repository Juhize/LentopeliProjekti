def money(lentokentta, icao):
#Tämä funktio laskee pelaajan lennon tuoton - kulut ja laskee tehtyjen lentojen määrän
#Funktio myös ilmoittaa pelaajalle edellisen lennon tuoton, kulut, päivitetyn rahatilanteen, tehtyjen lentojen määrän, sekä nykyisen päästökertoimen.
#Mysteeri syystä ilman pyöristystä luvusta saadaan enemmän desimaaleja, kun pitäisi.
    creation.execute(f"SELECT flights FROM game WHERE id = {player_id}")
    lennot = creation.fetchone()
    flight_counter = lennot[0]
    CO2Tax = round(1 - (flight_counter // 3 * 0.2), 1)
    CO2Tax = max(0.2, CO2Tax)
    #Seuraavassa haetaan aktiivisen pelaajan rahamäärä
    creation.execute(f"SELECT balance FROM game WHERE id = {player_id}")
    rahat = creation.fetchone()
    pieni = random.randint(200,1000) * CO2Tax
    keskikoko = random.randint(300,1500) * CO2Tax
    suuri = random.randint(400,2000) * CO2Tax
    kulut = flight_cost(icao)
    if lentokentta == 1:
        tuotto = pieni
    elif lentokentta == 2:
        tuotto = keskikoko
    elif lentokentta == 3:
        tuotto = suuri
    flight_counter += 1
    balance = rahat[0] + tuotto - kulut
    print(f"\nRahat ennen lentoa: {int(rahat[0])}€ \nTuotto: {int(tuotto)}€ \nKulut yhteensä:-{int(kulut)}€ \nSinulla on nyt {int(balance)}€ rahaa.")
    print(f"Olet suorittanut {int(flight_counter)} lentoa. \nPäästökertoimesi on {round(1 - (flight_counter // 3 * 0.2), 1)}")
    #Seuraavassa päivitetään uusi rahamäärä ja lentojen määrä aktiiviselle pelaajalle
    creation.execute(f'UPDATE game SET balance = {int(balance)}, flights = {int(flight_counter)} WHERE id={player_id}')
    # if balance <= 0:
    #     lopetus_funktio()