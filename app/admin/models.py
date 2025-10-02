from django.db import models
from django.contrib.auth.models import User


# Function: e.g. Chairperson, Member, etc. with fee
class Function(models.Model):
    name = models.CharField(max_length=100, verbose_name="Funktion")
    fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Abgabe in Euro",
        verbose_name="Abgabe",
    )

    def __str__(self):
        return self.name


# Committee: e.g. Committee, Board, etc.
class Committee(models.Model):
    name = models.CharField(max_length=100, verbose_name="Gremium")

    def __str__(self):
        return self.name


# Location: e.g. Town Hall, Meeting Room, etc.
class Location(models.Model):
    name = models.CharField(max_length=200, verbose_name="Ort")

    def __str__(self):
        return self.name



# Appointment: Committee, Location (ForeignKey), Date (with time), List of attendees
class Appointment(models.Model):
    committee = models.ForeignKey(
        Committee,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Gremium",
    )
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, verbose_name="Ort"
    )
    date = models.DateTimeField(verbose_name="Datum")
    def __str__(self):
        return f"{self.committee.name} {self.date:%d.%m.%Y %H:%M}"

    @property
    def attendees(self):
        from auth.models import Person
        return Person.objects.filter(appointments=self)


# Create your models here.
