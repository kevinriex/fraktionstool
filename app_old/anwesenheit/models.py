
from django.db import models
from django.contrib.auth.models import User

# Funktion: z.B. Vorsitzender, Mitglied, etc. mit Abgabe
class Funktion(models.Model):
	name = models.CharField(max_length=100)
	abgabe = models.DecimalField(max_digits=8, decimal_places=2, help_text="Abgabe in Euro")

	def __str__(self):
		return self.name

# Gremium: z.B. Ausschuss, Vorstand, etc.
class Gremium(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

# Person: Name, E-Mail, Funktion, Gremienzugehörigkeit, User-Verknüpfung
class Person(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=100)
	email = models.EmailField()
	funktion = models.ForeignKey(Funktion, on_delete=models.SET_NULL, null=True, blank=True)
	gremien = models.ManyToManyField(Gremium, related_name="mitglieder")

	def __str__(self):
		return self.name


# Ort: z.B. Rathaus, Sitzungssaal, etc.
class Ort(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

# Termin: Gremium, Ort (ForeignKey), Datum (mit Uhrzeit), Liste an Anwesenden
class Termin(models.Model):
	gremium = models.ForeignKey(Gremium, on_delete=models.CASCADE, related_name="termine")
	ort = models.ForeignKey(Ort, on_delete=models.SET_NULL, null=True)
	datum = models.DateTimeField()
	anwesende = models.ManyToManyField(Person, related_name="termine")

	def __str__(self):
		return f"{self.gremium.name} {self.datum:%d.%m.%Y %H:%M}"

# Create your models here.
