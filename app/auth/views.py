from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
def logout(request):
    auth_logout(request)
    return redirect('login')  # Change 'login' to your login url name if different
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Change 'home' to your desired redirect target
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'auth/login.html')