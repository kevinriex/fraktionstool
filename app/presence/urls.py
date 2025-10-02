from django.urls import path
from . import views

app_name = "presence"

urlpatterns = [
    path("", views.presence, name="home")
]
