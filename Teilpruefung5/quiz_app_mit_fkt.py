#----------------------------------------------------------------------------------------------
# Entwickle eine Python-Anwendung mit Tkinter für ein einfaches Quiz mit Fragen und mehreren Antwortmöglichkeiten über Radiobuttons. Die Anwendung soll Funktionen anbieten um Ergebnisse in einer Datei zu speichern und frühere Ergebnisse zu laden sowie Threads für Timer nutzen, um die GUI reaktionsfähig zu halten.
#
# a) Erstelle ein Python-Skript quiz_app.py, das die GUI aufbaut. Das Hauptfenster soll einen Titel, einen Bereich für die Frage, Radiobuttons für die Antwortmöglichkeiten, ein Timer-Label, einen "Nächste Frage"-Button und einen "Ergebnisse speichern"-Button enthalten.
#
# b) Implementiere Funktionen, um Fragen und Antwortmöglichkeiten anzuzeigen. Speichere jede Frage als Dictionary mit den folgenden Elementen: die Frage selbst, eine Liste der Antwortmöglichkeiten und die richtige Antwort.
#
# c) Füge einen Timer hinzu, der für jede Frage 30 Sekunden läuft. Verwende Threads, damit der Timer parallel zur GUI läuft und die Anwendung reaktionsfähig bleibt.
#
# d) Implementiere Eventhandler-Funktionen für die Buttons "Nächste Frage" und "Ergebnisse speichern". Der "Nächste Frage"-Button soll die nächste Frage laden und den Timer zurücksetzen. Der "Ergebnisse speichern"-Button soll die Antworten in einer Datei speichern und die Möglichkeit bieten, diese später zu laden.
#
# e) Verwende Dialogboxen, um den Pfad für das Speichern und Laden der Ergebnisse auszuwählen.
#
# Autor: Helena Rusch
# Letzte Änderung: 04.07.2025
#-----------------------------------------------------------------------------------------------

from tkinter import messagebox, filedialog 
import tkinter as tk 
import threading
import json
import time

def lade_fragen():
    """Lädt die Fragen aus einer JSON-Datei."""
    try:
        with open('fragen.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Fehler", "Die Datei 'fragen.json' wurde nicht gefunden.")
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Fehler", "Die Datei 'fragen.json' enthält kein gültiges JSON.")
        return []
    except IOError as e:
        messagebox.showerror("Fehler", f"Fehler beim Lesen der Datei: {e}")
        return []
def speichere_ergebnisse(antworten):
    """Speichert die Antworten in einer Datei."""
    dateipfad = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON-Dateien", "*.json")])
    if not dateipfad:
        return  # Abbrechen, wenn kein Pfad ausgewählt wurde
    try:
        with open(dateipfad, 'w', encoding='utf-8') as f:
            json.dump(antworten, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Erfolg", "Ergebnisse wurden gespeichert.")
    except IOError as e:
        messagebox.showerror("Fehler", f"Fehler beim Speichern der Datei: {e}")

def lade_ergebnisse():
    """Lädt die Antworten aus einer Datei."""
    dateipfad = filedialog.askopenfilename(filetypes=[("JSON-Dateien", "*.json")])
    if not dateipfad:
        return  # Abbrechen, wenn kein Pfad ausgewählt wurde
    try:
        with open(dateipfad, 'r', encoding='utf-8') as f:
            antworten = json.load(f)
        messagebox.showinfo("Erfolg", "Ergebnisse wurden geladen.")
        return antworten
    except FileNotFoundError:
        messagebox.showerror("Fehler", "Die Datei wurde nicht gefunden.")
    except json.JSONDecodeError:
        messagebox.showerror("Fehler", "Die Datei enthält kein gültiges JSON.")
    except IOError as e:
        messagebox.showerror("Fehler", f"Fehler beim Lesen der Datei: {e}")

def zeige_frage(frage, antworten):
    """Zeigt die aktuelle Frage und die Antwortmöglichkeiten an."""
    frage_label.config(text=frage)
    for i, antwort in enumerate(antworten):
        radiobuttons[i].config(text=antwort, value=antwort)
    for i in range(len(antworten), len(radiobuttons)):
        radiobuttons[i].pack_forget()  # Versteckt nicht verwendete Radiobuttons
    start_timer()

def start_timer():
    """Startet den Timer für die aktuelle Frage."""
    global timer_running, timer_thread, zeit
    zeit = 30  # Setzt die Zeit auf 30 Sekunden
    timer_running = True
    timer_label.config(text=f"Zeit: {zeit} Sekunden")
    if timer_thread is not None and timer_thread.is_alive():
        timer_thread.join()  # Wartet, bis der vorherige Thread beendet ist
    timer_thread = threading.Thread(target=timer_funktion)
    timer_thread.start()

def timer_funktion():
    """Die Funktion, die den Timer in einem separaten Thread ausführt."""
    global zeit, timer_running
    while zeit > 0 and timer_running:
        time.sleep(1)
        zeit -= 1
        timer_label.config(text=f"Zeit: {zeit} Sekunden")
    if zeit == 0:
        timer_running = False
        messagebox.showinfo("Zeit abgelaufen", "Die Zeit für diese Frage ist abgelaufen.")
        naechste_frage()  # Geht zur nächsten Frage, wenn die Zeit abgelaufen ist

def naechste_frage():
    global aktuelle_frage_index
    antwort = antwort_var.get()
    if antwort:
        fragen[aktuelle_frage_index]['user_antwort'] = antwort
    if aktuelle_frage_index < len(fragen) - 1:
        aktuelle_frage_index += 1
        antwort_var.set("")  # Zurücksetzen
        zeige_frage(fragen[aktuelle_frage_index]['frage'], fragen[aktuelle_frage_index]['antworten'])
    else:
        timer_running = False
        timer_label.config(text="Zeit: 0 Sekunden")
        messagebox.showinfo("Quiz beendet", "Das Quiz ist beendet.")

def speichern_antworten():
    """Speichert die Antworten des Benutzers."""
    antwort = antwort_var.get()
    if not antwort:
        messagebox.showwarning("Warnung", "Bitte wähle eine Antwort aus.")
        return
    antworten[aktuelle_frage_index]['user_antwort'] = antwort
    speichere_ergebnisse(antworten)
    messagebox.showinfo("Erfolg", "Antworten wurden gespeichert.")

def lade_antworten():
    """Lädt die Antworten des Benutzers aus einer Datei."""
    geladene_antworten = lade_ergebnisse()
    if geladene_antworten:
        for i, frage in enumerate(geladene_antworten):
            if i < len(fragen):
                fragen[i]['user_antwort'] = frage.get('user_antwort', '')
        zeige_frage(fragen[0]['frage'], fragen[0]['antworten'])
        messagebox.showinfo("Erfolg", "Antworten wurden geladen.")
    else:
        messagebox.showwarning("Warnung", "Keine Antworten geladen.")

# Initialisiert die GUI
root = tk.Tk() 
root.title("Quiz App")
fragen = lade_fragen()
if not fragen:
    messagebox.showerror("Fehler", "Keine Fragen zum Laden verfügbar.")
    root.destroy()
    exit()
aktuelle_frage_index = 0
antworten = fragen[aktuelle_frage_index]['antworten']
antwort_var = tk.StringVar()
frage_label = tk.Label(root, text="", wraplength=400)
frage_label.pack(pady=10)
radiobuttons = []
for i in range(4):
    rb = tk.Radiobutton(root, text="", variable=antwort_var, value="")
    rb.pack(anchor="w")
    radiobuttons.append(rb)
    rb.config(command=lambda: speichern_antworten())    # Speichert die Antwort, wenn eine Auswahl getroffen wird
zeige_frage(fragen[aktuelle_frage_index]['frage'], antworten)
timer_label = tk.Label(root, text="Zeit: 30 Sekunden")
timer_label.pack(pady=10)
timer_running = False
timer_thread = None  # Thread für den Timer
# Buttons für die Aktionen
naechste_button = tk.Button(root, text="Nächste Frage", command=naechste_frage)
naechste_button.pack(pady=5)
speichern_button = tk.Button(root, text="Ergebnisse speichern", command=speichere_ergebnisse)
speichern_button.pack(pady=5)
laden_button = tk.Button(root, text="Ergebnisse laden", command=lade_antworten)
laden_button.pack(pady=5)
# Startet die GUI
root.mainloop()
# Beendet den Timer-Thread, wenn die Anwendung geschlossen wird
if timer_thread is not None and timer_thread.is_alive():
    timer_running = False
    timer_thread.join()  # Wartet, bis der Timer-Thread beendet ist

