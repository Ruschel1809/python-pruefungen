#-----------------------------------------------------------------------
# Dateiname: feedback_analyzer.py
#-----------------------------------------------------------------------
# Beschreibung:
# Das Programm analysiert eine Textdatei mit Kundenkommentaren
# in verschiedenen Sprachen.
# zuerst wird die Arbeitsumgebung initialisiert, dazu wird in einem
# gewünschten Verzeichnis oder im aktuellen Verzeichnis eine Textdatei angelegt
# Funktionen:
# - Textdatei einselen
# - Vorkommen von Datumsangaben filtern und zählen.
# - Kommentare nach dem Wort exzellent filtern
# - Dict mit Datum und Liste mit "exzellent"-Kommentaren in zwei 
#   JSON-Dateien speichern
#   datums_vorkommen.json und exzellent_feedbacks.json
# - Fehlerbehandlung für alle notwendigen Stellen
# - mit Unicode spezielle Zeichen in die Ausgabe einfügen,
#   z.B.: Erfolg einer Operation kennzeichnen
# - Textdatei mit obigen Anforderungen erstellen, um den Code zu testen
# Autor: Helena Rusch
# Letzte Änderung: 27.06.2025
#-----------------------------------------------------------------------
import os
import re
import json
import time

dateiname = "feedback.txt"
def is_dateipfad_syntax_gueltig(pfad:str):
  reg = r"^(([a-zA-Z]:)?[\\/])?([\w\- äöüÄÖÜß]+[\\/])*[\w\- äöüÄÖÜß]+$"
  if re.search(reg,pfad):
    return True
  else:
    return False
#-----------------------------------------------------------------------------------------------------------------------
# Initialisierung
print("Vor dem Start der Analyzer Funktionalität muss die Arbeitsumgebung initialisiert werden.")
pfad = input("Möchtest du in einem bestimmten Verzeichnis arbeiten?\nFalls ja, dann gib es bitte vollständig an (anderenfalls arbeitest du mit \"ENTER\" im aktuellen Verzeichnis):\n").strip()

while not is_dateipfad_syntax_gueltig(pfad):
  if pfad == "":
    pfad = "."
    break
  pfad = input("Die Eingabe entspricht nicht den Vorgaben. Bitte gib einen gültigen Dateipfad oder drücke ENTER für das aktuelle Verzeichnis.\n\033[31mBEACHTE: Dateien im Pfad sind nicht zugelassen\nund lieber Unix/macOS Nutzer: statt \"~\" bitte das Home-Verzeichnis ausschreiben\033[0m\n").strip()
if not os.path.exists(pfad):
  os.makedirs(pfad)
pfad_mit_datei = os.path.join(pfad, dateiname)


# eine Spielerei, die den Progress simulieren soll, ohne auch nur im Geringsten etwas mit dem Prozess zutun zu haben ;)
dots = ["", ".", "..", "..."]
for i in range(10):
  print(f"\rIch lege eine \"feedback.txt\" in dem gewählten Verzeichnis an{dots[i%4]}", end="", flush=True )
  time.sleep(0.5)
print("\n")

initial_text = """\"Die Lieferung war schnell und problemlos. Exzellent organisiert!\" – 09.01.2024\n
\"Доставка была быстрой и без проблем. Упаковка — просто exzellent!\" – 09.01.2024\n
\"Excellent communication and fast delivery!\" – 27.11.2024\n
\"The product quality was average, not what I expected.\" – 05.08.2023\n
\"Товар не соответствовал описанию, пришлось вернуть.\" – 21.06.2023\n
\"Kundendienst hat leider lange gebraucht.\" – 21.06.2023\n
\"Service was exzellent and very professional.\" – 21.06.2023\n
\"Sehr zufrieden mit dem gesamten Ablauf. Alles top!\" – 19.10.2022\n
\"Всё пришло очень быстро. Качество отличное!\" – 12.12.2022\n
"""
try:
  with open(pfad_mit_datei,"w", encoding="utf-8") as file:
    file.write(initial_text)
except FileNotFoundError:
  pass
except IOError as ioe:
  print("Fehler beim Schreiben der Datei: ", ioe)

print(f"Initialisierung erfolgreich abgeschlossen. {chr(int("1F600",16))}")
#Initialisierung Ende
#-----------------------------------------------------------------------------------------------------------------------

def lese_feedback_datei() -> str | None:
  '''
  die Funktion liest die feedback.txt Datei ein
  da sie unterschiedliche Sprachen enthält wird sie utf-8 encoded

  Returns: den ausgelesenen Text oder None im Fehlerfall
  '''
  try:
    with open(pfad_mit_datei,"r", encoding="utf-8") as f:
      return f.read()
  except FileNotFoundError:
    print("Datei existiert nicht.")
    return None
  except IOError as e:
    print("Fehler beim Lesen der Datei: ", e)
    return None

def extract_date(t:str) -> list[str]:
  '''
  Die Funktion filtert nach dem Datum in den
  Kommentaren und speichert sie in einer Liste

  Args: t: String der durchsucht werden soll
  Returns: eine Liste von Strings (Datumsangaben)
  '''

  datumsliste = []
  regex=r"\d{2}\.\d{2}\.\d{4}" #TT.MM.JJJJ
  for zeilen in t.splitlines(): # jede Zeile einzeln betrachten
    datumsliste.extend(re.findall(regex, zeilen))
  return datumsliste

def anzahl_eintraege_pro_datum(l:list[str]) -> dict[str, int]:
  '''
  Legt ein Dictionary aus Datum und Anzahl seines Vorkommens im Text an

  Args: l: Liste der Datums
  Returns: Dictionary aus Datum und Anzahl
  '''
  return {elem: l.count(elem) for elem in set(l)} # alle verschiedenen Listenelemente ins dict und Vorkommen des schlüssels in der liste zählen

def finde_exzellente(t:str) -> list[str]:
  '''
  die Funktion filtert nach dem Wort exzellent
  und fügt die entsprechenden Kommentare in eine Liste ein

  Args: t: String der durchsucht werden soll
  Returns: Liste von Strings (exzellente Kommentare)
  '''
  exzellente_kommentare = []
  for line in t.splitlines():
    if "exzellent" in line.lower():
        exzellente_kommentare.append(line)
  return exzellente_kommentare

def speichere_json(d, datei: str):
  '''
  eine passende Datenstruktur wird in einem JSON File gespeichert

  Args: d: Kollektion zum Speichern
        datei: name der Datei
  '''
  try:
    with open(datei, 'w', encoding="utf-8") as f:
      json.dump(d, f)
  except FileNotFoundError:
    pass
  except (TypeError, OverflowError) as e:
    print("Keine passende Datenstruktur. Bitte überprüfe deine Textdatei. ", e)
  except IOError as e:
    print("Fehler beim Speichern der Datei: ", e)

text = lese_feedback_datei()

# nur damit es so wirkt, als würde kräftig gearbeitet :) und zum Einfügen von Emojis
print(f"Analyse läuft: Liste mit Datumsangaben wird erstellt. {chr(int("231B",16))}")
time.sleep(1)
print(f"Analyse läuft: Filtere nach exzellenten Kommentaren. {chr(int("231B",16))}")
time.sleep(1)

speichere_json(anzahl_eintraege_pro_datum(extract_date(text)), os.path.join(pfad, "datums_vorkommen.json"))
print(f"Datumsangaben wurden in datums_vorkommen.json erfolgreich gespeichert. {chr(int("1F44D",16))}")
speichere_json(finde_exzellente(text), os.path.join(pfad, "exzellente_feedbacks.json"))
print(f"exzellenten Kommentare wurden in exzellente_feedbacks.json erfolgreich gespeichert. {chr(int("1F44D",16))}")
