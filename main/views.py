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
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
import requests
from django.utils.html import strip_tags
import json
from match.models import Pertandingan


# MAIN PAGE 
@login_required(login_url='/login')
def show_main(request):
    items = [
        {"title": "Jelajahi Jadwal Match", "link": "/match/"},
        {"title": "Daftar Pemain Aktif", "link": reverse("ProfileAktif:show_main")},
        {"title": "Koleksi Merchandise", "link": "/merchandise/"},
        {"title": "Baca Berita Menarik", "link": "/news/"},
        {"title": "Galeri Pemain Legend", "link": "/ProfileLegend/"},
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
@require_POST
@csrf_protect
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

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)
    
@csrf_exempt
def create_match_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        jenis_pertandingan = data.get("jenis_pertandingan", "")
        tim_tuan_rumah = strip_tags(data.get("tim_tuan_rumah", "")) # Strip HTML tags
        tim_tamu =  strip_tags(data.get("tim_tamu", "")) # Strip HTML tags
        bendera_tuan_rumah = data.get("bendera_tuan_rumah", "")
        bendera_tamu = data.get("bendera_tamu", "")
        tanggal = data.get("tanggal", "")
        stadion = data.get("stadion", "")
        skor_tuan_rumah = data.get("skor_tuan_rumah", "")
        skor_tamu = data.get("skor_tamu", "")
        pencetak_gol_tuan_rumah = data.get("pencetak_gol_tuan_rumah", "")
        pencetak_gol_tamu = data.get("pencetak_gol_tamu", "")
        starter_tuan_rumah = data.get("starter_tuan_rumah", "")
        starter_tamu = data.get("starter_tamu", "")
        pengganti_tuan_rumah = data.get("pengganti_tuan_rumah", "")
        pengganti_tamu = data.get("pengganti_tamu", "")
        manajer_tuan_rumah = data.get("manajer_tuan_rumah", "")
        manajer_tamu = data.get("manajer_tamu", "")
        highlight = data.get("highlight", "")
        penguasaan_bola_tuan_rumah = data.get("penguasaan_bola_tuan_rumah", "")
        penguasaan_bola_tamu = data.get("penguasaan_bola_tamu", "")
        tembakan_tuan_rumah = data.get("tembakan_tuan_rumah", "")
        tembakan_tamu = data.get("tembakan_tamu", "")
        on_target_tuan_rumah = data.get("on_target_tuan_rumah", "")
        on_target_tamu = data.get("on_target_tamu", "")
        akurasi_umpan_tuan_rumah = data.get("akurasi_umpan_tuan_rumah", "")
        akurasi_umpan_tamu = data.get("akurasi_umpan_tamu", "")
        pelanggaran_tuan_rumah = data.get("pelanggaran_tuan_rumah", "")
        pelanggaran_tamu = data.get("pelanggaran_tamu", "")
        kartu_kuning_tuan_rumah = data.get("kartu_kuning_tuan_rumah", "")
        kartu_kuning_tamu = data.get("kartu_kuning_tamu", "")
        kartu_merah_tuan_rumah = data.get("kartu_merah_tuan_rumah", "")
        kartu_merah_tamu = data.get("kartu_merah_tamu", "")
        offside_tuan_rumah = data.get("offside_tuan_rumah", "")
        offside_tamu = data.get("offside_tamu", "")
        corner_tuan_rumah = data.get("corner_tuan_rumah", "")
        corner_tamu = data.get("corner_tamu", "")
        # user = request.user
        
        new_match = Pertandingan(
            jenis_pertandingan=jenis_pertandingan, 
            tim_tuan_rumah=tim_tuan_rumah,
            tim_tamu=tim_tamu,
            bendera_tuan_rumah=bendera_tuan_rumah,
            bendera_tamu=bendera_tamu,
            tanggal=tanggal,
            stadion=stadion,
            skor_tuan_rumah=skor_tuan_rumah,
            skor_tamu=skor_tamu,
            pencetak_gol_tuan_rumah=pencetak_gol_tuan_rumah,
            pencetak_gol_tamu=pencetak_gol_tamu,
            starter_tuan_rumah=starter_tuan_rumah,
            starter_tamu=starter_tamu,
            pengganti_tuan_rumah=pengganti_tuan_rumah,
            pengganti_tamu=pengganti_tamu,
            manajer_tuan_rumah=manajer_tuan_rumah,
            manajer_tamu=manajer_tamu,
            highlight=highlight,
            penguasaan_bola_tuan_rumah=penguasaan_bola_tuan_rumah,
            penguasaan_bola_tamu=penguasaan_bola_tamu,
            tembakan_tuan_rumah=tembakan_tuan_rumah,
            tembakan_tamu=tembakan_tamu,
            on_target_tuan_rumah=on_target_tuan_rumah,
            on_target_tamu=on_target_tamu,
            akurasi_umpan_tuan_rumah=akurasi_umpan_tuan_rumah,
            akurasi_umpan_tamu=akurasi_umpan_tamu,
            pelanggaran_tuan_rumah=pelanggaran_tuan_rumah,
            pelanggaran_tamu=pelanggaran_tamu,
            kartu_kuning_tuan_rumah=kartu_kuning_tuan_rumah,
            kartu_kuning_tamu=kartu_kuning_tamu,
            kartu_merah_tuan_rumah=kartu_merah_tuan_rumah,
            kartu_merah_tamu=kartu_merah_tamu,
            offside_tuan_rumah=offside_tuan_rumah,
            offside_tamu=offside_tamu,
            corner_tuan_rumah=corner_tuan_rumah,
            corner_tamu=corner_tamu,
            # user=user
        )
        new_match.save()
        
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)