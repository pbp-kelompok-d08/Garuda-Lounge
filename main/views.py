import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from .models import LandingPage


# MAIN PAGE 
@login_required(login_url='/login')
def show_main(request):
    items = [
        {"title": "Jelajahi Jadwal Match", "link": "/match/"},
        {"title": "Daftar Pemain Aktif", "link": "#"},
        {"title": "Koleksi Merchandise", "link": "/merchandise/"},
        {"title": "Baca Berita Menarik", "link": "/news/"},
        {"title": "Galeri Pemain Legend", "link": "#"},
    ]

    context = {
        "items": items,
        "username": request.user.username,
        "last_login": request.COOKIES.get("last_login", "Belum pernah login")
    }

    return render(request, "landing.html", context)


@login_required(login_url='/login')
def show_landingpage(request):
    data = LandingPage.objects.all()
    return render(request, "landing_list.html", {"landing_list": data})


# LOGIN 
def login_user(request):
    if request.user.is_authenticated:
        return redirect('main:show_main')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Simpan waktu login ke cookie
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, "Username atau password salah!")
            return redirect('main:login_user')

    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# LOGOUT 
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login_user'))
    response.delete_cookie('last_login')
    return response


# REGISTER 
def register_user(request):
    if request.user.is_authenticated:
        return redirect('main:show_main')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Akun berhasil dibuat! Silakan login.")
            return redirect('main:login_user')
        else:
            messages.error(request, "Pendaftaran gagal. Coba lagi ya!")
            return redirect('main:register_user')

    form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


#  (JSON & XML) 
def show_json(request):
    data = LandingPage.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def show_xml(request):
    data = LandingPage.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
