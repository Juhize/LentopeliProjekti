#Tämä funktio laskee pelaajan lennon tuoton - kulut ja laskee tehtyjen lentojen määrän

def money(lentokentta, icao):
#Mysteeri syystä ilman pyöristystä luvusta saadaan enemmän desimaaleja, kun pitäisi.
    creation.execute(f"SELECT flights FROM game WHERE id = {player_id}")
    lennot = creation.fetchone()
    flight_counter = lennot[0]
    CO2Tax = round(1 - (flight_counter // 3 * 0.2), 1)
    CO2Tax = max(0.2, CO2Tax)
    #Seuraavassa haetaan aktiivisen pelaajan rahamäärä
    creation.execute(f"SELECT balance FROM game WHERE id = {player_id}")
    rahat = creation.fetchone()
    if lentokentta == 1:
        tuotto = rahat[0] + random.randint(200,1000) * CO2Tax - flight_cost(icao)
    elif lentokentta == 2:
        tuotto = rahat[0] + random.randint(300,1500) * CO2Tax - flight_cost(icao)
    elif lentokentta == 3:
        tuotto = rahat[0] + random.randint(400,2000) * CO2Tax - flight_cost(icao)
    flight_counter += 1
    #Seuraavassa päivitetään uusi rahamäärä ja lentojen määrä aktiiviselle pelaajalle
    creation.execute(f'UPDATE game SET balance = {int(tuotto)}, flights = {int(flight_counter)} WHERE id={player_id}')