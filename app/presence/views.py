from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from admin.models import Appointment

@login_required
def presence(request):
    user = request.user
    appointments = Appointment.objects.filter(attendees=user).select_related('committee', 'location').order_by('-date')
    return render(request, "presence/presence.html", {"appointments": appointments})