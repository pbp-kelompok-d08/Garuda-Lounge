# profil_legend/admin.py

from django.contrib import admin
from .models import PlayerProfile # Impor model baru

# Ini akan membuat tampilan admin lebih rapi
@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'current_club', 'age', 'market_value')
    search_fields = ('name', 'current_club')