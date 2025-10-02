from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    user = request.user
    is_admin_or_buero = False
    if user.is_authenticated:
        is_admin_or_buero = user.is_superuser or user.groups.filter(name="buero").exists()
    return render(request, "home/home.html", {"is_admin_or_buero": is_admin_or_buero})