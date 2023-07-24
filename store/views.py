from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from orders.models import OrderProduct
from store.forms import ReviewForm
from store.models import Product, ReviewRating


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        # If a category is selected, show all products of this category
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()

        # Paginator behavior
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
    else:
        # If none category is selected, show all products
        products = Product.objects.all().filter(is_available=True).order_by('id')
        product_count = products.count()

        # Paginator behavior
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        page_products = paginator.get_page(page)

    context = {
        'products': page_products,
        'product_count': product_count
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        # Select the product by his category slug and his slug
        single_product = Product.objects.get(category__slug=category_slug,
                                             slug=product_slug)  # category__slug is the syntax to access to the slug

        # Behavior of the button "ajouter au panier"
        # in_cart : if product is in the cart, don't show the button "ajouter au panier"
        # cart__cart_id : access to the cart of cart_id (cart is a foreign key of cart_item)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        # Check if the user already ordered the product and can post a review
        try:
            order_product = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            order_product = None
    else:
        order_product = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'order_product': order_product,
        'reviews': reviews,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    products = None
    product_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            # Do a case insensitive search for all products that have the value "keyword" in the description column:
            # Q : Queryset
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')  # Store the previous url
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)    # The ids of the foreign keys user and product -> __id
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Merci ! Votre commentaire a été modifié.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')   # Store IP address
                data.product_id = product_id
                data.user_id = request.user.id

                data.save()

                messages.success(request, 'Merci ! Votre commentaire a été créé.')
                return redirect(url)
