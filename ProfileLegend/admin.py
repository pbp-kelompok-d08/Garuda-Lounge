from django.contrib import admin
from .models import LegendPlayer

@admin.register(LegendPlayer)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'current_club', 'age', 'market_value')
    search_fields = ('name', 'current_club')
