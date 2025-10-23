from django.forms import ModelForm
from .models import News  # ✅ ganti ini, titik artinya import dari app yang sama

class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ["title", "content", "category", "thumbnail", "is_featured"]
