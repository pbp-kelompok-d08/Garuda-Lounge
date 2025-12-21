"""from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login(request):
    # 1. Pastikan metode yang digunakan adalah POST
    if request.method != 'POST':
        return JsonResponse({
            "status": False,
            "message": "Method not allowed. Use POST method."
        }, status=405)

    # 2. Tangani input data yang fleksibel (JSON vs Form Data)
    try:
        # Pilihan 1: Coba baca sebagai JSON dari body request. 
        # Ini adalah standar terbaik saat Flutter mengirim data menggunakan 'Content-Type: application/json'.
        data = json.loads(request.body)
    except json.JSONDecodeError:
        # Pilihan 2: Jika gagal diuraikan sebagai JSON, coba baca dari request.POST.
        # Ini digunakan jika Flutter mengirim data sebagai 'form-urlencoded' atau 'form-data'.
        data = request.POST.dict()
    except Exception:
        # Fallback untuk error lain, masih coba baca dari request.POST.
        data = request.POST.dict()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return JsonResponse({
            "status": False,
            "message": "Username and password are required."
        }, status=400)

    # 3. Logika Autentikasi
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Login status successful.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login successful!"
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login failed, account is disabled."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login failed, please check your username or password."
        }, status=401)
        """