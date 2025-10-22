from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.serializers import serialize
from .models import LegendPlayer
import json

def legend_list(request):
    """Display all legend players"""
    position_filter = request.GET.get('position', '')
    
    players = LegendPlayer.objects.all()
    if position_filter:
        players = players.filter(position=position_filter)
    
    positions = LegendPlayer.objects.values_list('position', flat=True).distinct()
    
    context = {
        'players': players,
        'positions': positions,
        'selected_position': position_filter,
    }
    return render(request, 'ProfileLegend/legend_list.html', context)

def legend_detail(request, id):
    """Display single legend player detail"""
    player = get_object_or_404(LegendPlayer, id=id)
    context = {
        'player': player,
    }
    return render(request, 'ProfileLegend/legend_detail.html', context)

def legend_list_json(request):
    """Return all legend players as JSON"""
    position_filter = request.GET.get('position', '')
    
    players = LegendPlayer.objects.all()
    if position_filter:
        players = players.filter(position=position_filter)
    
    data = serialize('json', players)
    return JsonResponse(json.loads(data), safe=False)

def legend_detail_json(request, id):
    """Return single legend player as JSON"""
    player = get_object_or_404(LegendPlayer, id=id)
    data = serialize('json', [player])
    return JsonResponse(json.loads(data)[0], safe=False)