from django.shortcuts import render, redirect, get_object_or_404
from .forms import MerchForm
from .models import Merch
from django.contrib.auth.decorators import login_required


def show_merch(request):
    merch_list = Merch.objects.all()
    context = {
        'merch_list': merch_list,
    }
    return render(request, "merchandise.html", context)


def create_merch(request):
    form = MerchForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_merch.html", context)

def show_merch_detail(request, id):
    merch = get_object_or_404(Merch, pk=id)

    context = {
        'merch': merch
    }

    return render(request, "merch_detail.html", context)