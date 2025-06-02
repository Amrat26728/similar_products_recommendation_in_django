from django.contrib import admin
from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at')
    search_fields = ('name', 'category')
    list_filter = ('category', 'created_at')
    ordering = ('created_at',)


admin.site.register(Product, ProductAdmin)