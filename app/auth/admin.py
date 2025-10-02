from django.contrib import admin
from .models import Position, Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ("user", "geburtsdatum", "telefonnummer", "position")
	search_fields = ("user__username", "telefonnummer", "position__name")


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
	list_display = ("name", "basisentschaedigung", "sitzungsgeld", "basis_abgabe", "sitzungsabgabe")
	search_fields = ("name",)


