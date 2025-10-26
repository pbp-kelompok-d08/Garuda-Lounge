import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import LegendPlayer
from .forms import LegendPlayerForm 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@login_required(login_url='/login')
def show_profile_legend(request):
    players = LegendPlayer.objects.filter(is_legend=True)

    if not players.exists():
        context = {
            'players': [
                {
                    "id": uuid.uuid4(),
                    'name': 'Bambang Pamungkas',
                    'position': 'Penyerang',
                    'club': 'Persija Jakarta',
                    'age': 45,
                    'photo_url': 'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTM11_YH0U4pF6qZBRQdB3ZNGVE203CPIPCh37soS8FF5u3FOMh-ecB-eMRSwVhy-YBp-R-XY4868o7ua_BKQS3FzA1dasPChpUi1gtpyk',
                    'is_dummy': True,
                }
            ]
        }
    else:
        context = {'players': players}

    return render(request, "show_profile_legend.html", context)

def create_legend(request):
    if request.method == "POST":
        form = LegendPlayerForm(request.POST)

        if form.is_valid():
            player = form.save()
            return JsonResponse({
                'success': True,
                'player_id': str(player.id),
                'message': 'Pemain legend berhasil ditambahkan'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': dict(form.errors)
            }, status=400)
    else:
        form = LegendPlayerForm()
    
    return render(request, "create_legend.html", {'form': form})

@login_required(login_url='/login')
def show_legend_detail(request, id):
    try:
        player = LegendPlayer.objects.get(id=id)
    except LegendPlayer.DoesNotExist:
        player = {
            'name': 'Bambang Pamungkas',
            'position': 'Penyerang',
            'club': 'Persija Jakarta',
            'age': 45,
            'photo_url': 'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTM11_YH0U4pF6qZBRQdB3ZNGVE203CPIPCh37soS8FF5u3FOMh-ecB-eMRSwVhy-YBp-R-XY4868o7ua_BKQS3FzA1dasPChpUi1gtpyk',
        }

    return render(request, "legend_detail.html", {'player': player})

def show_xml(request):
    player_list = LegendPlayer.objects.all()
    xml_data = serializers.serialize("xml", player_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    players = LegendPlayer.objects.all()
    data = [
        {
            'id': str(p.id),
            'name': p.name,
            'position': p.get_position_display(),
            'age': p.age,
            'club': p.club,
            'photo_url': p.photo_url,
            'is_legend': p.is_legend,
        }
        for p in players
    ]
    return JsonResponse(data, safe=False)

def show_xml_by_id(request, id):
    try:
        player_item = LegendPlayer.objects.filter(pk=id, is_legend=True)
        xml_data = serializers.serialize("xml", player_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except LegendPlayer.DoesNotExist:
        return HttpResponse(status=404)
    
def show_json_by_id(request, id):
    try:
        player_item = LegendPlayer.objects.get(pk=id, is_legend=True)
        json_data = serializers.serialize("json", [player_item])
        return HttpResponse(json_data, content_type="application/json")
    except LegendPlayer.DoesNotExist:
        return HttpResponse(status=404)

@csrf_exempt
@require_POST
def add_legend_ajax(request):
    name = request.POST.get("name")
    position = request.POST.get("position")
    age = request.POST.get("age")
    club = request.POST.get("club")
    photo_url = request.POST.get("photo_url")

    new_legend = LegendPlayer(
        name=name,
        position=position,
        age=age,
        club=club,
        photo_url=photo_url,
    )
    new_legend.save()

    return HttpResponse(b"CREATED", status=201)