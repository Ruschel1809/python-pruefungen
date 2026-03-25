#-----------------------------------------------------------------------
# Dateiname: quiz_app.py
#-----------------------------------------------------------------------
# Beschreibung:
# Das Programm ist ein einfaches Quiz.
# Es implementiert eine GUI mit Labels, Text, Radiobuttons, Buttons, Dialogboxen und Messageboxen
# Ein nebenläufiger Timer ist für einen Countdown umgesetzt
# Das Ergebnis der Quiz kann als JSON auf dem Dateisystem gespeichert werden
# Autor: Helena Rusch
# Letzte Änderung: 04.07.2025
#-----------------------------------------------------------------------

import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import time
import json

# Quizfragen
ursprungsfragen = [
    {
        "frage": "Was ist die Hauptstadt von Deutschland?",
        "antworten": ["Paris", "Berlin", "Madrid", "Rom"],
        "richtig": "Berlin"
    },
    {
        "frage": "Wie ist das Ergebnis von 2 + 2?",
        "antworten": ["3", "5", "4", "7"],
        "richtig": "4"
    },
    {
        "frage": "Wie viele Kontinente gibt es?",
        "antworten": ["5", "6", "7", "8"],
        "richtig": "7"
    },
    {
        "frage": "Welche Farbe hat der Himmel?",
        "antworten": ["rot", "grün", "blau"],
        "richtig": "blau"
    }
]

# Globale Variablen

fragen = []  # wird beim Start neu befüllt
benutzer_antworten = []
aktuelle_frage = 0
timer_thread = None
timer_running = False
zeit = 30

# GUI-Funktionen

def quiz_neu_starten():
    """
    Räumt Oberfläche auf, wenn das Quiz neu gestartet wird
    """
    global fragen, benutzer_antworten, aktuelle_frage
    fragen = [dict(f) for f in ursprungsfragen]  # Kopie, nur für den Fall, dass ich irgendwann nochmal dran rum bastel ;)
    benutzer_antworten.clear()
    aktuelle_frage = 0
    naechste_btn.config(state="normal")
    quiz_wiederholen_btn.grid_remove()
    zeige_frage()
    anzeige_text.config(state="normal")
    anzeige_text.delete("1.0", tk.END)
    anzeige_text.config(state="disabled")

def zeige_frage():
    """
    zeigt aktuelle Frage und die Fortschrittsanzeige als Label,
    die dazugehörigen Antworten als Radiobuttons an und
    setzt einen Timer auf 30 Sekunden
    """
    global zeit, timer_running

    frage = fragen[aktuelle_frage]
    frage_label.config(text=f"{frage['frage']}")
    fortschritt_label.config(text=f"Frage {aktuelle_frage + 1} von {len(fragen)}")
    antwort_var.set(None)

    for i, text in enumerate(frage["antworten"]):
        radiobuttons[i].config(text=text, value=text)
        radiobuttons[i].grid(row=i+3, column=0, columnspan=2, padx=10, pady=10)

    for i in range(len(frage["antworten"]), len(radiobuttons)): # entfernen von überflüssigen Radiobuttons (z.B. aus der Frage davor)
        radiobuttons[i].grid_remove()

    zeit = 30
    timer_label.config(text=f"Zeit: {zeit} Sekunden")
    timer_running = False
    start_timer()

def start_timer():
    """
    Timer in extra Thread starten
    """

    global timer_thread, timer_running
    timer_running = True
    timer_thread = threading.Thread(target=timer_ablauf, daemon=True)
    timer_thread.start()

def timer_ablauf():
    """
    Wenn die Zeit abgelaufen ist und der Timer noch läuft
    (also noch nicht auf nächste Frage geklickt wurde)
    wird eine Sekunde pausiert und Zeit um 1 verringert,
    das Zeitlabel wird aktualisiert
    """
    global zeit, timer_running
    while zeit > 0 and timer_running:
        time.sleep(1)
        zeit -= 1
        timer_label.config(text=f"Zeit: {zeit} Sekunden")
    if zeit == 0:
        messagebox.showinfo("Zeit abgelaufen", "Die Zeit ist abgelaufen.")
        naechste_frage()

def naechste_frage():
    """
    Timer wird angehalten und die Antwort mit der zugehörigen Frage werden gespeichert
    Antwort, Frage und im Fehlerfall die richtige Antwort werden in einer Liste gespeichert
    Falls es noch fragen gibt, wird die Frage angezeigt, sondt das Ergebnis
    """
    global aktuelle_frage, timer_running
    timer_running = False

    antwort = antwort_var.get()
    frage = fragen[aktuelle_frage]
    benutzer_antworten.append({
        "frage": frage["frage"],
        "gewaehlt": antwort if antwort else None,
        "richtig": frage["richtig"]
    })

    aktuelle_frage += 1
    if aktuelle_frage < len(fragen):
        zeige_frage()
    else:
        zeige_ergebnis()

def zeige_ergebnis():
    """
    Wenn alle Frage beantwortet wurden, wird eine Messagebox mit dem Ergebnis angezeigt
    außerdem wird die Quiz-Gui aktualisiert und ein Button für eine neue Runde wird angezeigt
    """
    frage_label.config(text="Das Quiz ist beendet.")
    timer_label.grid_remove()
    fortschritt_label.grid_remove()

    richtige = sum(1 for a in benutzer_antworten if a["gewaehlt"] == a["richtig"])
    gesamt = len(benutzer_antworten)
    messagebox.showinfo("Ergebnis", f"Du hast {richtige} von {gesamt} Fragen richtig beantwortet.")

    for rb in radiobuttons:
        rb.grid_remove()

    naechste_btn.config(state="disabled")
    quiz_wiederholen_btn.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

def ergebnisse_speichern():
    """
    Dialogbox zum Speichern erscheint, um das Ergebnis als JSON zu speichern
    Im Fehlerfall erscheint eine Messagebox mit dem Fehler
    """
    dateipfad = filedialog.asksaveasfilename(defaultextension=".json",
                                             filetypes=[("JSON-Dateien", "*.json")])
    if dateipfad:
        try:
            with open(dateipfad, "w", encoding="utf-8") as f:
                json.dump(benutzer_antworten, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Erfolg", "Ergebnisse gespeichert.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Speichern fehlgeschlagen: {e}")

def ergebnisse_laden():
    """
    Gespeicherte Ergebnisse könne geladen und in einem Text-Widget ausgegeben
    Fehler erscheinen in einer Messagebox
    """
    global benutzer_antworten
    dateipfad = filedialog.askopenfilename(filetypes=[("JSON-Dateien", "*.json")])
    if dateipfad:
        try:
            with open(dateipfad, "r", encoding="utf-8") as f:
                benutzer_antworten = json.load(f)
            messagebox.showinfo("Erfolg", "Ergebnisse geladen.")
            zeige_geladene_ergebnisse()
        except Exception as e:
            messagebox.showerror("Fehler", f"Laden fehlgeschlagen: {e}")

def zeige_geladene_ergebnisse():
    """
    Das geladene Ergebnis aus einem früheren Spiel wird in einem vorher geleerten Text-Widget angezeigt
    Das Text-Widget ist nicht editierbar
    Falls keine Ergebnisse vorhanden, wird eine Info angezeigt
    """
    anzeige_text.config(state="normal")
    anzeige_text.delete("1.0", tk.END)

    if not benutzer_antworten:
        anzeige_text.insert(tk.END, "Keine geladenen Antworten vorhanden.")
    else:
        for i, eintrag in enumerate(benutzer_antworten, start=1):
            frage = eintrag.get("frage", "")
            gewaehlt = eintrag.get("gewaehlt", "Keine Antwort")
            richtig = eintrag.get("richtig", "")
            text = f"Frage {i}:\n{frage}\nAntwort: {gewaehlt}\nRichtig: {richtig}\n\n"
            anzeige_text.insert(tk.END, text)

    anzeige_text.config(state="disabled")

def beenden():
    """
    kontrolliertes beenden des Fensters und aller Threads
    """
    global timer_running
    timer_running = False
    root.destroy()

# GUI Aufbau

root = tk.Tk()
root.title("Einfaches Quiz")

frage_label = tk.Label(root, text="", wraplength=400, font=("Arial", 12, "bold"), fg="blue")
frage_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

fortschritt_label = tk.Label(root, text="", font=("Arial", 10))
fortschritt_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

timer_label = tk.Label(root, text="Zeit: 30 Sekunden", font=("Arial", 10, "bold"))
timer_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

antwort_var = tk.StringVar()
radiobuttons = [tk.Radiobutton(root, text="", variable=antwort_var, value="", font=("Arial", 10)) for _ in range(4)]

naechste_btn = tk.Button(root, text="Nächste Frage", command=naechste_frage)
naechste_btn.grid(row=8, column=0, padx=10, pady=10)

speichern_btn = tk.Button(root, text="Ergebnisse speichern", command=ergebnisse_speichern)
speichern_btn.grid(row=9, column=0, padx=10, pady=10)

laden_btn = tk.Button(root, text="Ergebnisse laden", command=ergebnisse_laden)
laden_btn.grid(row=9, column=1, padx=10, pady=10)

quiz_wiederholen_btn = tk.Button(root, text="Quiz wiederholen", command=quiz_neu_starten)

anzeige_text = tk.Text(root, height=10, width=60)
anzeige_text.grid(row=11, column=0, columnspan=2, padx=10, pady=10)
anzeige_text.config(state="disabled")  # schreibgeschützt

root.protocol("WM_DELETE_WINDOW", beenden) # kontrolliertes Beenden. Sicherstellen, dass Threads nicht mehr weiterlaufen

quiz_neu_starten()
root.mainloop()