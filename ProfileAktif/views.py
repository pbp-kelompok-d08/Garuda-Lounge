import uuid
import json
import requests

from django.shortcuts import render, redirect, get_object_or_404
from ProfileAktif.forms import PlayerForm
from ProfileAktif.models import Player
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.utils.html import strip_tags



# 🌟 halaman utama (show semua pemain, atau tampilkan Marselino kalau kosong)
@login_required(login_url='/login')
def show_main(request):
    players = Player.objects.all()

    if not players.exists():
        context = {
            'players': [
                {
                    "id": uuid.uuid4(),
                    'nama': 'Marselino Ferdinan',
                    'posisi': 'Gelandang Serang',
                    'klub': 'KMSK Deinze (Belgia)',
                    'umur': 20,
                    'market_value': '€2.00 juta',
                    'foto': 'https://upload.wikimedia.org/wikipedia/commons/2/24/Marselino_Ferdinan_2023.jpg',
                    'is_dummy': True,  # tambahin flag
                }
            ]
        }
    else:
        context = {'players': players}

    return render(request, "main.html", context)



# 🌟 form untuk tambah pemain baru
def create_player(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        
        if form.is_valid():
            player = form.save()
            
            # SELALU return JSON untuk AJAX
            return JsonResponse({
                'success': True,
                'player_id': str(player.id),
                'message': 'Pemain berhasil ditambahkan'
            })
        else:
            # Jika form tidak valid
            return JsonResponse({
                'success': False,
                'errors': dict(form.errors)
            }, status=400)
    
    else:
        form = PlayerForm()
    
    return render(request, "create_player.html", {'form': form})


# 🌟 halaman detail satu pemain
@login_required(login_url='/login')
def show_player(request, id):
    player = None

    # Coba ambil dari database
    try:
        player = Player.objects.get(id=id)
    except Player.DoesNotExist:
        # Kalau gak ada, buat dummy player biar gak error
        player = {
            'nama': 'Marselino Ferdinan',
            'posisi': 'Gelandang Serang',
            'klub': 'KMSK Deinze (Belgia)',
            'umur': 20,
            'market_value': '2.00 juta',
            'foto': 'https://upload.wikimedia.org/wikipedia/commons/2/24/Marselino_Ferdinan_2023.jpg',
        }

    return render(request, "player_detail.html", {'player': player})

def show_xml(request):
    player_list = Player.objects.all()
    xml_data = serializers.serialize("xml", player_list)
    return HttpResponse(xml_data, content_type="application/xml")

from django.http import JsonResponse

def show_json(request):
    players = Player.objects.all()
    data = [
        {
            'id': str(p.id),
            'nama': p.nama,
            'posisi': p.get_posisi_display(),  # teks untuk ditampilkan
            'posisi_kode': p.posisi,           # kode GK/DF/MF/FW untuk <select>
            'klub': p.klub,
            'umur': p.umur,
            'market_value': float(p.market_value),
            'foto': p.foto,
        }
        for p in players
    ]
    return JsonResponse(data, safe=False)



def show_xml_by_id(request, player_id):
    try:
        player_item = Player.objects.filter(pk=player_id)
        xml_data = serializers.serialize("xml", player_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Player.DoesNotExist:
        return HttpResponse(status=404)
    
def show_json_by_id(request, player_id):
    try:
        player_item = Player.objects.get(pk=player_id)
        json_data = serializers.serialize("json", [player_item])
        return HttpResponse(json_data, content_type="application/json")
    except Player.DoesNotExist:
        return HttpResponse(status=404)
    
@csrf_exempt
@require_POST
def add_player_ajax(request):
    nama = request.POST.get("nama")
    posisi = request.POST.get("position")
    umur = request.POST.get("age")
    klub = request.POST.get("team")
    foto = request.POST.get("photo")
    user = request.user

    new_player = Player(
        nama=nama,
        posisi=posisi,
        umur=umur,
        klub=klub,
        foto=foto,
        user=user
    )
    new_player.save()

    return HttpResponse(b"CREATED", status=201)

@login_required(login_url='/login')
def edit_player(request, id):
    player = get_object_or_404(Player, pk=id)

    if request.method == "POST":
        form = PlayerForm(request.POST, instance=player)

        if form.is_valid():
            player = form.save()

            # kalau dari AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'player_id': str(player.id),
                })

            # fallback biasa
            return redirect('ProfileAktif:show_main')

        # form tidak valid, kirim error ke AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': dict(form.errors),
            }, status=400)

    # fallback GET (jarang dipakai sekarang)
    form = PlayerForm(instance=player)
    context = {'form': form, 'player': player}
    return render(request, "edit_player.html", context)


@login_required(login_url='/login')
def delete_player(request, id):
    player = get_object_or_404(Player, pk=id)

    # request dari AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        player.delete()
        return JsonResponse({'success': True})

    # fallback biasa (kalau dipanggil via link)
    player.delete()
    return HttpResponseRedirect(reverse('ProfileAktif:show_main'))

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36",
            "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            "Referer": "https://www.okezone.com/",
        }

        response = requests.get(
            image_url,
            headers=headers,
            timeout=10,
            stream=True,
        )
        response.raise_for_status()

        return HttpResponse(
            response.content,
            content_type=response.headers.get(
                'Content-Type', 'image/jpeg'
            ),
        )

    except requests.RequestException as e:
        return HttpResponse(
            f'Error fetching image: {str(e)}',
            status=500,
        )

@csrf_exempt
def create_player_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        nama = strip_tags(data.get("nama", ""))
        posisi = data.get("posisi", "")          # pakai kode posisi, misal "MF"
        klub = strip_tags(data.get("klub", ""))
        umur = data.get("umur", 0)
        market_value = data.get("market_value", 0)
        foto = data.get("foto", "")

        new_player = Player(
            nama=nama,
            posisi=posisi,
            klub=klub,
            umur=umur,
            market_value=market_value,
            foto=foto,
        )
        new_player.save()

        return JsonResponse({"status": "success"}, status=200)
    return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
@require_POST
def delete_player_flutter(request, id):
    try:
        player = Player.objects.get(pk=id)
        player.delete()
        return JsonResponse({"status": "success"}, status=200)
    except Player.DoesNotExist:
        return JsonResponse({"status": "not_found"}, status=404)

@csrf_exempt
def edit_player_flutter(request, id):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

    try:
        player = Player.objects.get(pk=id)
    except Player.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Player not found"}, status=404)

    try:
        data = json.loads(request.body)

        player.nama = strip_tags(data.get("nama", player.nama))
        player.posisi = data.get("posisi", player.posisi)
        player.klub = strip_tags(data.get("klub", player.klub))
        player.umur = int(data.get("umur", player.umur))

        # PENTING: DecimalField → CAST KE STRING
        player.market_value = str(data.get("market_value", player.market_value))

        player.foto = data.get("foto", player.foto)

        player.save()

        return JsonResponse({
            "status": "success",
            "player_id": str(player.id)
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)
