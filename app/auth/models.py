
from django.db import models
from django.contrib.auth.models import User
from presence.models import Committee, Function


# Person: Name, Username, Email, Function, Committee membership, User link
class Person(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Benutzer")
	username = models.CharField(max_length=150, unique=True, verbose_name="Benutzername")
	name = models.CharField(max_length=100, verbose_name="Name")
	email = models.EmailField(verbose_name="E-Mail")
	function = models.ForeignKey(Function, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Funktion")
	committees = models.ManyToManyField(Committee, related_name="members", verbose_name="Gremien")

	def __str__(self):
		return self.name
