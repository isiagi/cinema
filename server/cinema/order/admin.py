from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ( 'showing', 'total_price', 'created_at', 'updated_at')
