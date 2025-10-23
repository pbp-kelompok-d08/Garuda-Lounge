import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from django.urls import reverse


class News(models.Model):
    CATEGORY_CHOICES = [
        ('match', 'Match'),
        ('exclusive', 'Exclusive'),
        ('update', 'Update'),
        ('analysis', 'Analysis'),
        ('rumor', 'Rumor'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='news')
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='update')
    thumbnail = models.URLField(blank=True, null=True)
    news_views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_hot(self):
        return self.news_views > 20

    def increment_views(self):
        type(self).objects.filter(pk=self.pk).update(news_views=F('news_views') + 1)
        self.refresh_from_db(fields=['news_views'])

    def get_absolute_url(self):
        return reverse('news:show_news_detail', args=[str(self.pk)])


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Komentar oleh {self.user.username} di {self.news.title}"
