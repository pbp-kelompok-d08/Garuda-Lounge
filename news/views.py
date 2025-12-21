from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
from django.utils.html import strip_tags
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import News, Comment
from .forms import NewsForm, CommentForm

import json
import requests

# Halaman Publik/List 
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


@login_required(login_url='/login')
def create_news(request):
    form = NewsForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        news_entry = form.save(commit=False)
        news_entry.user = request.user
        news_entry.save()
        messages.success(request, "Berita berhasil dibuat.")
        return redirect('news:show_news_main')

    ctx = {
        'form': form,
        'action_url': reverse('news:create_news'),
        'page_title': 'Tambah Berita Baru',
        'submit_label': 'Publish News',
    }
    return render(request, "create_news.html", ctx)


@login_required(login_url='/login')
def edit_news(request, id):
    news = get_object_or_404(News, pk=id, user=request.user)
    form = NewsForm(request.POST or None, instance=news)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Berita berhasil diperbarui.")
        return redirect('news:show_news_detail', id=news.id)

    ctx = {
        'form': form,
        'action_url': reverse('news:edit_news', args=[news.id]),
        'page_title': 'Edit Berita',
        'page_subtitle': 'Update your football news and stories',
        'submit_label': 'Update News',
    }
    return render(request, "create_news.html", ctx)


@require_POST
@login_required(login_url='/login')
def delete_news(request, id):
    try:
        n = News.objects.get(pk=id)
    except News.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    if n.user_id != request.user.id:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    n.delete()
    return JsonResponse({'ok': True})

@require_GET
def show_json(request):
    news_list = News.objects.select_related('user').all().order_by('-created_at')
    data = [
        {
            'id': str(news.id),
            'slug': news.slug,
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
def show_json_by_id(request, id):
    n = get_object_or_404(News.objects.select_related('user'), pk=id)
    data = {
        'id': str(n.id),
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


@require_GET
def show_xml(request):
    news_list = News.objects.all().order_by('-created_at')
    xml_data = serializers.serialize("xml", news_list)
    return HttpResponse(xml_data, content_type="application/xml; charset=utf-8")


@require_GET
def show_xml_by_id(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    xml_data = serializers.serialize("xml", [news_item])
    return HttpResponse(xml_data, content_type="application/xml; charset=utf-8")


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

@csrf_exempt
def add_comment(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    # kalau belum login, jangan create comment
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not authenticated"}, status=401)

    try:
        body = json.loads(request.body.decode("utf-8"))
        content = (body.get("content") or "").strip()
        if not content:
            return JsonResponse({"error": "Komentar tidak boleh kosong."}, status=400)

        news = get_object_or_404(News, id=id)

        comment = Comment.objects.create(
            news=news,
            user=request.user,   # INI PENTING
            content=content,
            created_at=timezone.now()
        )

        return JsonResponse({
            "id": str(comment.id),
            "user": comment.user.username,
            "content": comment.content,
            "created_at": comment.created_at.strftime("%d %b %Y, %H:%M"),
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Payload harus JSON."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)

@csrf_exempt
def add_news_entry_ajax(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body from the request
            data = json.loads(request.body.decode('utf-8'))
            title = strip_tags(data.get("title", "")).strip()
            content = strip_tags(data.get("content", "")).strip()
            category = data.get("category", "").strip()
            thumbnail = data.get("thumbnail", "").strip()
            is_featured = bool(data.get("is_featured", False))

            # Validate input fields
            if not title or not content or not category:
                return JsonResponse({"error": "Title, content, and category are required."}, status=400)

            # Create the new news entry
            new_news = News.objects.create(
                title=title,
                content=content,
                category=category,
                thumbnail=thumbnail or None,
                is_featured=is_featured,
                user=request.user
            )

            # Return the created news entry as JSON
            return JsonResponse({
                "status": "success",
                "id": new_news.id,
                "slug": new_news.slug,
                "title": new_news.title,
                "content": new_news.content,
                "category": new_news.category,
                "thumbnail": new_news.thumbnail,
                "is_featured": new_news.is_featured,
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)

@csrf_exempt
def create_news_flutter(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "error", "message": "Not authenticated. Please login first."},
            status=401
        )

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse(
            {"status": "error", "message": "Payload must be valid JSON."},
            status=400
        )

    title = strip_tags(data.get("title", "")).strip()
    content = strip_tags(data.get("content", "")).strip()
    category = (data.get("category") or "").strip()
    thumbnail = (data.get("thumbnail") or "").strip()
    is_featured = bool(data.get("is_featured", False))

    if not title or not content or not category:
        return JsonResponse(
            {"status": "error", "message": "title, content, category wajib diisi."},
            status=400
        )

    allowed = {'transfer', 'update', 'exclusive', 'match', 'rumor', 'analysis'}
    if category not in allowed:
        return JsonResponse(
            {"status": "error", "message": f"Invalid category: {category}"},
            status=400
        )

    new_news = News.objects.create(
        title=title,
        content=content,
        category=category,
        thumbnail=thumbnail or None,
        is_featured=is_featured,
        user=request.user
    )

    return JsonResponse({"status": "success", "id": str(new_news.id)}, status=201)
