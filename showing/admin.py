from django.contrib import admin
from .models import Showing

@admin.register(Showing)
class ShowingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'date', 'time', 'price', 'created_at', 'updated_at')
    list_filter = ('date', 'movie')
    search_fields = ('movie__title',)
