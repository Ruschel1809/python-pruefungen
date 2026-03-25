#---------------------------------------------------------------
# Dateiname: buecherverwaltung.py
#---------------------------------------------------------------
# Beschreibung:
# Das Programm verwaltet eine Sammlung von Büchern. Mit Funktionen zur Buchsuche,
# Hinzufügung von Büchern, Jahresfilter, sowie zur Anzeige aller Bücher.
# Autor: Helena Rusch
# Letzte Änderung: 13.06.2025
#---------------------------------------------------------------

buecherei_datenbank = [
    {"Titel": "Python mit Biss", "Autor": "Michael Hartl", "Jahr": 2025},
    {"Titel": "Python für Kinder", "Autor": "Florian André Dalwigk", "Jahr": 2025},
    {"Titel": "Python Programming", "Autor": "Guido van Rossum", "Jahr": 1990},
    {"Titel": "Python Pocket Reference", "Autor": "Mark Lutz", "Jahr": 2002},
    {"Titel": "Einführung in Python", "Autor": "Mark Lutz", "Jahr": 2000}
]

def buch_suchen(titel: str, autor=None) -> list:
    """
    Sucht ein Buch in der Datenbank.

    :param titel: Der Titel des gesuchten Buches.
    :param autor: Der Autor des gesuchten Buches (optional).
    :return: Eine Liste mit dem gefundenen Buch oder eine leere Liste, wenn das Buch nicht gefunden wurde.
    """
    for buch in buecherei_datenbank:
        if buch["Titel"] == titel and (autor is None or buch["Autor"] == autor):
            return [buch]
    return []

def fuege_buch_hinzu(titel: str, autor: str, jahr: int) -> None:
    """
    Fügt ein neues Buch zur Datenbank hinzu.

    :param titel: Der Titel des neuen Buches.
    :param autor: Der Autor des neuen Buches.
    :param jahr: Das Jahr der Veröffentlichung des neuen Buches.
    """
    buecherei_datenbank.append({"Titel": titel, "Autor": autor, "Jahr": jahr})

def buecher_nach_jahr(jahr: int) -> list:
    """
    Filtert die Bücher nach dem Veröffentlichungsjahr.

    :param jahr: Das Jahr, nach dem gefiltert werden soll.
    :return: Eine Liste der Bücher, die im angegebenen Jahr veröffentlicht wurden.
    """
    return list(filter(lambda buch: buch["Jahr"] == jahr, buecherei_datenbank))

def zeige_datenbank() -> None:
    """
    Zeigt alle Bücher in der Datenbank an.
    """
    if not buecherei_datenbank:
        print("Die Datenbank ist leer.")
        return
    for buch in buecherei_datenbank:
        print(f'Titel: {buch["Titel"]}, Autor: {buch["Autor"]}, Jahr: {buch["Jahr"]}')