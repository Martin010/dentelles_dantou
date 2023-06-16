from django.contrib import admin

from carts.models import CartItem, Cart

admin.site.register(Cart)
admin.site.register(CartItem)
