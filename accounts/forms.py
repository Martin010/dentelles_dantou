from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Entrez un mot de passe',
        'class': 'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Répétez le mot de passe',
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Entrez votre prénom'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Entrez votre nom'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Entrez votre numéro de téléphone'
        self.fields['email'].widget.attrs['placeholder'] = 'Entrez votre adresse email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

