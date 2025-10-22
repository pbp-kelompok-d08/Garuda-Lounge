from django.shortcuts import render, get_object_or_404
from .models import LegendPlayer

def show_profile_list(request):
    players = LegendPlayer.objects.all().order_by('name')
    context = {
        'players_list': players,
    }
    return render(request, "profile_list.html", context) 

def show_profile_detail(request, id):
    player = get_object_or_404(LegendPlayer, pk=id) 
    context = {
        'player': player,
    }
    return render(request, "profile_detail.html", context)
