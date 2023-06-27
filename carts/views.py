from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from carts.models import Cart, CartItem
from store.models import Product, Variation


def _cart_id(request):
    """
        Get cart_id
    """
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    # Get product
    product = Product.objects.get(id=product_id)

    # Get product variations
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            # Get variations chosen
            key = item
            value = request.POST[key]

            try:
                # iexact : get records with a specified value (i ignore the casse)
                # Here check if the key and the value are matching with the model values (variation category and value)
                variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                  variation_value__iexact=value)
                product_variation.append(variation)
            except ObjectDoesNotExist:
                pass

    # Get or create cart
    try:
        # Get the cart using the cart_id present in the session
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    # Combine product, variations and cart
    # Check if the cart item already exist
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)

        # Check if the variation of the item already exist
        existing_variations_list = []
        items_id_list = []
        for item in cart_item:
            existing_variation = item.variations.all()
            existing_variations_list.append(list(existing_variation)) # list() because existing_variation is a query_set
            items_id_list.append(item.id)

        if product_variation in existing_variations_list:
            # The item and the variation already exist -> increase quantity
            index = existing_variations_list.index(product_variation)
            item_id = items_id_list[index]
            cart_item = CartItem.objects.get(product=product, id=item_id)
            cart_item.quantity += 1
        else:
            # The item exists but not the variation -> create new item
            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)

    else:
        # The item does not exist -> create new item
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)

    cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        # Remove cart item if user press the minus button and quantity = 1
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except ObjectDoesNotExist:
        pass

    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

    # Remove cart item if user press the button remove
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        # total price, total quantity for all the cart
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (1.5 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass  # Just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)
