from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.utils.html import strip_tags
from django.contrib import messages

from .models import Merch
from .forms import MerchForm

#  MAIN MERCH PAGE (List)
@login_required(login_url='/login')
def show_merch(request):
    filter_type = request.GET.get("filter", "all")

    if filter_type == "all":
        merch_list = Merch.objects.all()
    else:
        merch_list = Merch.objects.filter(user=request.user)

    context = {
        'name': request.user.username,
        'merch_list': merch_list,
        'last_login': request.COOKIES.get('last_login', 'Never'),
    }

    return render(request, "merchandise.html", context)

#  CREATE MERCH
def create_merch(request):
    form = MerchForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        merch_entry = form.save(commit=False)
        merch_entry.user = request.user
        merch_entry.save()
        messages.success(request, "Merchandise berhasil ditambahkan.")
        return redirect('merchandise:show_merch')

    context = {'form': form}
    return render(request, "create_merch.html", context)

#  DETAIL MERCH
@login_required(login_url='/login')
def show_merch_detail(request, id):
    merch = get_object_or_404(Merch, pk=id)

    context = {'merch': merch}
    return render(request, "merch_detail.html", context)

#  EDIT MERCH
def edit_merch(request, id):
    merch = get_object_or_404(Merch, pk=id)
    form = MerchForm(request.POST or None, instance=merch)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Merchandise berhasil diperbarui.")
        return redirect('merchandise:show_merch_detail', merch.id)

    context = {'form': form}
    return render(request, "create_merch.html", context)

#  DELETE MERCH
def delete_merch(request, id):
    merch = get_object_or_404(Merch, pk=id)
    merch.delete()
    messages.success(request, "Merchandise berhasil dihapus.")
    return HttpResponseRedirect(reverse('merchandise:show_merch'))

#  AJAX CREATE MERCH
@csrf_exempt
@require_POST
def add_merch_entry_ajax(request):
    name = strip_tags(request.POST.get("name", "")).strip()
    description = strip_tags(request.POST.get("description", "")).strip()
    category = request.POST.get("category", "")
    price = request.POST.get("price", 0)
    thumbnail = request.POST.get("thumbnail", "")
    product_link = request.POST.get("product_link", "")

    if not name or not description or not category:
        return HttpResponse(b"BAD REQUEST", status=400)

    new_merch = Merch(
        name=name,
        description=description,
        category=category,
        price=price,
        thumbnail=thumbnail,
        product_link=product_link,
        user=request.user
    )
    new_merch.save()

    return HttpResponse(b"CREATED", status=201)

#  JSON / XML SERIALIZERS
def show_xml(request):
    merch_list = Merch.objects.all().order_by('-created_at')
    xml_data = serializers.serialize("xml", merch_list)
    return HttpResponse(xml_data, content_type="application/xml; charset=utf-8")

def show_json(request):
    merch_list = Merch.objects.select_related('user').all().order_by('-created_at')
    data = [
        {
            'id': str(merch.id),
            'name': merch.name,
            'description': merch.description,
            'category': merch.category,
            'thumbnail': merch.thumbnail,
            'price': merch.price,
            'product_link': merch.product_link,
            'user_id': merch.user_id,
            'user_username': merch.user.username if merch.user_id else None,
        }
        for merch in merch_list
    ]
    return JsonResponse(data, safe=False)

def show_xml_by_id(request, merch_id):
    merch_item = get_object_or_404(Merch, pk=merch_id)
    xml_data = serializers.serialize("xml", [merch_item])
    return HttpResponse(xml_data, content_type="application/xml; charset=utf-8")

def show_json_by_id(request, id):
    n = get_object_or_404(Merch.objects.select_related('user'), pk=id)
    data = {
        'id': str(n.id),
        'name': n.name,
        'description': n.description,
        'category': n.category,
        'thumbnail': n.thumbnail,
        'price': n.price,
        'product_link': n.product_link,
        'user_id': n.user_id,
        'user_username': n.user.username if n.user_id else None,
    }
    return JsonResponse(data)