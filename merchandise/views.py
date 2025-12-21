from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
import json

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

@login_required(login_url='/login')
def show_merch_detail(request, id):
    merch = get_object_or_404(Merch, pk=id)
    return render(request, "merch_detail.html", {"merch": merch})


#  CREATE MERCH
@login_required(login_url='/login')
def create_merch(request):
    form = MerchForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        merch_entry = form.save(commit=False)
        merch_entry.user = request.user
        merch_entry.save()
        messages.success(request, "Merchandise berhasil ditambahkan.")
        return redirect('merchandise:show_merch')

    context = {'form': form,
               'action_url': reverse('merchandise:create_merch'),
                'page_title': 'Tambah Merchandise Baru',
                'submit_label': 'Publish Merch'}
    return render(request, "create_merch.html", context)

#  EDIT MERCH
@login_required(login_url='/login')
def edit_merch(request, id):
    merch = get_object_or_404(Merch, pk=id)
    form = MerchForm(request.POST or None, instance=merch)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Merchandise berhasil diperbarui.")
        return redirect('merchandise:show_merch_detail', merch.id)

    context = {'form': form,
                'action_url': reverse('merchandise:edit_merch', args=[merch.id]),
                'page_title': 'Edit Merchandise',
                'page_subtitle': 'Update your merchandise',
                'submit_label': 'Update Merch'}
    return render(request, "create_merch.html", context)

#  DELETE MERCH
@require_POST
@login_required(login_url='/login')
def delete_merch(request, id):
     # 1) cek ada/tidak
    try:
        n = Merch.objects.get(pk=id)
    except Merch.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    # 2) cek kepemilikan
    if n.user_id != request.user.id:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    # 3) hapus
    n.delete()
    return JsonResponse({'ok': True})

#  AJAX CREATE MERCH
@login_required(login_url='/login')
@require_POST
def add_merch_entry_ajax(request):
    name = strip_tags(request.POST.get("name", "")).strip()
    description = strip_tags(request.POST.get("description", "")).strip()
    category = request.POST.get("category", "")
    price = request.POST.get("price", "")
    thumbnail = request.POST.get("thumbnail", "")
    product_link = request.POST.get("product_link", "")

    if not name or not description or not category or not price or not thumbnail or not product_link:
        return JsonResponse({"error": "semua field wajib diisi"}, status=400)

    new_merch = Merch.objects.create(
        name=name,
        description=description,
        category=category,
        price=price,
        thumbnail=thumbnail,
        product_link=product_link,
        user=request.user
    )
    data={
        'id': str(new_merch.id),
        'name': new_merch.name,
        'description': new_merch.description,
        'category': new_merch.category,
        'thumbnail': new_merch.thumbnail,
        'product_link': new_merch.product_link
    }

    return JsonResponse(data, status=201)

#  JSON / XML SERIALIZERS
def show_xml(request):
    merch_list = Merch.objects.all()
    xml_data = serializers.serialize("xml", merch_list)
    return HttpResponse(xml_data, content_type="application/xml; charset=utf-8")

def show_json(request):
    merch_list = Merch.objects.select_related('user').all()
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

@csrf_exempt
def create_merch_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = strip_tags(data.get("name", ""))  # Strip HTML tags
        description = strip_tags(data.get("description", ""))  # Strip HTML tags
        category = data.get("category", "")
        price = data.get("price", "")
        thumbnail = data.get("thumbnail", "")
        product_link = data.get("product_link", "")
        user = request.user
        
        new_merch = Merch(
            name=name, 
            description=description,
            category=category,
            price=price,
            thumbnail=thumbnail,
            product_link=product_link,
            user=user
        )
        new_merch.save()
        
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def edit_merch_flutter(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            merch = Merch.objects.get(pk=id)
            merch.name = strip_tags(data.get("name", ""))  # Strip HTML tags
            merch.description = strip_tags(data.get("description", ""))  # Strip HTML tags
            merch.category = data.get("category", "")
            merch.price = data.get("price", "")
            merch.thumbnail = data.get("thumbnail", "")
            merch.product_link = data.get("product_link", "")

            merch.save()
        
            return JsonResponse({"status": "success"}, status=200)
        except Merch.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Not found"}, status=404)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def delete_merch_flutter(request, id):
    if request.method == 'POST':
        try:
            match = Merch.objects.get(pk=id)
            match.delete()
            return JsonResponse({"status": "success"}, status=200)
        except Merch.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Match not found"}, status=404)
    return JsonResponse({"status": "error"}, status=401)