from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.core import serializers
from .models import LandingPage

@login_required(login_url='/login')
def show_main(request):
    items = [
        {"title": "Jelajahi Jadwal Match", "link": "#"},
        {"title": "Daftar Pemain Aktif", "link": "#"},
        {"title": "Koleksi Merchandise", "link": "/merchandise/"},
        {"title": "Baca Berita Menarik", "link": "/news/"},
        {"title": "Galeri Pemain Legend", "link": "#"},
    ]
    return render(request, "landing.html", {"items": items})

@login_required(login_url='/login')
def show_landingpage(request):
    data = LandingPage.objects.all()
    return render(request, "landing_list.html", {"landing_list": data})


def login_user(request):
    # Kalau udah login, jangan bisa buka /login lagi
    if request.user.is_authenticated:
        return redirect('main:show_main')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login berhasil! Selamat datang.")
            return redirect('main:show_main')
        else:
            messages.error(request, "Username atau password salah!")
            # redirect biar message gak keulang tiap refresh
            return redirect('main:login_user')

    # GET request
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, "Berhasil logout.")
    return redirect('main:login_user')


def register_user(request):
    # Kalau udah login, langsung ke main
    if request.user.is_authenticated:
        return redirect('main:show_main')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Akun berhasil dibuat! Silakan login.")
            return redirect('main:login_user')
        else:
            # kasih tahu kalau ada error di form
            messages.error(request, "Pendaftaran gagal. Pastikan form terisi dengan benar.")
            return redirect('main:register_user')

    # GET request
    form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def show_json(request):
    data = LandingPage.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def show_xml(request):
    data = LandingPage.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")