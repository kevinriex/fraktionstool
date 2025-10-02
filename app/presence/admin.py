
from django.contrib import admin
from .models import Committee, Location, Appointment, Person

@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
	list_display = ("name",)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
	list_display = ("name",)


# Admin für Termine (Appointment)
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
	list_display = ("committee", "location", "date")
	list_filter = ("committee", "location", "date")
	search_fields = ("committee__name", "location__name")
	filter_horizontal = ("attendees",)


# Optional: Person-Admin für Auswahl der Teilnehmenden
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
	list_display = ("name",)
