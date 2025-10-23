from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewsForm
from .models import News
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def show_news(request):
    news_list = News.objects.all().order_by('-created_at')  # urut dari terbaru
    context = {
        'news_list': news_list,
    }
    return render(request, "news.html", context)


@login_required(login_url='/login')
def create_news(request):
    form = NewsForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('news:show_news')

    context = {'form': form}
    return render(request, "create_news.html", context)


@login_required(login_url='/login')
def show_news_detail(request, id):
    news = get_object_or_404(News, pk=id)
    news.increment_views()

    context = {
        'news': news
    }
    return render(request, "news_detail.html", context)
