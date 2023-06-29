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

    def clean(self):
        # Django function called after the execution and the cleaning of all fields.
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Check if the fields password are the same
        if password != confirm_password:
            raise forms.ValidationError(
                "Les mots de passes ne sont pas identiques."
            )

    def __init__(self, *args, **kwargs):
        # Django function called at the initialisation of the form
        super(RegistrationForm, self).__init__(*args, **kwargs)

        # Add placeholders in fields
        self.fields['first_name'].widget.attrs['placeholder'] = 'Entrez votre prénom'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Entrez votre nom'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Entrez votre numéro de téléphone'
        self.fields['email'].widget.attrs['placeholder'] = 'Entrez votre adresse email'

        # Add class 'form-control' attributes to all the fields
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

