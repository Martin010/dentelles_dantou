from carts.models import Cart, CartItem
from carts.views import _cart_id


def counter(request):
    """
        Update digit of the card with the number of products in the card
    """

    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))

            # If user is login -> count all items which have the field of this particular user
            # if the user is not login -> count all objects of the cart
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])

            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0

    return dict(cart_count=cart_count)
