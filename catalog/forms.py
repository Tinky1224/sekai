from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from catalog.models import Account, Music

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label = 'Email',
        widget = forms.EmailInput(attrs={'autocomplete':'email'}),
        error_messages = {'invalid':'Please enter a valid email.', 'required':'Please enter your email.'},
    )
    password1 = forms.CharField(
        label = 'Password1',
        strip = False,
        widget = forms.PasswordInput(attrs={'autocomplete':'new-password'}),
        error_messages = {'required':'Please enter your password'},
    )
    password2 = forms.CharField(
        label = 'Password2',
        strip = False,
        widget = forms.PasswordInput(attrs={'autocomplete':'new-password'}),
        error_messages = {'required':'Please repeat your password'},
    )
    error_messages = ({'password_mismatch': 'two passwords must be same.'},)
    
    class Meta:
        model = Account
        fields = ['email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            Account.objects.get(email=email)
        except:
            return email
        raise forms.ValidationError(f'{email} is existed')


class MusicForm(ModelForm):
    class Meta:
        model = Music
        fields = '__all__'