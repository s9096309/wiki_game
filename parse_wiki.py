import random
import requests

# Liste der Bundesländer und ihrer geografischen Zentren (Koordinaten)
bundesland_koordinaten = {
    "Baden-Württemberg": (48.6616, 9.3500),
    "Bayern": (48.7904, 11.4979),
    "Berlin": (52.5200, 13.4050),
    "Brandenburg": (52.4135, 13.0595),
    "Bremen": (53.0793, 8.8017),
    "Hamburg": (53.5511, 9.9937),
    "Hessen": (50.2270, 8.5820),
    "Niedersachsen": (52.5563, 9.9625),
    "Mecklenburg-Vorpommern": (53.6292, 12.2855),
    "Nordrhein-Westfalen": (51.1657, 6.9781),
    "Rheinland-Pfalz": (50.2377, 7.1261),
    "Saarland": (49.3966, 7.0230),
    "Sachsen": (51.1047, 13.2010),
    "Sachsen-Anhalt": (51.3804, 11.8123),
    "Schleswig-Holstein": (54.3233, 10.1201),
    "Thüringen": (50.9820, 11.0291)
}

# Festgelegtes Bundesland
bundesland = "Bayern"
koord = bundesland_koordinaten[bundesland]

print(f"Bundesland: {bundesland}")
print(f"Koordinaten: {koord}")

# Wikimedia API
def get_landmarks_from_wikimedia(coords, radius=5000):
    """
    Holt Landmarken für die gegebenen Koordinaten aus der Wikimedia API.
    """
    endpoint = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'list': 'geosearch',
        'gscoord': f"{coords[0]}|{coords[1]}",
        'gsradius': radius,
        'gslimit': 50,
        'format': 'json'
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        # Prüfen, ob Ergebnisse vorhanden sind
        landmarks = data.get('query', {}).get('geosearch', [])
        if not landmarks:
            print("Keine Landmarken gefunden.")
            return None

        # Landmark-Titel extrahieren
        landmark_titles = [landmark['title'] for landmark in landmarks]

        # Eine zufällige Landmarke auswählen und zurückgeben
        return random.choice(landmark_titles)

    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return None

# Abrufen einer zufälligen Landmarke
landmark = get_landmarks_from_wikimedia(koord)

if landmark:
    print(f"Zufällige Landmarke in {bundesland}: {landmark}")
else:
    print(f"Keine Landmarke gefunden.")
