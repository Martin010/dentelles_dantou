from django.contrib import admin

from store.models import Product, Variation


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    readonly_fields = ('created_date', 'modified_date')

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    readonly_fields = ('created_date',)
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
