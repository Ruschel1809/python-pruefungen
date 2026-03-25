import unittest
import buecherverwaltung

class TestBuecherverwaltung(unittest.TestCase):
    def setUp(self):
        # Vor jedem Test die Datenbank zurücksetzen
        buecherverwaltung.buecherei_datenbank.clear()
        buecherverwaltung.buecherei_datenbank.extend([
            {"Titel": "Python mit Biss", "Autor": "Michael Hartl", "Jahr": 2025},
            {"Titel": "Python für Kinder", "Autor": "Florian André Dalwigk", "Jahr": 2025},
            {"Titel": "Python Programming", "Autor": "Guido van Rossum", "Jahr": 1990},
            {"Titel": "Python Pocket Reference", "Autor": "Mark Lutz", "Jahr": 2002},
            {"Titel": "Einführung in Python", "Autor": "Mark Lutz", "Jahr": 2000}
        ])

    def test_buch_suchen_titel(self):
        result = buecherverwaltung.buch_suchen("Python mit Biss")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Autor"], "Michael Hartl")

    def test_buch_suchen_titel_und_autor(self):
        result = buecherverwaltung.buch_suchen("Python Pocket Reference", "Mark Lutz")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Jahr"], 2002)

    def test_buch_suchen_nicht_vorhanden(self):
        result = buecherverwaltung.buch_suchen("Nicht vorhanden")
        self.assertEqual(result, [])

    def test_fuege_buch_hinzu(self):
        buecherverwaltung.fuege_buch_hinzu("Neues Buch", "Neue Autorin", 2024)
        result = buecherverwaltung.buch_suchen("Neues Buch")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Autor"], "Neue Autorin")
        self.assertEqual(result[0]["Jahr"], 2024)

    def test_buecher_nach_jahr(self):
        result = buecherverwaltung.buecher_nach_jahr(2025)
        self.assertEqual(len(result), 2)
        self.assertTrue(any(buch["Titel"] == "Python mit Biss" for buch in result))

    def test_buecher_nach_jahr_leer(self):
        result = buecherverwaltung.buecher_nach_jahr(1800)
        self.assertEqual(result, [])

    def test_zeige_datenbank(self):
        # Testet nur, ob die Funktion ohne Fehler durchläuft
        try:
            buecherverwaltung.zeige_datenbank()
        except Exception as e:
            self.fail(f"zeige_datenbank() raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()