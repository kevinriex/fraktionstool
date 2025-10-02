from anwesenheit.models import Gremium, Funktion, Person, Ort, Termin
from django.utils import timezone

# Orte
orte = []
for name in ["Rathaus", "Bürgerhaus", "Sitzungssaal A", "Sitzungssaal B", "Online"]:
    orte.append(Ort.objects.create(name=name))

# Gremien
gremien = []
for name in ["Fraktion", "Ausschuss 1", "Ausschuss 2", "Vorstand", "Arbeitskreis"]:
    gremien.append(Gremium.objects.create(name=name))

# Funktionen
funktion_mitglied = Funktion.objects.create(name="Mitglied", abgabe=0.00)
funktion_vorsitz = Funktion.objects.create(name="Vorsitzender", abgabe=100.00)

# Personen
personen = []
personendaten = [
    ("Person A", "a@example.com", funktion_mitglied),
    ("Person B", "b@example.com", funktion_mitglied),
    ("Person C", "c@example.com", funktion_vorsitz),
    ("Person D", "d@example.com", funktion_mitglied),
    ("Person E", "e@example.com", funktion_mitglied),
]
for name, email, funktion in personendaten:
    p = Person.objects.create(name=name, email=email, funktion=funktion)
    personen.append(p)
    p.gremien.set(gremien)  # Jede Person in jedem Gremium

# Termine (2 pro Gremium, Orte rotierend)
from datetime import datetime, timedelta
termine = []
start = datetime(2025, 10, 1, 18, 0)
for i, gremium in enumerate(gremien):
    for j in range(2):
        ort = orte[(i + j) % len(orte)]
        datum = start + timedelta(days=i*2 + j, hours=j)
        termin = Termin.objects.create(gremium=gremium, ort=ort, datum=datum)
        termin.anwesende.set(personen)  # Alle Personen anwesend
        termine.append(termin)
print("Testdaten erfolgreich erstellt.")
