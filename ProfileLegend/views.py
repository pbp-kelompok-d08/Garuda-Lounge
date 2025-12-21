import uuid, json, requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core import serializers
from .models import LegendPlayer
from .forms import LegendPlayerForm 
from django.urls import reverse
from django.utils.html import strip_tags
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
    player = None
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
    user = request.user

    new_legend = LegendPlayer(
        name=name,
        position=position,
        age=age,
        club=club,
        photo_url=photo_url,
        user=user
    )
    new_legend.save()

    return HttpResponse(b"CREATED", status=201)

@login_required(login_url='/login')
def edit_legend(request, id):
    legend = get_object_or_404(LegendPlayer, pk=id)

    if request.method == "POST":
        form = LegendPlayerForm(request.POST, instance=legend)
        if form.is_valid():
            legend = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'player_id': str(legend.id),})
            return redirect('ProfileLegend:show_profile_legend')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': dict(form.errors),}, status=400)
    
    form = LegendPlayerForm(instance=legend)
    context = {'form': form, 'legend': legend}
    return render(request, "edit_legend.html", context)

@login_required(login_url='/login')
def delete_legend(request, id):
    legend = get_object_or_404(LegendPlayer, pk=id)
    legend.delete()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return HttpResponseRedirect(reverse('ProfileLegend:show_profile_legend'))

def proxyimage(request):
    image_url = request.GET.get('url')
    if not image_url:return HttpResponse('No URL provided', status=400)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
            "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        }
        response = requests.get(image_url, headers=headers, timeout=10, stream=True)
        response.raise_for_status()
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg'),
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)

#flutter
@csrf_exempt
def create_legend_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        name= strip_tags(data.get("name", ""))
        position= data.get("position", "")
        club= strip_tags(data.get("club", ""))
        age= int(data.get("age", 0))
        photo_url= data.get("photo_url", "")
        is_legend= True 

        new_legend = LegendPlayer.objects.create(
            name=name,
            position=position,
            club=club,
            age=age,
            photo_url=photo_url,
            is_legend=is_legend,
        )
        new_legend.save()
        return JsonResponse({"status": "success"}, status=200)
    return JsonResponse({"status": "error"}, status=401)


@csrf_exempt
@require_POST
def delete_legend_flutter(request, id):
    try:
        legend = LegendPlayer.objects.get(pk=id)
        legend.delete()
        return JsonResponse({"status": "success"}, status=200)
    except LegendPlayer.DoesNotExist:
        return JsonResponse({"status": "not_found"}, status=404)

@csrf_exempt
def edit_legend_flutter(request, id):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid"}, status=405)
    try:
        legend = LegendPlayer.objects.get(pk=id)
        data = json.loads(request.body)

        legend.name = strip_tags(data.get("name", legend.name))
        legend.position = data.get("position", legend.position)
        legend.club = strip_tags(data.get("club", legend.club))
        legend.age = int(data.get("age", legend.age))
        legend.photo_url = data.get("photo_url", legend.photo_url)
        legend.save()

        return JsonResponse({
            "status": "success",
            "player_id": str(legend.id)
        })

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)