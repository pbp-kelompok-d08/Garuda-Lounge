from django.shortcuts import render, get_object_or_404
from .models import PlayerProfile

def show_profile_list(request):
    players = PlayerProfile.objects.all().order_by('name')
    context = {
        'players_list': players,
    }
    return render(request, "profile_list.html", context) 

def show_profile_detail(request, id):
    player = get_object_or_404(PlayerProfile, pk=id) 
    context = {
        'player': player,
    }
    return render(request, "profile_detail.html", context)