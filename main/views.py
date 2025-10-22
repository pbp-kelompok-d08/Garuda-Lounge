from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def show_main(request):
    items = [
        {"title": "Lihat Match", "link": "#"},
        {"title": "Lihat Pemain", "link": "#"},
        {"title": "Lihat Merch", "link": "#"},
        {"title": "Lihat News", "link": "#"},
        {"title": "Lihat Legend", "link": "#"},
    ]
    return render(request, "landing.html", {"items": items})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main:show_main')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('main:login_user')

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:login_user')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
