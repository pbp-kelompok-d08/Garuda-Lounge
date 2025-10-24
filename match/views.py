from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from match.forms import PertandinganForm
from match.models import Pertandingan

# Create your views here.
def show_match(request):
    matches = Pertandingan.objects.all()
    context = {
        'pertandingan_list': matches # <-- BENAR! Namanya cocok.
    }
    return render(request, "match.html", context)

def add_match(request):
    form = PertandinganForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('match:show_match')

    context = {'form': form}
    return render(request, "add_match.html", context)

def show_match_details(request, id):
    pertandingan = get_object_or_404(Pertandingan, pk=id)

    # Field yang text nya dipisahkan oleh titik koma, kita split dulu sebelum di-render biar nampilinnya rapih
    pencetak_gol_tuan_rumah_list = pertandingan.pencetak_gol_tuan_rumah.split(';')
    pencetak_gol_tamu_list = pertandingan.pencetak_gol_tamu.split(';')

    starters_tuan_rumah_list = pertandingan.starter_tuan_rumah.split(';')
    starters_tamu_list = pertandingan.starter_tamu.split(';')

    pengganti_tuan_rumah_list = pertandingan.pengganti_tuan_rumah.split(';')
    pengganti_tamu_list = pertandingan.pengganti_tamu.split(';')
    
    context = {
        'pertandingan': pertandingan,
        'pencetak_gol_tuan_rumah_list': pencetak_gol_tuan_rumah_list,
        'pencetak_gol_tamu_list': pencetak_gol_tamu_list,
        'starters_tuan_rumah': starters_tuan_rumah_list,
        'starters_tamu': starters_tamu_list,
        'pengganti_tuan_rumah': pengganti_tuan_rumah_list,
        'pengganti_tamu': pengganti_tamu_list,
    }
    return render(request, 'match_details.html', context)

def edit_match(request, id):
    pertandingan = get_object_or_404(Pertandingan, pk=id)
    form = PertandinganForm(request.POST or None, instance=pertandingan)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('match:show_match')

    context = {
        'form': form
    }

    return render(request, "edit_match.html", context)

def delete_match(request, id):
    pertandingan = get_object_or_404(Pertandingan, pk=id)
    pertandingan.delete()
    return HttpResponseRedirect(reverse('match:show_match'))