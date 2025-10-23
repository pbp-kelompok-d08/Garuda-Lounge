from django.forms import ModelForm
from .models import Merch  # ✅ ganti ini, titik artinya import dari app yang sama

class MerchForm(ModelForm):
    class Meta:
        model = Merch
        fields = ["name", "description", "price", "image"]