#(tämä osuus on Willen koodia 
# Tämä funktio arpoo saadun voidon
# if tulos:
lentokentta = int(input("Mille lentokentälle haluat mennä? (1-3): "))
#     #seuraavan rivin lopussa numero "1" on game_id ja sen voi muuttaa käyttäjän muuttuvaksi game_id
#     kentta = valitse(tulos, lentokentta, 1)
#)

#Funktioon tarvitaan rakenne, joka hakee tietokannassa pelaajan rahat, sekä lennettyjen lentojen määrän
#Funktioon tarvitaan rakenne, joka mittaa etäisyyttä lentokenttien välillä, minkä mukaan lisätään menoihin lennon pituudesta riippuva elementti 
# -Varmaan pienennän kiinteitä lentokenttämaksuja tämän jälkeen
#Funktion loppuun tarvitaan rakenne missä uusi rahamäärä, sekä lentojen määrä tallennetaan tietokantaan
#Pääohjelma ilmoittaa pelaajalle(-vai funktio?) uuden rahamäärän ja CO2Tax kertoimen

#CO2Tax lisätty testin vuoksi - CO2Tax voi sitoa suoraan koodissa lennettyihin lentoihin if lauseessa
CO2Tax = 1
import random
def money():
    if lentokentta == 1:
        tuotto = random.randint(200,1000) * CO2Tax - 400
    elif lentokentta == 2:
        tuotto = random.randint(300,1500) * CO2Tax - 600
    elif lentokentta == 3:
        tuotto = random.randint(400,2000) * CO2Tax - 800
    return int(tuotto)

kierroksen_tuotto = money()

print(f"Kierroksen tuotto: {kierroksen_tuotto}")