# news/models.py
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from django.urls import reverse
from django.utils.text import slugify


class News(models.Model):
    CATEGORY_CHOICES = [
        ('match', 'Match'),
        ('exclusive', 'Exclusive'),
        ('update', 'Update'),
        ('analysis', 'Analysis'),
        ('rumor', 'Rumor'),
        ('transfer', 'Transfer'),
    ]

    # PK tetap UUID agar kompatibel dengan data/URL lama
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # penulis/editor (boleh kosong supaya tidak crash saat seeding)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='news'
    )

    title = models.CharField(max_length=255)

    # slug untuk URL cantik; unik; otomatis dari title saat pertama kali save
    slug = models.SlugField(max_length=260, unique=True, blank=True)

    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='update')

    # pakai URLField; kalau nanti mau upload file lokal tinggal ganti ke ImageField
    thumbnail = models.URLField(blank=True, null=True)

    news_views = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    @property
    def is_hot(self):
        return self.news_views > 20

    def increment_views(self):
        type(self).objects.filter(pk=self.pk).update(news_views=F('news_views') + 1)
        self.refresh_from_db(fields=['news_views'])

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:240] or str(self.id)
            candidate = base
            n = 1
            while News.objects.filter(slug=candidate).exists():
                n += 1
                candidate = f"{base}-{n}"
            self.slug = candidate
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        try:
            return reverse('news:show_news_detail_slug', kwargs={'slug': self.slug})
        except Exception:
            # fallback: kompatibel dengan implementasi lama kamu
            return reverse('news:show_news_detail', args=[str(self.pk)])


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)   # komentar wajib login
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['news', 'created_at']),
        ]

    def __str__(self):
        return f"Komentar oleh {self.user.username} di {self.news.title}"
