from django import forms
from .models import News, Comment

# Base Tailwind styles (biar konsisten di semua form)
BASE_INPUT = (
    "w-full border border-gray-300 rounded-xl2 p-2 "
    "focus:outline-none focus:ring-2 focus:ring-[#AA1515]/40 "
    "text-[#111111] placeholder-gray-400"
)
BASE_TEXTAREA = BASE_INPUT + " min-h-[120px]"
BASE_SELECT = BASE_INPUT + " bg-white"
BASE_CHECKBOX = "h-4 w-4 text-[#AA1515] focus:ring-[#AA1515]/40 rounded"

# News Form 
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "content", "category", "thumbnail", "is_featured"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": BASE_INPUT, "placeholder": "Masukkan judul berita"}
            ),
            "content": forms.Textarea(
                attrs={"class": BASE_TEXTAREA, "placeholder": "Tulis isi berita..."}
            ),
            "category": forms.Select(attrs={"class": BASE_SELECT}),
            "thumbnail": forms.URLInput(
                attrs={"class": BASE_INPUT, "placeholder": "https://example.com/image.jpg"}
            ),
            "is_featured": forms.CheckboxInput(attrs={"class": BASE_CHECKBOX}),
        }

# Comment Form 
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "w-full border border-gray-300 rounded-xl2 p-2 "
                             "focus:outline-none focus:ring-2 focus:ring-[#AA1515]/40 "
                             "text-[#111111] placeholder-gray-400",
                    "placeholder": "Tulis komentar...",
                }
            ),
        }
