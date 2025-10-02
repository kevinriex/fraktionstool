from django.urls import path
from . import views

app_name = "auth"

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('meine-anwesenheiten/', views.meine_anwesenheiten, name='meine_anwesenheiten'),
]
