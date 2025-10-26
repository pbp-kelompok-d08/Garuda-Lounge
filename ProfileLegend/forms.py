from django.forms import ModelForm
from ProfileLegend.models import Player

class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ["nama", "posisi", "klub", "umur", "foto"]