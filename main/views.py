import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import LandingPage


# MAIN PAGE 
@login_required(login_url='/login')
def show_main(request):
    items = [
        {"title": "Jelajahi Jadwal Match", "link": "#"},
        {"title": "Daftar Pemain Aktif", "link": "#"},
        {"title": "Koleksi Merchandise", "link": "#"},
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


# LOGIN (form biasa, tetap dipakai untuk render halaman)
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


# LOGIN AJAX (untuk handle request AJAX)
@csrf_exempt
def login_ajax(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                "status": True,
                "message": "Login berhasil!",
                "username": user.username
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Username atau password salah."
            }, status=401)
    
    return JsonResponse({
        "status": False,
        "message": "Invalid request method."
    }, status=400)


# LOGOUT 
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login_user'))
    response.delete_cookie('last_login')
    return response


# REGISTER (form biasa, tetap dipakai untuk render halaman)
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


# REGISTER AJAX (untuk handle request AJAX)
@csrf_exempt
def register_ajax(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validasi password match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Password tidak cocok!"
            }, status=400)
        
        # Validasi username sudah ada
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username sudah digunakan!"
            }, status=400)
        
        # Validasi password terlalu pendek (minimal 8 karakter)
        if len(password1) < 8:
            return JsonResponse({
                "status": False,
                "message": "Password minimal 8 karakter!"
            }, status=400)
        
        # Buat user baru
        try:
            user = User.objects.create_user(username=username, password=password1)
            user.save()
            
            return JsonResponse({
                "status": True,
                "message": "Registrasi berhasil! Silakan login."
            }, status=201)
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": f"Terjadi kesalahan: {str(e)}"
            }, status=500)
    
    return JsonResponse({
        "status": False,
        "message": "Invalid request method."
    }, status=400)


# JSON & XML
def show_json(request):
    data = LandingPage.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def show_xml(request):
    data = LandingPage.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")