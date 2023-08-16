from django import forms
from .models import Account, UserProfile


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


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        """ Add attribute class="form-control" in all the fields """
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    # Hide path of the file in the profile picture field
    profile_picture = forms.ImageField(required=False, error_messages={'invalid': ("Uniquement des images")}, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'address_line_1', 'address_line_2', 'country', 'state', 'city')

    def __init__(self, *args, **kwargs):
        """ Add attribute class="form-control" in all the fields"""
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
