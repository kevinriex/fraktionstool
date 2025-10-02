from .models import Appointment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
@login_required
def appointment_admin_panel(request):
    from .models import Committee, Location
    appointments = Appointment.objects.select_related('committee', 'location').prefetch_related('attendees').all()
    committees = Committee.objects.all()
    locations = Location.objects.all()
    users = User.objects.all()
    selected_appointment = None
    appointment_id = request.GET.get("appointment")
    if appointment_id:
        selected_appointment = Appointment.objects.filter(id=appointment_id).first()

    if request.method == "POST":
        action = request.POST.get("action")
        attendees_ids = request.POST.getlist("attendees")
        if action == "create":
            committee_id = request.POST.get("committee")
            location_id = request.POST.get("location")
            date = request.POST.get("date")
            if committee_id and date:
                appointment = Appointment.objects.create(
                    committee_id=committee_id,
                    location_id=location_id or None,
                    date=date
                )
                if attendees_ids:
                    appointment.attendees.set(attendees_ids)
                appointments = Appointment.objects.select_related('committee', 'location').prefetch_related('attendees').all()
        elif action == "update" and selected_appointment:
            committee_id = request.POST.get("committee")
            location_id = request.POST.get("location")
            date = request.POST.get("date")
            if committee_id and date:
                selected_appointment.committee_id = committee_id
                selected_appointment.location_id = location_id or None
                selected_appointment.date = date
                selected_appointment.save()
                selected_appointment.attendees.set(attendees_ids)
        elif action == "delete" and selected_appointment:
            selected_appointment.delete()
            selected_appointment = None
            appointments = Appointment.objects.select_related('committee', 'location').prefetch_related('attendees').all()

    return render(request, "admin/appointment_admin_panel.html", {
        "appointments": appointments,
        "selected_appointment": selected_appointment,
        "committees": committees,
        "locations": locations,
        "users": users,
    })
from .models import Location
from django.contrib.auth.decorators import login_required
@login_required
def location_admin_panel(request):
    locations = Location.objects.all()
    selected_location = None
    location_id = request.GET.get("location")
    if location_id:
        selected_location = Location.objects.filter(id=location_id).first()

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create":
            name = request.POST.get("name", "").strip()
            if name:
                Location.objects.create(name=name)
                locations = Location.objects.all()
        elif action == "update" and selected_location:
            name = request.POST.get("name", "").strip()
            if name:
                selected_location.name = name
                selected_location.save()
        elif action == "delete" and selected_location:
            selected_location.delete()
            selected_location = None
            locations = Location.objects.all()

    return render(request, "admin/location_admin_panel.html", {
        "locations": locations,
        "selected_location": selected_location,
    })
from .models import Committee

@login_required
def committee_admin_panel(request):
    committees = Committee.objects.all()
    selected_committee = None
    committee_id = request.GET.get("committee")
    if committee_id:
        selected_committee = Committee.objects.filter(id=committee_id).first()

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create":
            name = request.POST.get("name", "").strip()
            if name:
                Committee.objects.create(name=name)
                committees = Committee.objects.all()
        elif action == "update" and selected_committee:
            name = request.POST.get("name", "").strip()
            if name:
                selected_committee.name = name
                selected_committee.save()
        elif action == "delete" and selected_committee:
            selected_committee.delete()
            selected_committee = None
            committees = Committee.objects.all()

    return render(request, "admin/committee_admin_panel.html", {
        "committees": committees,
        "selected_committee": selected_committee,
    })

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from auth.models import Profile, Position

@login_required
def user_admin_panel(request):
    User = get_user_model()
    users = User.objects.all()
    positions = Position.objects.all()
    selected_user_id = request.GET.get("user")
    selected_user = None
    selected_profile = None
    if request.method == "POST" and request.GET.get("add_user") == "1":
        # Neuen Benutzer anlegen
        email = request.POST.get("new_email")
        first_name = request.POST.get("new_first_name", "").strip()
        last_name = request.POST.get("new_last_name", "").strip()
        password = request.POST.get("new_password")
        # Username automatisch generieren
        username = ""
        if first_name and last_name:
            username = (first_name[0] + last_name).lower().replace(" ", "")
        new_position_id = request.POST.get("new_position")
        new_geburtsdatum = request.POST.get("new_geburtsdatum")
        new_telefonnummer = request.POST.get("new_telefonnummer")
        if username and password:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            # Profil wird automatisch per Signal angelegt
            try:
                profile = user.profile
                if new_position_id:
                    profile.position_id = new_position_id
                profile.geburtsdatum = new_geburtsdatum or None
                profile.telefonnummer = new_telefonnummer
                profile.save()
            except Exception:
                pass
    elif selected_user_id:
        selected_user = get_object_or_404(User, pk=selected_user_id)
        try:
            selected_profile = selected_user.profile
        except Profile.DoesNotExist:
            selected_profile = None
        # Benutzer- und Profil bearbeiten
        if request.method == "POST" and selected_profile:
            # User-Felder
            selected_user.email = request.POST.get("email", "")
            selected_user.first_name = request.POST.get("first_name", "")
            selected_user.last_name = request.POST.get("last_name", "")
            selected_user.is_active = bool(request.POST.get("is_active"))
            selected_user.save()
            # Profil-Felder
            geburtsdatum = request.POST.get("geburtsdatum")
            telefonnummer = request.POST.get("telefonnummer")
            position_id = request.POST.get("position")
            selected_profile.geburtsdatum = geburtsdatum or None
            selected_profile.telefonnummer = telefonnummer
            if position_id:
                selected_profile.position_id = position_id
            else:
                selected_profile.position = None
            selected_profile.save()
    return render(request, "admin/user_admin_panel.html", {
        "users": users,
        "selected_user": selected_user,
        "selected_profile": selected_profile,
        "positions": positions,
    })

@login_required
def home(request):
    return render(request, "admin/home.html")

@login_required
def presence_admin_panel(request):
    users = None
    appointments = None
    if request.user.is_superuser or request.user.groups.filter(name="buero").exists():
        User = get_user_model()
        users = User.objects.all()
        appointments = []
    return render(request, "admin/presence_admin_panel.html", {"users": users, "appointments": appointments})