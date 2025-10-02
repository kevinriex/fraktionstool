
app_name = "anwesenheit"
from django.urls import path
from . import views

urlpatterns = [
    path('gremien/', views.gremium_list, name='gremium_list'),
    path('gremien/neu/', views.gremium_add, name='gremium_add'),
    path('funktionen/', views.funktion_list, name='funktion_list'),
    path('funktionen/neu/', views.funktion_add, name='funktion_add'),
    path('personen/', views.person_list, name='person_list'),
    path('personen/neu/', views.person_add, name='person_add'),
    path('termin/anlegen/', views.termin_add, name='termin_add'),
    path('orte/', views.ort_list, name='ort_list'),
    path('orte/neu/', views.ort_add, name='ort_add'),

    path('anwesenheit/', views.anwesenheit_matrix, name='anwesenheit_matrix'),
]
