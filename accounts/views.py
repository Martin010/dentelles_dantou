from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm
from accounts.models import Account

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.template.loader import render_to_string
from django.core.mail import EmailMessage


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
            return redirect('/accounts/login/?command=verification&email='+email)

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
            auth.login(request, user)
            messages.success(request, 'Vous êtes maintenant connecté !')
            return redirect('dashboard')
        else:
            messages.error(request, 'l\'email et/ou le mot de passe est incorrect.')
            return redirect('login')

    return render(request, 'accounts/login.html')


# Check if you are login before trying to logout
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Vous êtes déconnectez.')

    return redirect('login')


def activate(request, uidb64, token):
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


@login_required(login_url='login')  # If not login, redirect to login page (can access to the dashboard only if the user if login)
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
