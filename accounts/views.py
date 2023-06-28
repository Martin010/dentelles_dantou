from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.forms import RegistrationForm
from accounts.models import Account


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
            messages.success(request, 'Inscription validée !')

            return redirect('register')

    else:
        form = RegistrationForm()

    context ={
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
            # messages.success(request, 'Vous êtes maintenant connecté !')
            return redirect('home')
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

