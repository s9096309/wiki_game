import requests
import random

# Liste der Bundesländer und deren Wikidata-IDs
bundesland_liste = [
    "Baden-Württemberg", "Bayern", "Berlin", "Brandenburg",
    "Bremen", "Hamburg", "Hessen", "Niedersachsen",
    "Mecklenburg-Vorpommern", "Nordrhein-Westfalen", "Rheinland-Pfalz",
    "Saarland", "Sachsen", "Sachsen-Anhalt", "Schleswig-Holstein", "Thüringen"
]

bundesland_wikidata = {
    "Baden-Württemberg": "Q1078",
    "Bayern": "Q1039",
    "Berlin": "Q183",
    "Brandenburg": "Q1253",
    "Bremen": "Q2456",
    "Hamburg": "Q1304",
    "Hessen": "Q1361",
    "Niedersachsen": "Q1283",
    "Mecklenburg-Vorpommern": "Q1295",
    "Nordrhein-Westfalen": "Q1306",
    "Rheinland-Pfalz": "Q1337",
    "Saarland": "Q1297",
    "Sachsen": "Q1315",
    "Sachsen-Anhalt": "Q1290",
    "Schleswig-Holstein": "Q1308",
    "Thüringen": "Q1371"
}

# Benutzer nach dem Bundesland fragen
while True:
    try:
        ask_bundesland = int(input("""
Wähle ein Bundesland (1-16):
1.  Baden-Württemberg
2.  Bayern
3.  Berlin
4.  Brandenburg
5.  Bremen
6.  Hamburg
7.  Hessen
8.  Mecklenburg-Vorpommern
9.  Niedersachsen
10. Nordrhein-Westfalen
11. Rheinland-Pfalz
12. Saarland
13. Sachsen
14. Sachsen-Anhalt
15. Schleswig-Holstein
16. Thüringen
"""))

        # Eingabevalidierung
        if ask_bundesland < 1 or ask_bundesland > 16:
            print("Ungültige Eingabe. Bitte wählen Sie eine Zahl zwischen 1 und 16.")
            continue
        break

    except ValueError:
        print("Bitte geben Sie eine gültige Zahl ein (1-16):")

# Bundesland aus der Liste anhand der Benutzereingabe auswählen
bundesland = bundesland_liste[ask_bundesland - 1]  # -1, weil die Liste bei 0 startet
wikidata_id = bundesland_wikidata[bundesland]

def get_landmarks_from_wikidata(bundesland):
    """
    Holt Landmarken mit Bild-URLs für ein gegebenes Bundesland aus Wikidata.
    """
    # SPARQL-Abfrage für Wikidata: Suche nach Landmarken aus einem bestimmten Bundesland mit einem Bild
    sparql_query = f"""
    SELECT ?landmark ?landmarkLabel ?image WHERE {{
      ?landmark wdt:P31 wd:Q3918;  # Landmarken (Denkmal, Sehenswürdigkeit)
              wdt:P131 wd:{wikidata_id};  # Dynamischer Wikidata-Code des Bundeslandes
              wdt:P18 ?image.   # Muss ein Bild haben
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],de". }}
    }}
    LIMIT 10
    """

    endpoint = "https://query.wikidata.org/sparql"
    headers = {
        "User-Agent": "Wikidata API Example"
    }
    params = {
        "query": sparql_query,
        "format": "json"
    }

    # Senden der Anfrage an Wikidata API
    response = requests.get(endpoint, params=params, headers=headers)
    data = response.json()

    landmarks = []

    for item in data['results']['bindings']:
        landmark = item['landmarkLabel']['value']
        image_url = item['image']['value']
        landmarks.append({'name': landmark, 'image_url': image_url})

    return landmarks

# Landmarken für das gewählte Bundesland abrufen
landmarks = get_landmarks_from_wikidata(bundesland)

if landmarks:
    selected_landmark = random.choice(landmarks)
    print(f"Landmarke: {selected_landmark['name']}")
    print(f"Bild-URL: {selected_landmark['image_url']}")
else:
    print("Keine Landmarken mit Bildern gefunden.")
