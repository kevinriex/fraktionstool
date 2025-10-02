from django.urls import path
from . import views

app_name = "app_admin"

urlpatterns = [
    path("", views.home, name="admin_home"),
    path("presence/", views.presence_admin_panel, name="presence_admin_panel"),
    path("users/", views.user_admin_panel, name="user_admin_panel"),
    path("committees/", views.committee_admin_panel, name="committee_admin_panel"),
    path("locations/", views.location_admin_panel, name="location_admin_panel"),
    path("appointments/", views.appointment_admin_panel, name="appointment_admin_panel"),
]
