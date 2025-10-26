from django.forms import ModelForm
from ProfileAktif.models import Player  # ⬅️ pastikan ini sesuai dengan nama app kamu

class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ["nama", "posisi", "klub", "umur", "market_value", "foto"]
