from django.forms import ModelForm
from .models import Merch

class MerchForm(ModelForm):
    class Meta:
        model = Merch
        fields = ["name", "description", "category", "price", "thumbnail", "product_link"]