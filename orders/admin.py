from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from orders.models import Payment, Order, OrderProduct


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user', 'payment_method', 'amount_paid', 'created_at', 'status')
    list_display_links = ('payment_id', 'user')
    readonly_fields = ('created_at',)
    ordering = ('payment_id',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'first_name', 'last_name', 'order_total', 'status', 'created_at', 'updated_at', 'is_ordered')
    list_display_links = ('order_number', 'first_name', 'last_name', 'order_total')
    readonly_fields = ('created_at',)
    ordering = ('-updated_at',)


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment', 'user', 'product', 'variation', 'ordered', 'created_at', 'updated_at')
    list_display_links = ('order', 'payment', 'user', 'variation')
    readonly_fields = ('created_at',)
    ordering = ('-user',)


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
