from django.shortcuts import render, redirect, get_object_or_404
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

def show_match_detail(request, id):
    pertandingan = get_object_or_404(Pertandingan, pk=id)

    context = {
        'pertandingan': pertandingan
    }

    return render(request, "match_detail.html", context)