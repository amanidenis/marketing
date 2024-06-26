from django.contrib import admin
from .models import Product, Variations

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}

admin.site.register(Product, ProductAdmin)

class VariationsAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'created_date')
    list_filter = ('product', 'variation_category', 'is_active')
    list_editable = ('is_active',)

admin.site.register(Variations, VariationsAdmin)
