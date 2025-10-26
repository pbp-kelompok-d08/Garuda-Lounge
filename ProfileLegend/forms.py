from django.forms import ModelForm
from ProfileLegend.models import LegendPlayer

class LegendPlayerForm(ModelForm):
    class Meta:
        model = LegendPlayer
        fields = ["name", "position", "club", "age", "photo_url"]