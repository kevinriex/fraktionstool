
from django.contrib import admin
from .models import Committee, Location, Appointment

@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
	list_display = ("name",)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
	list_display = ("name",)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
	list_display = ("committee", "location", "date")
	list_filter = ("committee", "location", "date")
	search_fields = ("committee__name", "location__name")
