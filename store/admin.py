from django.contrib import admin

from store.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    readonly_fields = ('created_date', 'modified_date')

admin.site.register(Product, ProductAdmin)
