#----------------------------------------------------------------------------------------------
# Quiz App
#
# Autor: Helena Rusch
# Letzte Änderung: 04.07.2025
#-----------------------------------------------------------------------------------------------

import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import time 
import json
import os

class DieErsteQuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz App")
        
        self.fragen = [
            {"frage": "Was ist die Hauptstadt von Deutschland?", 
             "option": ["Berlin", "München", "Hamburg", "Köln"], 
             "answer": "Berlin"},
            {"frage": "Was ist 2 + 2?", 
             "option": ["3", "4", "5", "6"], 
             "answer": "4"},
            {"frage": "Welche Farbe hat der Himmel?", 
             "option": ["Blau", "Grün", "Rot", "Gelb"], 
             "answer": "Blau"}
        ]
        
        self.aktuelle_frage_index = 0
        self.punkte = 0
        self.timer = 30
        self.timer_thread = None
        
        self.frage_label = tk.Label(master, text="", wraplength=300)
        self.frage_label.pack(pady=10)
        
        self.var = tk.StringVar()
        self.optionen_frame = tk.Frame(master)
        self.optionen_frame.pack(pady=10)
        
        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(self.optionen_frame, text="", variable=self.var, value="")
            rb.pack(anchor='w')
            self.radio_buttons.append(rb)
        
        self.timer_label = tk.Label(master, text="Zeit übrig: 30 Sekunden")
        self.timer_label.pack(pady=10)
        
        self.next_button = tk.Button(master, text="Nächste Frage", command=self.next_question)
        self.next_button.pack(pady=5)
        
        self.save_button = tk.Button(master, text="Ergebnisse speichern", command=self.save_results)
        self.save_button.pack(pady=5)
        
        self.lade_fragen()
    
    def lade_fragen(self):
        if self.aktuelle_frage_index < len(self.fragen):
            aktuelle_frage = self.fragen[self.aktuelle_frage_index]
            self.frage_label.config(text=aktuelle_frage["frage"])
            for i, option in enumerate(aktuelle_frage["option"]):
                self.radio_buttons[i].config(text=option, value=option)
            for rb in self.radio_buttons[len(aktuelle_frage["option"]):]:
                rb.pack_forget()  # versteckt ungenutzte Radiobuttons
            
            self.var.set("")  # setzt die Auswahl zurück
            self.start_timer()
        else:
            messagebox.showinfo("Quiz beendet", f"Quiz beendet! Dein Punktestand: {self.punkte}")
            self.master.quit()
    def start_timer(self):
        self.timer = 30
        self.update_timer_label()
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join()
        self.timer_thread = threading.Thread(target=self.run_timer)
        self.timer_thread.start()

    def run_timer(self):
        while self.timer > 0:
            time.sleep(1)
            self.timer -= 1
            self.update_timer_label()
        messagebox.showinfo("Zeit abgelaufen", "Die Zeit ist abgelaufen!")
        self.next_question()

    def update_timer_label(self):
        self.timer_label.config(text=f"Zeit übrig: {self.timer} Sekunden")
    def next_question(self):
        selected_answer = self.var.get()
        if selected_answer == self.fragen[self.aktuelle_frage_index]["answer"]:
            self.punkte += 1
        
        self.aktuelle_frage_index += 1
        self.lade_fragen()
    def save_results(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", 
                                                  filetypes=[("JSON Dateien", "*.json"), ("Alle Dateien", "*.*")])
        if file_path:
            results = {
                "punkte": self.punkte,
                "alle_fragen": len(self.fragen)
            }
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("Ergebnisse gespeichert", "Deine Ergebnisse wurden erfolgreich gespeichert.")
            except IOError as e:
                messagebox.showerror("Fehler", f"Fehler beim Speichern der Datei: {e}")
    def load_results(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Dateien", "*.json"), ("Alle Dateien", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    results = json.load(f)
                messagebox.showinfo("Ergebnisse geladen", f"Dein Punktestand: {results['punkte']} von {results['alle_fragen']}")
            except IOError as e:
                messagebox.showerror(f"Fehler beim Laden der Datei: {e}")
            except json.JSONDecodeError as e:
                messagebox.showerror(f"Ungültiges JSON-Format: {e}")
if __name__ == "__main__":
    root = tk.Tk()
    quiz_app = DieErsteQuizApp(root)
    root.mainloop()

