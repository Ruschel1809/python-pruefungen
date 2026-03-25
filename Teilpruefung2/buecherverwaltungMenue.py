#---------------------------------------------------------------
# Dateiname: buecherverwaltungMenue.py
#---------------------------------------------------------------
# Beschreibung:
# Das Programm bietet ein interaktives Menü, dass dem Nutzer 
# die Verwendung der Funktionen aus dem Modul buecherverwaltung anbietet.
# Autor: Helena Rusch
# Letzte Änderung: 13.06.2025
#---------------------------------------------------------------

from buecherverwaltung import buch_suchen, fuege_buch_hinzu, buecher_nach_jahr, zeige_datenbank
while True:
    # Auswahlmenü anzeigen
    print("\nBücherverwaltungsmenü:")
    print("1. Buch suchen")
    print("2. Buch hinzufügen")
    print("3. Bücher nach Jahr filtern")
    print("4. Alle Bücher anzeigen")
    print("5. Beenden")

    wahl = input("Bitte wählen Sie eine Option (1-5): ")
    # Eingabe verarbeiten
    if wahl == "1":
        titel = input("Geben Sie den Titel des Buches ein: ")
        autor = input("Geben Sie den Autor des Buches ein (optional, Enter zum Überspringen): ")
        ergebnis = buch_suchen(titel, autor if autor else None) # Suche nach Buch mit importierter Funktion
        # Ergebnis anzeigen
        if ergebnis:
            print(f"Buch gefunden: {ergebnis[0]}")
        else:
            print("Buch nicht gefunden.")

    elif wahl == "2":
        titel = input("Geben Sie den Titel des neuen Buches ein: ")
        autor = input("Geben Sie den Autor des neuen Buches ein: ")
        # prüfen ob eine Zahl eingegeben wurde
        try: 
            jahr = int(input("Geben Sie das Jahr der Veröffentlichung ein: "))
        # falls andere Eingabe als Zahl erfolgt, wird eine Fehlermeldung ausgegeben und der Nutzer aufgefordert eine neue Eingabe zu tätigen
        except ValueError:
            print("Ungültige Eingabe, bitte geben Sie eine gültige Jahreszahl ein.")
            continue
        fuege_buch_hinzu(titel, autor, jahr) # Buch hinzufügen mit importierter Funktion
        print(f"Buch '{titel}' wurde hinzugefügt.")

    elif wahl == "3":
        # prüfen ob eine Zahl eingegeben wurde
        try:
            jahr = int(input("Geben Sie das Jahr ein, nach dem gefiltert werden soll: "))
        # falls andere Eingabe als Zahl erfolgt, wird eine Fehlermeldung ausgegeben und der Nutzer aufgefordert eine neue Eingabe zu tätigen
        except ValueError:
            print("Ungültige Eingabe, bitte geben Sie eine gültige Jahreszahl ein.")
            continue
        gefilterte_buecher = buecher_nach_jahr(jahr) # Bücher nach Jahr filtern mit importierter Funktion
        if gefilterte_buecher: # Wenn Bücher gefunden wurden
            # Ausgabe der gefilterten Bücher
            print(f"Bücher aus dem Jahr {jahr}:")
            for buch in gefilterte_buecher:
                print(f"Titel: {buch['Titel']}, Autor: {buch['Autor']}, Jahr: {buch['Jahr']}")
        else:
            print(f"Keine Bücher aus dem Jahr {jahr} gefunden.")

    elif wahl == "4":
        zeige_datenbank() # Alle Bücher anzeigen mit importierter Funktion

    elif wahl == "5":
        print("Programm beendet.") # Beenden des Programms
        break

    else:
        print("Ungültige Auswahl, bitte versuchen Sie es erneut.") # Ungültige Eingabe, Nutzer wird aufgefordert eine neue Eingabe zu tätigen