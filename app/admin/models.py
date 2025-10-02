# Modelle für Admin-Panel
from django.db import models

class Committee(models.Model):
	name = models.CharField(max_length=100, verbose_name="Gremium")

	def __str__(self):
		return self.name

class Location(models.Model):
	name = models.CharField(max_length=200, verbose_name="Ort")

	def __str__(self):
		return self.name

from django.contrib.auth.models import User

class Appointment(models.Model):
	committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name="appointments", verbose_name="Gremium")
	location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL, verbose_name="Ort")
	date = models.DateTimeField(verbose_name="Datum")
	attendees = models.ManyToManyField(User, blank=True, related_name="attended_appointments", verbose_name="Anwesende")

	def __str__(self):
		return f"{self.committee} am {self.date:%d.%m.%Y %H:%M} in {self.location}"
