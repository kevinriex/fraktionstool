from django.contrib import admin
from anwesenheit.models import Funktion, Gremium, Person, Termin, Ort

@admin.register(Funktion)
class FunktionAdmin(admin.ModelAdmin):
	list_display = ("name", "abgabe")

@admin.register(Gremium)
class GremiumAdmin(admin.ModelAdmin):
	list_display = ("name",)

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "funktion")
	list_filter = ("funktion", "gremien")
	search_fields = ("name", "email")

@admin.register(Ort)
class OrtAdmin(admin.ModelAdmin):
	list_display = ("name",)

@admin.register(Termin)
class TerminAdmin(admin.ModelAdmin):
	list_display = ("gremium", "ort", "datum")
	list_filter = ("gremium", "ort", "datum")
	search_fields = ("gremium__name", "ort__name")

# Register your models here.
