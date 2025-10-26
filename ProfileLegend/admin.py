from django.contrib import admin
from .models import LegendPlayer

@admin.register(LegendPlayer)
class LegendPlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'club', 'age', 'is_legend')
    list_filter = ('position', 'is_legend')
    search_fields = ('name', 'club')
