from django.contrib import admin

from store.models import Product, Variation, ReviewRating


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    readonly_fields = ('created_date', 'modified_date')


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    readonly_fields = ('created_date',)
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'product', 'rating', 'created_at', 'updated_at', 'status')
    readonly_fields = ('product', 'user', 'subject', 'review', 'rating', 'ip', 'created_at', 'updated_at')
    list_filter = ('product', 'updated_at', 'status')


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
