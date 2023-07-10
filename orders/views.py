import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect

from carts.models import CartItem
from orders.forms import OrderForm
from orders.models import Order


def payments(request):
    return render(request, 'orders/payments.html')


def place_order(request, total=0, quantity=0):
    current_user = request.user

    # If there is no item in the cart, redirect to the shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (1.5 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']

            data.order_total = grand_total
            data.tax = tax

            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number with current day, month and year, with the id number of this order
            year = int(datetime.date.today().strftime('%Y'))
            month = int(datetime.date.today().strftime('%m'))
            day = int(datetime.date.today().strftime('%d'))
            date = datetime.date(year, month, day)
            current_date = date.strftime("%Y%m%d")  #20220710

            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            # To display all the data (billing address etc.) we need order object
            # is_ordered is False because we can have the same order_number if the user orders several times in a day.
            # So the only order which can be ordered is the order object with the variable is_ordered to False
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)

    else:
        return redirect('checkout')