from django import forms
from .models import Merch

# Base Tailwind styles (biar konsisten di semua form)
BASE_INPUT = (
    "w-full border border-gray-300 rounded-xl2 p-2 "
    "focus:outline-none focus:ring-2 focus:ring-[#AA1515]/40 "
    "text-[#111111] placeholder-gray-400"
)
BASE_TEXTAREA = BASE_INPUT + " min-h-[120px]"
BASE_SELECT = BASE_INPUT + " bg-white"

class MerchForm(forms.ModelForm):
    class Meta:
        model = Merch
        fields = ["name", "description", "category", "price", "thumbnail", "product_link"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": BASE_INPUT, "placeholder": "Masukkan nama merchandise"}
            ),
            "description": forms.Textarea(
                attrs={"class": BASE_TEXTAREA, "placeholder": "Tulis deskripsi merchandise..."}
            ),
            "category": forms.Select(attrs={"class": BASE_SELECT}),
            "price": forms.NumberInput(
                attrs={"class": BASE_INPUT, "placeholder": "Masukkan harga merchandise"}),
            "thumbnail": forms.URLInput(
                attrs={"class": BASE_INPUT, "placeholder": "https://example.com/image.jpg"}
            ),
            "product_link": forms.URLInput(
                attrs={"class": BASE_INPUT, "placeholder": "https://example.com/example-merch"}
            ),
        }