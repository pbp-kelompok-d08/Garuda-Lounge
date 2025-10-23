import uuid
from django.shortcuts import render, redirect, get_object_or_404
from ProfileAktif.forms import PlayerForm
from ProfileAktif.models import Player
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required


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
    form = PlayerForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('ProfileAktif:show_main')

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

def show_json(request):
    player_list = Player.objects.all()
    json_data = serializers.serialize("json", player_list)
    return HttpResponse(json_data, content_type="application/json")

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