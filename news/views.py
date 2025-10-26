from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
<<<<<<< HEAD

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

=======
from django.views.decorators.http import require_POST, require_GET
from django.utils.html import strip_tags
from django.contrib import messages
from django.utils import timezone
from .models import News, Comment
from .forms import NewsForm, CommentForm
import json

# Halaman Publik/List 
@login_required(login_url='/login')
def show_news_main(request):
    filter_type = request.GET.get("filter", "all")
>>>>>>> origin/feat/news
    if filter_type == "all":
        news_list = News.objects.all().order_by('-created_at')
    else:
        news_list = News.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'name': request.user.username,
        'news_list': news_list,
        'last_login': request.COOKIES.get('last_login', 'Never'),
    }
<<<<<<< HEAD

    return render(request, "news.html", context)

#  CREATE NEWS
@login_required(login_url='/login')
def create_news(request):
    form = NewsForm(request.POST or None)

=======
    return render(request, "news.html", context)

# Detail (slug & uuid fallback)
@login_required(login_url='/login')
def show_news_detail_slug(request, slug):
    news = get_object_or_404(News, slug=slug)
    news.increment_views()
    return render(request, "news_detail.html", {"news": news})

@login_required(login_url='/login')
def show_news_detail_uuid(request, id):
    news = get_object_or_404(News, pk=id)
    news.increment_views()
    return render(request, "news_detail.html", {"news": news})

# CREATE
@login_required(login_url='/login')
def create_news(request):
    form = NewsForm(request.POST or None)
>>>>>>> origin/feat/news
    if request.method == 'POST' and form.is_valid():
        news_entry = form.save(commit=False)
        news_entry.user = request.user
        news_entry.save()
        messages.success(request, "Berita berhasil dibuat.")
<<<<<<< HEAD
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
=======
        return redirect('news:show_news_main')

    ctx = {
        'form': form,
        'action_url': reverse('news:create_news'),
        'page_title': 'Tambah Berita Baru',
        'submit_label': 'Publish News',
    }
    return render(request, "create_news.html", ctx)


# EDIT
@login_required(login_url='/login')
def edit_news(request, id):
    news = get_object_or_404(News, pk=id, user=request.user)  # batasi milik sendiri
>>>>>>> origin/feat/news
    form = NewsForm(request.POST or None, instance=news)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Berita berhasil diperbarui.")
<<<<<<< HEAD
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
=======
        return redirect('news:show_news_detail', id=news.id)

    ctx = {
        'form': form,
        'action_url': reverse('news:edit_news', args=[news.id]),
        'page_title': 'Edit Berita',
        'page_subtitle': 'Update your football news and stories',
        'submit_label': 'Update News',
    }
    return render(request, "create_news.html", ctx)


# Delete News
@require_POST
@login_required(login_url='/login')
def delete_news(request, id):
    # 1) cek ada/tidak
    try:
        n = News.objects.get(pk=id)
    except News.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    # 2) cek kepemilikan
    if n.user_id != request.user.id:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    # 3) hapus
    n.delete()
    return JsonResponse({'ok': True})
    
# AJAX: Create News
@login_required(login_url='/login')
@require_POST
def add_news_entry_ajax(request):
    if request.content_type == 'application/json':
        body = json.loads(request.body.decode('utf-8'))
        title = strip_tags(body.get("title", "")).strip()
        content = strip_tags(body.get("content", "")).strip()
        category = body.get("category", "")
        thumbnail = body.get("thumbnail", "")
        is_featured = bool(body.get("is_featured", False))
    else:
        title = strip_tags(request.POST.get("title", "")).strip()
        content = strip_tags(request.POST.get("content", "")).strip()
        category = request.POST.get("category", "")
        thumbnail = request.POST.get("thumbnail", "")
        is_featured = request.POST.get("is_featured") in ('on', 'true', '1')

    if not title or not content or not category:
        return JsonResponse({"error": "title, content, category wajib diisi."}, status=400)

    n = News.objects.create(
        title=title,
        content=content,
        category=category,
        thumbnail=thumbnail or None,
        is_featured=is_featured,
        user=request.user,
    )
    data = {
        'id': str(n.id),
        'slug': n.slug,
        'title': n.title,
        'content': n.content,
        'category': n.category,
        'thumbnail': n.thumbnail,
        'is_featured': n.is_featured,
        'created_at': n.created_at.isoformat() if n.created_at else None,
        'detail_url': n.get_absolute_url(),
    }
    return JsonResponse(data, status=201)

# JSON/XML Serializers
>>>>>>> origin/feat/news
@require_GET
def show_xml(request):
    news_list = News.objects.all().order_by('-created_at')
    xml_data = serializers.serialize("xml", news_list)
    return HttpResponse(xml_data, content_type="application/xml; charset=utf-8")

<<<<<<< HEAD
=======
# JSON Views
>>>>>>> origin/feat/news
@require_GET
def show_json(request):
    news_list = News.objects.select_related('user').all().order_by('-created_at')
    data = [
        {
            'id': str(news.id),
<<<<<<< HEAD
=======
            'slug': news.slug,
>>>>>>> origin/feat/news
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

<<<<<<< HEAD
=======
# XML by ID
>>>>>>> origin/feat/news
@require_GET
def show_xml_by_id(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    xml_data = serializers.serialize("xml", [news_item])
    return HttpResponse(xml_data, content_type="application/xml; charset=utf-8")

<<<<<<< HEAD
=======
# JSON by ID    
>>>>>>> origin/feat/news
@require_GET
def show_json_by_id(request, id):
    n = get_object_or_404(News.objects.select_related('user'), pk=id)
    data = {
        'id': str(n.id),
<<<<<<< HEAD
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
=======
        'slug': n.slug,
        'title': n.title or '',
        'content': n.content or '',
        'category': n.category or '',
        'thumbnail': n.thumbnail or '',
        'news_views': n.news_views or 0,
        'created_at': n.created_at.isoformat() if n.created_at else None,
        'is_featured': bool(n.is_featured),
        'user_id': n.user_id,
        'user_username': getattr(n.user, 'username', 'Anonymous'),
    }
    return JsonResponse(data)

# Komentar via AJAX
@require_GET
def get_comments(request, id):
    comments = Comment.objects.filter(news_id=id).select_related('user').order_by('-created_at')
    data = [
        {
            'id': str(c.id),
            'user': c.user.username,
            'content': c.content,
            'created_at': c.created_at.strftime('%d %b %Y, %H:%M')
        }
        for c in comments
    ]
    return JsonResponse({'comments': data})

# Tambah Komentar via AJAX
@login_required(login_url='/login')
@require_POST
def add_comment(request, id):
    try:
        body = json.loads(request.body.decode('utf-8'))
        content = (body.get('content') or '').strip()
        if not content:
            return JsonResponse({'error': 'Komentar tidak boleh kosong.'}, status=400)

        news = get_object_or_404(News, id=id)
        comment = Comment.objects.create(
            news=news,
            user=request.user,
            content=content,
            created_at=timezone.now()
        )
        return JsonResponse({
            'id': str(comment.id),
            'user': comment.user.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%d %b %Y, %H:%M')
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Payload harus JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
>>>>>>> origin/feat/news
