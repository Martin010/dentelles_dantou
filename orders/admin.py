from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from orders.models import Payment, Order, OrderProduct


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user', 'payment_method', 'amount_paid', 'created_at', 'status')
    list_filter = ('status', 'payment_method', 'created_at')
    readonly_fields = ('created_at',)
    list_per_page = 20


class OrderProductInline(admin.TabularInline):
    # Elements to display inline
    model = OrderProduct
    extra = 0   # don't add extra empty inline elements
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'phone', 'email', 'order_total', 'status', 'created_at', 'is_ordered')
    list_filter = ('status', 'is_ordered', 'created_at')
    search_fields = ('order_number', 'first_name', 'last_name', 'phone', 'email')
    readonly_fields = ('created_at',)
    list_per_page = 20
    # Display all products in the details of the order
    inlines = [OrderProductInline]


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'payment', 'user', 'ordered', 'created_at', 'updated_at')
    list_filter = ('product', 'created_at')
    readonly_fields = ('created_at',)


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
