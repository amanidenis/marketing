from django.contrib import admin
from .models import Product  # Ensure this matches the correct import

# Register your models here.
class ProductAdmin(admin.ModelAdmin):  # Class names should be in CamelCase
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}  # Fixed spelling

admin.site.register(Product, ProductAdmin)  # Ensure this matches the correct class names
