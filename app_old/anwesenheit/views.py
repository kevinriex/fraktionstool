# Anwesenheitsmatrix
from django.http import HttpResponseForbidden

def anwesenheit_matrix(request):
    user = request.user
    # Zugriff nur für admin, buero, oder Funktion=Ratsmitglied
    if user.is_superuser or user.groups.filter(name__in=["admin", "buero"]).exists():
        pass
    else:
        person = getattr(user, "person", None)
        if not person or not person.funktion or person.funktion.name.lower() != "ratsmitglied":
            return HttpResponseForbidden("Keine Berechtigung für die Anwesenheitsmatrix.")
    from django.db.models import Prefetch
    personen = Person.objects.all()
    termine = Termin.objects.select_related('gremium', 'ort').prefetch_related('anwesende')
    return render(request, 'anwesenheit/anwesenheit_matrix.html', {'personen': personen, 'termine': termine})

from django.shortcuts import render, redirect
from anwesenheit.models import Gremium, Funktion, Person, Termin, Ort
from django.urls import reverse
from django.views.decorators.http import require_http_methods

def gremium_list(request):
    gremien = Gremium.objects.all()
    return render(request, 'anwesenheit/gremium_list.html', {'gremien': gremien})


def funktion_list(request):
    funktionen = Funktion.objects.all()
    return render(request, 'anwesenheit/funktion_list.html', {'funktionen': funktionen})

@require_http_methods(["GET", "POST"])
def funktion_add(request):
    if request.method == "POST":
        name = request.POST.get('name')
        abgabe = request.POST.get('abgabe')
        if name and abgabe:
            Funktion.objects.create(name=name, abgabe=abgabe)
            return redirect('funktion_list')
    return render(request, 'anwesenheit/funktion_add.html')


def person_list(request):
    personen = Person.objects.all()
    return render(request, 'anwesenheit/person_list.html', {'personen': personen})

@require_http_methods(["GET", "POST"])
def person_add(request):
    funktionen = Funktion.objects.all()
    gremien = Gremium.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        funktion_id = request.POST.get('funktion')
        gremien_ids = request.POST.getlist('gremien')
        if name and email:
            person = Person.objects.create(
                name=name,
                email=email,
                funktion_id=funktion_id if funktion_id else None
            )
            person.gremien.set(gremien_ids)
            return redirect('person_list')
    return render(request, 'anwesenheit/person_add.html', {'funktionen': funktionen, 'gremien': gremien})

@require_http_methods(["GET", "POST"])
def termin_add(request):
    if request.method == "POST":
        ort_id = request.POST.get('ort')
        datum = request.POST.get('datum')
        gremium_id = request.POST.get('gremium')
        anwesende_ids = request.POST.getlist('anwesende')
        if ort_id and datum and gremium_id:
            termin = Termin.objects.create(
                ort_id=ort_id,
                datum=datum,
                gremium_id=gremium_id
            )
            termin.anwesende.set(anwesende_ids)
            return redirect(reverse('gremium_list'))
    gremien = Gremium.objects.all()
    personen = Person.objects.all()
    orte = Ort.objects.all()
    return render(request, 'anwesenheit/termin_form.html', {'gremien': gremien, 'personen': personen, 'orte': orte})
# Orte
def ort_list(request):
    orte = Ort.objects.all()
    return render(request, 'anwesenheit/ort_list.html', {'orte': orte})

@require_http_methods(["GET", "POST"])
def ort_add(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            Ort.objects.create(name=name)
            return redirect('ort_list')
    return render(request, 'anwesenheit/ort_add.html')

# Create your views here.

@require_http_methods(["GET", "POST"])
def gremium_add(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            Gremium.objects.create(name=name)
            return redirect('gremium_list')
    return render(request, 'anwesenheit/gremium_add.html')
def home(request):
    return render(request,"anwesenheit/home.html")