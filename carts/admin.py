from django.contrib import admin

from carts.models import CartItem, Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')
    readonly_fields = ('date_added',)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
