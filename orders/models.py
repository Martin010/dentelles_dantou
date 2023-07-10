from django.db import models

from accounts.models import Account
from store.models import Product, Variation


class Payment(models.Model):
    user            = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id      = models.CharField(max_length=128)
    payment_method  = models.CharField(max_length=128)
    amount_paid     = models.CharField(max_length=128)  # Total amount paid
    status          = models.CharField(max_length=128)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user            = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment         = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number    = models.CharField(max_length=32)
    first_name      = models.CharField(max_length=64)
    last_name       = models.CharField(max_length=64)
    phone           = models.CharField(max_length=64)
    email           = models.EmailField(max_length=128)
    address_line_1  = models.CharField(max_length=128)
    address_line_2  = models.CharField(max_length=128)
    country         = models.CharField(max_length=64)
    state           = models.CharField(max_length=64)
    city            = models.CharField(max_length=64)
    order_note      = models.CharField(max_length=128, blank=True)
    order_total     = models.FloatField()
    tax             = models.FloatField()
    status          = models.CharField(max_length=16, choices=STATUS, default='New')
    ip              = models.CharField(blank=True, max_length=32)
    is_ordered      = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name


class OrderProduct(models.Model):
    order           = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment         = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user            = models.ForeignKey(Account, on_delete=models.CASCADE)
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation       = models.ForeignKey(Variation, on_delete=models.CASCADE)
    color           = models.CharField(max_length=64)
    size            = models.CharField(max_length=64)
    quantity        = models.IntegerField()
    product_price   = models.FloatField()
    ordered         = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
