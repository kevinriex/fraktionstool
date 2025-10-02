from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("anwesenheit:anwesenheit_matrix")
        else:
            return render(request, "auth/login.html", {"error": "Login fehlgeschlagen"})
    return render(request, "auth/login.html")

def logout_view(request):
    logout(request)
    return redirect("auth:login")

@login_required
def meine_anwesenheiten(request):
    person = getattr(request.user, "person", None)
    termine = []
    if person:
        termine = person.termine.all().select_related("gremium", "ort")
    return render(request, "auth/meine_anwesenheiten.html", {"termine": termine})
