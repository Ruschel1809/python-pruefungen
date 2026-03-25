class Buch:
    def __init__(self, titel, autor, kategorie, preis):
        assert(isinstance(titel,str))
        assert(isinstance(autor,str))
        assert(isinstance(kategorie,str))
        assert(isinstance(preis,float))
        self.titel = titel
        self.autor = autor
        self.kategorie = kategorie
        self.preis = preis

    def __str__(self):
        return f"Titel: {self.titel}, Autor: {self.autor}, Kategorie:  {self.kategorie}, Preis: {self.preis} Geld"

    def get_titel(self):
        return self.titel
    def get_autor(self):
        return self.autor
    def get_kategorie(self):
        return self.kategorie
    def get_preis(self):
        return self.preis
    def set_preis(self,preis):
        assert(isinstance(preis,float))
        self.preis = preis

class Buchladen:
    def __init__(self):
        self.inventar=[]

    def hinzufuegen(self, buch):
        if isinstance(buch, Buch):
            self.inventar.append(buch)
        else:
            raise TypeError("Nur Buch-Objekte können hinzugefügt werden")

    def suchen(self, suchbegriff):
        ergebnisse = []
        for buch in self.inventar:
            if suchbegriff.lower() in buch.kategorie.lower():
                ergebnisse.append(buch)
        return ergebnisse

    def get_inventar(self):
        return self.inventar

    @staticmethod
    def gesamtpreis(buecherauswahl):
        summe = 0
        for buch in buecherauswahl:
            summe += buch.preis
        return summe

def main():
    buch1 = Buch("Das Parfüm", "Patrick Süskind", "Thriller", 26.0)
    buch2 = Buch("Illuminati", "Dan Brown", "Thriller", 24.0)
    buch3 = Buch("Der Herr der Ringe", "J.R.R. Tolkien", "Fantasy", 54.0)
    buch4 = Buch("Harry Potter", "J.K. Rowling", "Fantasy", 58.0)
    buch5 = Buch("Dune", "Frank Herbert", "Science-Fiction", 27.0)
    buch6 = Buch("1984", "Georg Orwell", "Science-Fiction", 24.0)

    buchladen = Buchladen()
    buchladen.hinzufuegen(buch1)
    buchladen.hinzufuegen(buch2)
    buchladen.hinzufuegen(buch3)
    buchladen.hinzufuegen(buch4)
    buchladen.hinzufuegen(buch5)
    buchladen.hinzufuegen(buch6)

    fantasy = buchladen.suchen("Fantasy")
    thriller = buchladen.suchen("Thriller")
    scify = buchladen.suchen("Science-Fiction")
    print(f"Fantasy-Reihe:")
    for buch in fantasy:
        print(buch)
    print(f"Thriller-Reihe:")
    for buch in thriller:
        print(buch)
    print(f"Science-Fiction-Reihe:")
    for buch in scify:
        print(buch)
    preis_fantasy = buchladen.gesamtpreis(fantasy)
    preis_thriller = buchladen.gesamtpreis(thriller)
    preis_scify = buchladen.gesamtpreis(scify)
    preis_alle_buecher = Buchladen.gesamtpreis(buchladen.get_inventar())
    print("Der Gesamtpreis für die Fantasy-Reihe beträgt:",preis_fantasy, "Geld")
    print("Der Gesamtpreis für die Thrille-Reihe beträgt:",preis_thriller, "Geld")
    print("Der Gesamtpreis für die Science-Fiction-Reihe beträgt:",preis_scify, "Geld")
    print("Der Gesamtpreis für das Inventer beträgt:",preis_alle_buecher, "Geld")

if __name__ == "__main__":
    main()