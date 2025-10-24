from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from match.forms import PertandinganForm
from match.models import Pertandingan
import json
import itertools

# Create your views here.
def show_match(request):
    matches = Pertandingan.objects.all()
    form = PertandinganForm()
    context = {
        'pertandingan_list': matches,
        'form':form,
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

    starters_paired = list(itertools.zip_longest(
    starters_tuan_rumah_list, 
    starters_tamu_list, 
    fillvalue=''
    ))

    # Pasangkan list pengganti
    pengganti_paired = list(itertools.zip_longest(
        pengganti_tuan_rumah_list, 
        pengganti_tamu_list, 
        fillvalue=''
    ))
    
    context = {
        'pertandingan': pertandingan,
        'pencetak_gol_tuan_rumah': pencetak_gol_tuan_rumah_list,
        'pencetak_gol_tamu': pencetak_gol_tamu_list,
        'starters_paired': starters_paired,
        'pengganti_paired': pengganti_paired,
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

def show_match_json(request):
    pertandingan_list = Pertandingan.objects.all()
    data = [
        { # sebernya yang perlu cuma yang tampil di match.html aja kayak nama tim, jeni pertandingan, bender, skor, highlight
            'id': str(p.id),
            'jenis_pertandingan': str(p.jenis_pertandingan),
            'tim_tuan_rumah': str(p.tim_tuan_rumah),
            'tim_tamu': str(p.tim_tamu),
            'bendera_tuan_rumah': str(p.bendera_tuan_rumah),
            'bendera_tamu': str(p.bendera_tamu),
            'tanggal': str(p.tanggal),
            'stadion': str(p.stadion),
            'skor_tuan_rumah': str(p.skor_tuan_rumah),
            'skor_tamu': str(p.skor_tamu),
            'pencetak_gol_tuan_rumah': str(p.pencetak_gol_tuan_rumah),
            'pencetak_gol_tamu': str(p.pencetak_gol_tamu),
            'starter_tuan_rumah': str(p.starter_tuan_rumah),
            'starter_tamu': str(p.starter_tamu),
            'pengganti_tuan_rumah': str(p.pengganti_tuan_rumah),
            'pengganti_tamu': str(p.pengganti_tamu),
            'manajer_tuan_rumah': str(p.manajer_tuan_rumah),
            'manajer_tamu': str(p.manajer_tamu),
            'highlight': str(p.highlight),
            'penguasaan_bola_tuan_rumah': str(p.penguasaan_bola_tuan_rumah),
            'penguasaan_bola_tamu': str(p.penguasaan_bola_tamu),
            'tembakan_tuan_rumah': str(p.tembakan_tuan_rumah),
            'tembakan_tamu': str(p.tembakan_tamu),
            'on_target_tuan_rumah': str(p.on_target_tuan_rumah),
            'on_target_tamu': str(p.on_target_tamu),
            'akurasi_umpan_tuan_rumah': str(p.akurasi_umpan_tuan_rumah),
            'akurasi_umpan_tamu': str(p.akurasi_umpan_tamu),
            'pelanggaran_tuan_rumah': str(p.pelanggaran_tuan_rumah),
            'pelanggaran_tamu': str(p.pelanggaran_tamu),
            'kartu_kuning_tuan_rumah': str(p.kartu_kuning_tuan_rumah),
            'kartu_kuning_tamu': str(p.kartu_kuning_tamu),
            'kartu_merah_tuan_rumah': str(p.kartu_merah_tuan_rumah),
            'kartu_merah_tamu': str(p.kartu_merah_tamu),
            'offside_tuan_rumah': str(p.offside_tuan_rumah),
            'offside_tamu': str(p.offside_tamu),
            'corner_tuan_rumah': str(p.corner_tuan_rumah),
            'corner_tamu': str(p.corner_tamu),   
        }
        for p in pertandingan_list
    ]

    return JsonResponse(data, safe=False)

@require_POST # Memastikan view ini hanya menerima request POST
def add_match_ajax(request):
    """
    Menangani pembuatan Pertandingan baru via AJAX dari modal.
    """
    # request.POST akan berisi data dari FormData
    form = PertandinganForm(request.POST) 

    if form.is_valid():
        # Jika data valid, simpan objek baru ke database
        form.save()
        
        # Kirim balasan sukses
        return JsonResponse({'status': 'success', 'message': 'Match added successfully!'})
    else:
        # Jika form tidak valid, kirim kembali daftar error
        # status=400 memberi tahu browser bahwa ini adalah bad request
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
def show_json_by_id(request, match_id):
    try:
        p = Pertandingan.objects.select_related('user').get(pk=match_id)
        data = {
           'id': str(p.id),
            'jenis_pertandingan': str(p.jenis_pertandingan),
            'tim_tuan_rumah': str(p.tim_tuan_rumah),
            'tim_tamu': str(p.tim_tamu),
            'bendera_tuan_rumah': str(p.bendera_tuan_rumah),
            'bendera_tamu': str(p.bendera_tamu),
            'tanggal': str(p.tanggal),
            'stadion': str(p.stadion),
            'skor_tuan_rumah': str(p.skor_tuan_rumah),
            'skor_tamu': str(p.skor_tamu),
            'pencetak_gol_tuan_rumah': str(p.pencetak_gol_tuan_rumah),
            'pencetak_gol_tamu': str(p.pencetak_gol_tamu),
            'starter_tuan_rumah': str(p.starter_tuan_rumah),
            'starter_tamu': str(p.starter_tamu),
            'pengganti_tuan_rumah': str(p.pengganti_tuan_rumah),
            'pengganti_tamu': str(p.pengganti_tamu),
            'manajer_tuan_rumah': str(p.manajer_tuan_rumah),
            'manajer_tamu': str(p.manajer_tamu),
            'highlight': str(p.highlight),
            'penguasaan_bola_tuan_rumah': str(p.penguasaan_bola_tuan_rumah),
            'penguasaan_bola_tamu': str(p.penguasaan_bola_tamu),
            'tembakan_tuan_rumah': str(p.tembakan_tuan_rumah),
            'tembakan_tamu': str(p.tembakan_tamu),
            'on_target_tuan_rumah': str(p.on_target_tuan_rumah),
            'on_target_tamu': str(p.on_target_tamu),
            'akurasi_umpan_tuan_rumah': str(p.akurasi_umpan_tuan_rumah),
            'akurasi_umpan_tamu': str(p.akurasi_umpan_tamu),
            'pelanggaran_tuan_rumah': str(p.pelanggaran_tuan_rumah),
            'pelanggaran_tamu': str(p.pelanggaran_tamu),
            'kartu_kuning_tuan_rumah': str(p.kartu_kuning_tuan_rumah),
            'kartu_kuning_tamu': str(p.kartu_kuning_tamu),
            'kartu_merah_tuan_rumah': str(p.kartu_merah_tuan_rumah),
            'kartu_merah_tamu': str(p.kartu_merah_tamu),
            'offside_tuan_rumah': str(p.offside_tuan_rumah),
            'offside_tamu': str(p.offside_tamu),
            'corner_tuan_rumah': str(p.corner_tuan_rumah),
            'corner_tamu': str(p.corner_tamu),   
        }
        return JsonResponse(data)
    except Pertandingan.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)