from django.shortcuts import render

# Create your views here.
def presence(request):
    return render(request, "presence/presence.html")