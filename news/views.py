from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.utils.html import strip_tags
from django.contrib import messages

from .models import News
from .forms import NewsForm

import datetime

#  MAIN NEWS PAGE (List)
@login_required(login_url='/login')
def show_news_main(request):
    filter_type = request.GET.get("filter", "all")

    if filter_type == "all":
        news_list = News.objects.all().order_by('-created_at')
    else:
        news_list = News.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'name': request.user.username,
        'news_list': news_list,
        'last_login': request.COOKIES.get('last_login', 'Never'),
    }

    return render(request, "news.html", context)

#  CREATE NEWS
@login_required(login_url='/login')
def create_news(request):
    form = NewsForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        news_entry = form.save(commit=False)
        news_entry.user = request.user
        news_entry.save()
        messages.success(request, "Berita berhasil dibuat.")
        return redirect('news:show_news_main')# Kembali ke halaman utama (main)

    context = {'form': form}
    return render(request, "create_news.html", context)

#  DETAIL NEWS
@login_required(login_url='/login')
def show_news_detail(request, id):
    news = get_object_or_404(News, pk=id)
    news.increment_views()

    context = {'news': news}
    return render(request, "news_detail.html", context)

#  EDIT NEWS
@login_required(login_url='/login')
def edit_news(request, id):
    news = get_object_or_404(News, pk=id)
    form = NewsForm(request.POST or None, instance=news)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Berita berhasil diperbarui.")
        return redirect('news:show_news_detail', news.id)

    context = {'form': form}
    return render(request, "create_news.html", context)

#  DELETE NEWS
@login_required(login_url='/login')
def delete_news(request, id):
    news = get_object_or_404(News, pk=id)
    news.delete()
    messages.success(request, "Berita berhasil dihapus.")
    return HttpResponseRedirect(reverse('news:show_news_main'))

#  AJAX CREATE NEWS
@csrf_exempt
@require_POST
@login_required(login_url='/login')
def add_news_entry_ajax(request):
    title = strip_tags(request.POST.get("title", "")).strip()
    content = strip_tags(request.POST.get("content", "")).strip()
    category = request.POST.get("category", "")
    thumbnail = request.POST.get("thumbnail", "")
    is_featured = request.POST.get("is_featured") == 'on'

    if not title or not content or not category:
        return HttpResponse(b"BAD REQUEST", status=400)

    new_news = News(
        title=title,
        content=content,
        category=category,
        thumbnail=thumbnail,
        is_featured=is_featured,
        user=request.user
    )
    new_news.save()

    return HttpResponse(b"CREATED", status=201)

#  JSON / XML SERIALIZERS
@require_GET
def show_xml(request):
    news_list = News.objects.all().order_by('-created_at')
    xml_data = serializers.serialize("xml", news_list)
    return HttpResponse(xml_data, content_type="application/xml; charset=utf-8")

@require_GET
def show_json(request):
    news_list = News.objects.select_related('user').all().order_by('-created_at')
    data = [
        {
            'id': str(news.id),
            'title': news.title,
            'content': news.content,
            'category': news.category,
            'thumbnail': news.thumbnail,
            'news_views': news.news_views,
            'created_at': news.created_at.isoformat() if news.created_at else None,
            'is_featured': news.is_featured,
            'user_id': news.user_id,
            'user_username': news.user.username if news.user_id else None,
        }
        for news in news_list
    ]
    return JsonResponse(data, safe=False)

@require_GET
def show_xml_by_id(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    xml_data = serializers.serialize("xml", [news_item])
    return HttpResponse(xml_data, content_type="application/xml; charset=utf-8")

@require_GET
def show_json_by_id(request, id):
    n = get_object_or_404(News.objects.select_related('user'), pk=id)
    data = {
        'id': str(n.id),
        'title': n.title,
        'content': n.content,
        'category': n.category,
        'thumbnail': n.thumbnail,
        'news_views': n.news_views,
        'created_at': n.created_at.isoformat() if n.created_at else None,
        'is_featured': n.is_featured,
        'user_id': n.user_id,
        'user_username': n.user.username if n.user_id else None,
    }
    return JsonResponse(data)

