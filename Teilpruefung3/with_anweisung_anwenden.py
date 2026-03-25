#---------------------------------------------------------------
# Dateiname: with_anweisung_anwenden.py
#---------------------------------------------------------------
# Beschreibung:
# Das Programm liest Namen aus einer Textdatei und gibt sie zeilenweise aus.
# Weiterhin bietet das Programm die Möglichkeit die Daten aus der Textdatei
# ins Json-Format umzuwandeln und in einer JSON-Datei zu speichern.
# Außerdem bietet das Programm die Option Namen einzupflegen. Und falls der
# Nutzer nur die Funktionen testen möchte, dann bietet das Programm an, eine
# Namensliste zu generieren. In einer CLI hat der Nutzer die Möglichkeit
# zwischen den Funktionen zu wählen.
# Autor: Helena Rusch
# Letzte Änderung: 20.06.2025
#---------------------------------------------------------------
import json as j

FILE_TXT="namen.txt"
FILE_JSON="namen.json"

def speichere_namen_json(liste: list[str]) -> None:
    """
    Speichert Namen in einer JSON-Datei als Liste von Strings.
    Vorhandene Namen werden ergänzt.
    """
    existing = []
    try:
        with open(FILE_JSON,"r") as f:
            existing = j.load(f)
    except FileNotFoundError:
        pass # Datei gibt es noch nicht, nicht schlimm
    except j.JSONDecodeError as e:
        existing = []
        print("Datei existiert, enthält aber kein gültiges JSON: ", e)
    except IOError as e:
        print("Fehler beim Lesen: ", e)
    for name in liste:
        existing.append(name)
    try:
        with open(FILE_JSON,"w") as f:
            j.dump(existing,f)
    except IOError as e:
        print("Fehler beim Schreiben der Datei: ", e)

def lade_namen_json() -> list[str] | None:
    """
    Lädt Namen aus der JSON-Datei.
    Gibt eine Liste von Strings zurück oder None
    """
    try:
        with open(FILE_JSON,"r") as f:
           return j.load(f)
    except FileNotFoundError:
        print("Noch keine Personen gespeichert.")
    except j.JSONDecodeError as e:
        print("Datei enthält ungültiges JSON: ",e)
    except IOError as e:
        print("Fehler beim Laden: ", e)
    except Exception as e:
        print("Es ist ein unbekannter Fehler aufgetreten: ", e)
    return None

def speichere_namen_txt(l:list[str]) -> None:
    """
    Speichert Naemn in einer Textdatei pro Zeile
    Vorhandene namen werden ergänzt
    """
    existing = []
    try:
        with open(FILE_TXT,"r") as f:
            for line in f:
                existing.append(line.strip())
    except FileNotFoundError:
        pass
    except IOError as e:
        print("Fehler beim Laden: ", e)
    except Exception as e:
        print("Es ist ein unbekannter Fehler aufgetreten: ", e)
    for elem in l:
        existing.append(elem.strip())
    try:
        with open(FILE_TXT,"w") as f:
            for elem in existing:
                f.write(elem + "\n")
    except IOError as e:
        print("Fehler beim speichern: ", e)
    except Exception as e:
        print("Es ist ein unbekannter Fehler aufgetreten: ", e)

def lade_namen_txt() -> list[str]:
    """
    Lädt Namen aus einer Textdatei.
    Gibt eine Liste zurück.
    """
    liste_namen=[]
    try:
        with open(FILE_TXT,"r") as f:
           liste_namen = [line.strip() for line in f]
    except FileNotFoundError:
        print("Noch keine Personen gespeichert.")
    except IOError as e:
        print("Fehler beim Laden: ", e)
    except Exception as e:
        print("Es ist ein unbekannter Fehler aufgetreten: ", e)
    finally:
        return liste_namen


def main () -> None:
    print("Personen")
    eingabe = ""

    while eingabe != "e":
        eingabe = input("[stxt] Neue Personen in der namen.txt speichern.\n[ltxt] Vorhandene Personen in namen.txt anzeigen.\n[sjson] Neue Personen in der namen.json speichern.\n[ljson] Vorhandene Personen in namen.json anzeigen.\n[t] Personenliste zum Test generieren un in einer namen.txt Datei speichern.\n[txt2json] namen.txt in namen.json Datei speichern.\n[e] Programm beenden.\n").strip()
        if eingabe == "e":
            print("Programm beendet.")
        elif eingabe == "t":
            test_namen = ["Anna Aa", "Bobo Be", "Cora Ce", "Dora De", "Emil Ee", "Fibi Ef", "Gerd Ge"]
            speichere_namen_txt(test_namen)
            print("Es wurden 7 Namen gespeichert.")
        elif eingabe == "stxt":
            liste = []
            while True:
                eingabe_zum_speichern = input("Gib einen Namen ein (oder se zum Beenden):\n")
                if eingabe_zum_speichern.lower().strip() == "se":
                    break
                liste.append(eingabe_zum_speichern)
            speichere_namen_txt(liste)
            print(f"Es wurden {len(liste)} Namen gespeichert")
        elif eingabe == "ltxt":
            namen = lade_namen_txt()
            if namen:
                for l in namen:
                    print(f"- {l}")
            else:
                print("Keine Personen gespeichert.")
        elif eingabe == "txt2json":
            speichere_namen_json(lade_namen_txt())
        elif eingabe == "sjson":
            liste= []
            while True:
                eingabe_zum_speichern = input("Gib einen Namen ein (oder se zum Beenden):\n")
                if eingabe_zum_speichern.lower().strip() == "se":
                    break
                liste.append(eingabe_zum_speichern)
            speichere_namen_json(liste)
            print(f"Es wurden {len(liste)} Namen gespeichert")
        elif eingabe == "ljson":
            namen = lade_namen_json()
            if namen:
                print("Deine Namensliste:")
                for i, eintrag in enumerate(namen, 1):
                    print(f"{i}. {eintrag}")
            else:
                print("Keine Personen gespeichert.")

if __name__ == "__main__":
    main()
