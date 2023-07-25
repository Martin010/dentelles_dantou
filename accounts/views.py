from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import RegistrationForm, UserForm, UserProfileForm
from accounts.models import Account, UserProfile

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from carts.models import Cart, CartItem
from carts.views import _cart_id

import requests

from orders.models import Order


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Auto create username (can add field in register form)
            username = email.split("@")[0]

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )

            # Can pass phone_number in the function create_user (in models.py) so add it after the user's creation
            user.phone_number = phone_number

            user.save()

            # Create User Profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()

            # User Activation
            current_site = get_current_site(request)
            mail_subject = 'Activation de votre compte "Les Dentelles de Dantou"'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),  # Encode the user id for safety (hidden)
                'token': default_token_generator.make_token(user)  # Create a token for this particular user
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # messages.success(
            #     request,
            #     'Merci pour votre inscription. '
            #     'Nous vous avons envoyé un lien de validation de compte sur votre adresse email. '
            #     'Veuillez valider votre compte afin de poursuivre votre navigation.'
            # )

            # send command and email in the request to display the email verification message in the login page
            return redirect('/accounts/login/?command=verification&email=' + email)

    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            # Check if the user adds items to the cart before being logged in
            try:
                # If a cart id exists, link the user and the cart items
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()

                if is_cart_item_exists:
                    # Getting the product variations by cart id
                    cart_item = CartItem.objects.filter(cart=cart)
                    product_variation = []
                    product_id_list = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))  # list() because existing_variation is a query_set
                        product_id_list.append(item.id)

                    # Get the cart items from the user to access to his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    existing_variations_list = []
                    items_id_list = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        existing_variations_list.append(list(existing_variation))  # list() because existing_variation is a query_set
                        items_id_list.append(item.id)

                    # Check if the product of the cart is in the product list of the user
                    for i, product in enumerate(product_variation):
                        product_id = product_id_list[i]
                        current_item = CartItem.objects.get(id=product_id)

                        if product in existing_variations_list:
                            # If the product is in the user list : get the object and increment the quantity
                            index = existing_variations_list.index(product)
                            item_id = items_id_list[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += current_item.quantity
                            item.user = user
                            item.save()
                        else:
                            # If the product is not in the user list : add the product to the cart
                            current_item.user = user
                            current_item.save()
            except:
                pass

            auth.login(request, user)
            messages.success(request, 'Vous êtes maintenant connecté !')
            url = request.META.get('HTTP_REFERER')  # Get the previous url
            try:
                # Clean the url
                query = requests.utils.urlparse(url).query  # next=/cart/checkout
                params = dict(x.split('=') for x in query.split('&'))   # {'next': '/cart/checkout'}

                # If you try to login through a redirection
                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'l\'email et/ou le mot de passe est incorrect.')
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')  # Check if you are login before trying to logout
def logout(request):
    auth.logout(request)
    messages.success(request, 'Vous êtes déconnectez.')

    return redirect('login')


def activate(request, uidb64, token):
    # Check if the link is available
    try:
        uid = urlsafe_base64_decode(uidb64).decode()  # Decode uidb64 and restore it
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    # If user and token exist
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Félicitation ! Votre compte est activé et votre inscription est terminée !')
        return redirect('login')
    else:
        messages.error(request, 'Le lien d\'activation n\'est plus valide')
        return redirect('register')


@login_required(login_url='login')  # If not login, redirect to login page (can access to the dashboard only if the user is login)
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()

    context = {
        'orders_count': orders_count
    }

    return render(request, 'accounts/dashboard.html', context)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)  # The exact lookup is used to get records with a specified value. The exact lookup is case-sensitive.

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Réinitialisation de votre mot de passe'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),  # Encode the user id for safety (hidden)
                'token': default_token_generator.make_token(user)  # Create a token for this particular user
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(
                request,
                f'Nous vous avons envoyé un lien de réinitialisation de mot de passe sur votre adresse email : {email}'
            )

            return redirect('login')
        else:
            messages.error(request, 'Le compte n\'existe pas.')
            return redirect('forgot_password')

    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    # Check if the link is available
    try:
        uid = urlsafe_base64_decode(uidb64).decode()  # Decode uidb64 and restore it
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    # If user and token exist
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Veuillez réinitialiser votre mot de passe')
        return redirect('reset_password')
    else:
        messages.error(request, 'Le lien n\'est plus valide')
        return redirect('login')


def reset_password(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # If the two passwords are the same reset the user password
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)  # set_password is a django function to change a specific user password (automatically hash the password)
            user.save()
            messages.success(request, 'Le mot de passe a été réinitialisé avec succès !')
            return redirect('login')
        else:
            messages.error(request, 'Les mots de passe ne sont pas identiques !')
            return redirect('reset_password')

    else:
        return render(request, 'accounts/reset_password.html')


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')

    context = {
        'orders': orders
    }

    return render(request, 'accounts/my_orders.html', context)


@login_required(login_url='login')
def edit_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        # Update the user and the profile if forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Votre profil a été mis à jour.')
            return redirect('edit_profile')

        # Display user and profile information if no form is sent
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_profile': user_profile,
    }

    return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)   # Check this username is exactly the same in the database

        if new_password == confirm_password:
            success = user.check_password(current_password)     # Django's method that check if the current password is available (hash)
            if success:
                user.set_password(new_password)     # Django inbuilt function that automatically hash the new password
                user.save()

                # If you want automatically logout the user after password change:
                # auth.logout(request)

                messages.success(request, 'Le mot de passe a été modifié avec succès.')
                return redirect('change_password')

            else:
                messages.error(request, 'Le mot de passe actuel est incorrect.')
                return redirect('change_password')

        else:
            messages.error(request, 'Les nouveaux mots de passe ne correspondent pas.')
            return redirect('change_password')


    return render(request, 'accounts/change_password.html')
