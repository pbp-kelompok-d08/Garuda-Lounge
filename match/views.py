from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from match.forms import PertandinganForm
from match.models import Pertandingan
import json
import itertools
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags

# Create your views here.
def show_match(request):
    matches = Pertandingan.objects.all()
    form = PertandinganForm()
    context = {
        'pertandingan_list': matches,
        'form':form,
    }
    return render(request, "match.html", context)

# Diganti karena sudah ada yang pakai ajax
# def add_match(request):
#     form = PertandinganForm(request.POST or None)

#     if form.is_valid() and request.method == "POST":
#         form.save()
#         return redirect('match:show_match')

#     context = {'form': form}
#     return render(request, "add_match.html", context)

def show_match_details(request, id):
    pertandingan = get_object_or_404(Pertandingan, pk=id)

    pencetak_gol_tuan_rumah_list = pertandingan.pencetak_gol_tuan_rumah
    pencetak_gol_tamu_list = pertandingan.pencetak_gol_tamu

    starters_tuan_rumah_list = pertandingan.starter_tuan_rumah
    starters_tamu_list = pertandingan.starter_tamu

    pengganti_tuan_rumah_list = pertandingan.pengganti_tuan_rumah
    pengganti_tamu_list = pertandingan.pengganti_tamu

    context = {
        'pertandingan': pertandingan,
    }
    
    # Field yang text nya dipisahkan oleh titik koma, kita split dulu sebelum di-render biar nampilinnya rapih
    if (pencetak_gol_tuan_rumah_list != None): 
        pencetak_gol_tuan_rumah_list = pencetak_gol_tuan_rumah_list.split(';')
        context['pencetak_gol_tuan_rumah'] = pencetak_gol_tuan_rumah_list
        
    if (pencetak_gol_tamu_list != None): 
        pencetak_gol_tamu_list = pencetak_gol_tamu_list.split(';')
        context['pencetak_gol_tamu'] = pencetak_gol_tamu_list

    if (starters_tuan_rumah_list != None): 
        starters_tuan_rumah_list = starters_tuan_rumah_list.split(';')
        context['starters_tuan_rumah'] = starters_tuan_rumah_list
    
    if (starters_tamu_list != None):
        starters_tamu_list = starters_tamu_list.split(';')
        context['starters_tamu'] = starters_tamu_list

    if (pengganti_tuan_rumah_list != None):
        pengganti_tuan_rumah_list = pengganti_tuan_rumah_list.split(';')
        context['pengganti_tuan_rumah'] = pengganti_tuan_rumah_list
    
    if (pengganti_tamu_list != None):
        pengganti_tamu_list = pengganti_tamu_list.split(';')
        context['pengganti_tamu'] = pengganti_tamu_list

    if (starters_tuan_rumah_list != None) & (starters_tamu_list != None):
        starters_paired = list(itertools.zip_longest(
        starters_tuan_rumah_list, 
        starters_tamu_list, 
        fillvalue=''
        ))
        context['starters_paired'] = starters_paired

    if (pengganti_tuan_rumah_list != None) & (pengganti_tamu_list != None):
        # Pasangkan list pengganti
        pengganti_paired = list(itertools.zip_longest(
            pengganti_tuan_rumah_list, 
            pengganti_tamu_list, 
            fillvalue=''
        ))
        context['pengganti_paired'] = pengganti_paired
    
    
    return render(request, 'match_details.html', context)

# Diganti karena sudah pakai yang versi ajax
# def edit_match(request, id):
#     pertandingan = get_object_or_404(Pertandingan, pk=id)
#     form = PertandinganForm(request.POST or None, instance=pertandingan)
#     if form.is_valid() and request.method == 'POST':
#         form.save()
#         return redirect('match:show_match')

#     context = {
#         'form': form
#     }

#     return render(request, "edit_match.html", context)

def delete_match(request, id):
    pertandingan = get_object_or_404(Pertandingan, pk=id)
    pertandingan.delete()
    return HttpResponseRedirect(reverse('match:show_match'))

def show_match_json(request):
    pertandingan_list = Pertandingan.objects.all().order_by('-tanggal')
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
    
# def show_json_by_id(request, match_id):
#     try:
#         p = Pertandingan.objects.select_related('user').get(pk=match_id)
#         data = {
#            'id': str(p.id),
#             'jenis_pertandingan': str(p.jenis_pertandingan),
#             'tim_tuan_rumah': str(p.tim_tuan_rumah),
#             'tim_tamu': str(p.tim_tamu),
#             'bendera_tuan_rumah': str(p.bendera_tuan_rumah),
#             'bendera_tamu': str(p.bendera_tamu),
#             'tanggal': str(p.tanggal),
#             'stadion': str(p.stadion),
#             'skor_tuan_rumah': str(p.skor_tuan_rumah),
#             'skor_tamu': str(p.skor_tamu),
#             'pencetak_gol_tuan_rumah': str(p.pencetak_gol_tuan_rumah),
#             'pencetak_gol_tamu': str(p.pencetak_gol_tamu),
#             'starter_tuan_rumah': str(p.starter_tuan_rumah),
#             'starter_tamu': str(p.starter_tamu),
#             'pengganti_tuan_rumah': str(p.pengganti_tuan_rumah),
#             'pengganti_tamu': str(p.pengganti_tamu),
#             'manajer_tuan_rumah': str(p.manajer_tuan_rumah),
#             'manajer_tamu': str(p.manajer_tamu),
#             'highlight': str(p.highlight),
#             'penguasaan_bola_tuan_rumah': str(p.penguasaan_bola_tuan_rumah),
#             'penguasaan_bola_tamu': str(p.penguasaan_bola_tamu),
#             'tembakan_tuan_rumah': str(p.tembakan_tuan_rumah),
#             'tembakan_tamu': str(p.tembakan_tamu),
#             'on_target_tuan_rumah': str(p.on_target_tuan_rumah),
#             'on_target_tamu': str(p.on_target_tamu),
#             'akurasi_umpan_tuan_rumah': str(p.akurasi_umpan_tuan_rumah),
#             'akurasi_umpan_tamu': str(p.akurasi_umpan_tamu),
#             'pelanggaran_tuan_rumah': str(p.pelanggaran_tuan_rumah),
#             'pelanggaran_tamu': str(p.pelanggaran_tamu),
#             'kartu_kuning_tuan_rumah': str(p.kartu_kuning_tuan_rumah),
#             'kartu_kuning_tamu': str(p.kartu_kuning_tamu),
#             'kartu_merah_tuan_rumah': str(p.kartu_merah_tuan_rumah),
#             'kartu_merah_tamu': str(p.kartu_merah_tamu),
#             'offside_tuan_rumah': str(p.offside_tuan_rumah),
#             'offside_tamu': str(p.offside_tamu),
#             'corner_tuan_rumah': str(p.corner_tuan_rumah),
#             'corner_tamu': str(p.corner_tamu),   
#         }
#         return JsonResponse(data)
#     except Pertandingan.DoesNotExist:
#         return JsonResponse({'detail': 'Not found'}, status=404)


@require_POST # Memastikan view ini hanya menerima request POST
def add_match_ajax(request):
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
    
# Ambil data dari match yang udah ada untuk dibuatkan form edit nya
def get_edit_form_html(request, id):
    pertandingan = get_object_or_404(Pertandingan, pk=id)
    form = PertandinganForm(instance=pertandingan) # Ambil form berisi data pertandingan
    
    # Render html form nya
    html = render_to_string('form.html', {'form': form}, request=request)
    
    return JsonResponse({'html': html})

@require_POST # Memastikan view ini hanya menerima request POST
def edit_match_ajax(request, id):
    pertandingan = get_object_or_404(Pertandingan, pk=id)
    
    # Validasi data yang masuk dengan instance yang ada
    form = PertandinganForm(request.POST, instance=pertandingan) 
    
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success', 'message': 'Match updated!'})
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
@csrf_exempt
def create_match_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        jenis_pertandingan = data.get("jenis_pertandingan", "")
        tim_tuan_rumah = strip_tags(data.get("tim_tuan_rumah", "")) # Strip HTML tags
        tim_tamu =  strip_tags(data.get("tim_tamu", "")) # Strip HTML tags
        bendera_tuan_rumah = data.get("bendera_tuan_rumah", "")
        bendera_tamu = data.get("bendera_tamu", "")
        tanggal = data.get("tanggal", "")
        stadion = data.get("stadion", "")
        skor_tuan_rumah = data.get("skor_tuan_rumah", "")
        skor_tamu = data.get("skor_tamu", "")
        pencetak_gol_tuan_rumah = data.get("pencetak_gol_tuan_rumah", "")
        pencetak_gol_tamu = data.get("pencetak_gol_tamu", "")
        starter_tuan_rumah = data.get("starter_tuan_rumah", "")
        starter_tamu = data.get("starter_tamu", "")
        pengganti_tuan_rumah = data.get("pengganti_tuan_rumah", "")
        pengganti_tamu = data.get("pengganti_tamu", "")
        manajer_tuan_rumah = data.get("manajer_tuan_rumah", "")
        manajer_tamu = data.get("manajer_tamu", "")
        highlight = data.get("highlight", "")
        penguasaan_bola_tuan_rumah = data.get("penguasaan_bola_tuan_rumah", "")
        penguasaan_bola_tamu = data.get("penguasaan_bola_tamu", "")
        tembakan_tuan_rumah = data.get("tembakan_tuan_rumah", "")
        tembakan_tamu = data.get("tembakan_tamu", "")
        on_target_tuan_rumah = data.get("on_target_tuan_rumah", "")
        on_target_tamu = data.get("on_target_tamu", "")
        akurasi_umpan_tuan_rumah = data.get("akurasi_umpan_tuan_rumah", "")
        akurasi_umpan_tamu = data.get("akurasi_umpan_tamu", "")
        pelanggaran_tuan_rumah = data.get("pelanggaran_tuan_rumah", "")
        pelanggaran_tamu = data.get("pelanggaran_tamu", "")
        kartu_kuning_tuan_rumah = data.get("kartu_kuning_tuan_rumah", "")
        kartu_kuning_tamu = data.get("kartu_kuning_tamu", "")
        kartu_merah_tuan_rumah = data.get("kartu_merah_tuan_rumah", "")
        kartu_merah_tamu = data.get("kartu_merah_tamu", "")
        offside_tuan_rumah = data.get("offside_tuan_rumah", "")
        offside_tamu = data.get("offside_tamu", "")
        corner_tuan_rumah = data.get("corner_tuan_rumah", "")
        corner_tamu = data.get("corner_tamu", "")
        # user = request.user
        
        new_match = Pertandingan(
            jenis_pertandingan=jenis_pertandingan, 
            tim_tuan_rumah=tim_tuan_rumah,
            tim_tamu=tim_tamu,
            bendera_tuan_rumah=bendera_tuan_rumah,
            bendera_tamu=bendera_tamu,
            tanggal=tanggal,
            stadion=stadion,
            skor_tuan_rumah=skor_tuan_rumah,
            skor_tamu=skor_tamu,
            pencetak_gol_tuan_rumah=pencetak_gol_tuan_rumah,
            pencetak_gol_tamu=pencetak_gol_tamu,
            starter_tuan_rumah=starter_tuan_rumah,
            starter_tamu=starter_tamu,
            pengganti_tuan_rumah=pengganti_tuan_rumah,
            pengganti_tamu=pengganti_tamu,
            manajer_tuan_rumah=manajer_tuan_rumah,
            manajer_tamu=manajer_tamu,
            highlight=highlight,
            penguasaan_bola_tuan_rumah=penguasaan_bola_tuan_rumah,
            penguasaan_bola_tamu=penguasaan_bola_tamu,
            tembakan_tuan_rumah=tembakan_tuan_rumah,
            tembakan_tamu=tembakan_tamu,
            on_target_tuan_rumah=on_target_tuan_rumah,
            on_target_tamu=on_target_tamu,
            akurasi_umpan_tuan_rumah=akurasi_umpan_tuan_rumah,
            akurasi_umpan_tamu=akurasi_umpan_tamu,
            pelanggaran_tuan_rumah=pelanggaran_tuan_rumah,
            pelanggaran_tamu=pelanggaran_tamu,
            kartu_kuning_tuan_rumah=kartu_kuning_tuan_rumah,
            kartu_kuning_tamu=kartu_kuning_tamu,
            kartu_merah_tuan_rumah=kartu_merah_tuan_rumah,
            kartu_merah_tamu=kartu_merah_tamu,
            offside_tuan_rumah=offside_tuan_rumah,
            offside_tamu=offside_tamu,
            corner_tuan_rumah=corner_tuan_rumah,
            corner_tamu=corner_tamu,
            # user=user
        )
        new_match.save()
        
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def edit_match_flutter(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            # cari match berdasarkan id
            match = Pertandingan.objects.get(pk=id)
            
            # update data (mirip seperti create, tapi ke objek yang sudah ada)
            match.jenis_pertandingan = data.get("jenis_pertandingan")
            match.tim_tuan_rumah = data.get("tim_tuan_rumah")
            match.tim_tamu =  strip_tags(data.get("tim_tamu", "")) # Strip HTML tags
            match.bendera_tuan_rumah = data.get("bendera_tuan_rumah", "")
            match.bendera_tamu = data.get("bendera_tamu", "")
            match.tanggal = data.get("tanggal", "")
            match.stadion = data.get("stadion", "")
            match.skor_tuan_rumah = data.get("skor_tuan_rumah", "")
            match.skor_tamu = data.get("skor_tamu", "")
            match.pencetak_gol_tuan_rumah = data.get("pencetak_gol_tuan_rumah", "")
            match.pencetak_gol_tamu = data.get("pencetak_gol_tamu", "")
            match.starter_tuan_rumah = data.get("starter_tuan_rumah", "")
            match.starter_tamu = data.get("starter_tamu", "")
            match.pengganti_tuan_rumah = data.get("pengganti_tuan_rumah", "")
            match.pengganti_tamu = data.get("pengganti_tamu", "")
            match.manajer_tuan_rumah = data.get("manajer_tuan_rumah", "")
            match.manajer_tamu = data.get("manajer_tamu", "")
            match.highlight = data.get("highlight", "")
            match.penguasaan_bola_tuan_rumah = data.get("penguasaan_bola_tuan_rumah", "")
            match.penguasaan_bola_tamu = data.get("penguasaan_bola_tamu", "")
            match.tembakan_tuan_rumah = data.get("tembakan_tuan_rumah", "")
            match.tembakan_tamu = data.get("tembakan_tamu", "")
            match.on_target_tuan_rumah = data.get("on_target_tuan_rumah", "")
            match.on_target_tamu = data.get("on_target_tamu", "")
            match.akurasi_umpan_tuan_rumah = data.get("akurasi_umpan_tuan_rumah", "")
            match.akurasi_umpan_tamu = data.get("akurasi_umpan_tamu", "")
            match.pelanggaran_tuan_rumah = data.get("pelanggaran_tuan_rumah", "")
            match.pelanggaran_tamu = data.get("pelanggaran_tamu", "")
            match.kartu_kuning_tuan_rumah = data.get("kartu_kuning_tuan_rumah", "")
            match.kartu_kuning_tamu = data.get("kartu_kuning_tamu", "")
            match.kartu_merah_tuan_rumah = data.get("kartu_merah_tuan_rumah", "")
            match.kartu_merah_tamu = data.get("kartu_merah_tamu", "")
            match.offside_tuan_rumah = data.get("offside_tuan_rumah", "")
            match.offside_tamu = data.get("offside_tamu", "")
            match.corner_tuan_rumah = data.get("corner_tuan_rumah", "")
            match.corner_tamu = data.get("corner_tamu", "")
            
            match.save()
            return JsonResponse({"status": "success"}, status=200)
        except Pertandingan.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Not found"}, status=404)
    return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def delete_match_flutter(request, id):
    if request.method == 'POST':
        try:
            match = Pertandingan.objects.get(pk=id)
            match.delete()
            return JsonResponse({"status": "success"}, status=200)
        except Pertandingan.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Match not found"}, status=404)
    return JsonResponse({"status": "error"}, status=401)