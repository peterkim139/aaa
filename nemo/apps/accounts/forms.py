import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm as CoreAuthenticationForm,UserCreationForm
from django.core.exceptions import ValidationError

from accounts.models import User


def valdiate_lettersonly(value):
    if not re.match("^[A-Za-z ]*$", value):
        raise ValidationError('Name field should contain only letters')


def valdiate_numbersonly(value):
    if not re.match("^[0-9 \+\-\(\)]*$", value):
        raise ValidationError('Please enter a valid phone number')

class LoginFormMixin(object):
    username = forms.CharField(label='User Name', max_length=255, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username', '')
        password = self.cleaned_data.get('password', '')
        if username and password:
            self.user = None
            if User.objects.filter(email=username).exists():
                user = User.objects.get(email=username)
                if user.check_password(password):
                    self.user = user
                    if self.user is not None:
                        self.user_cache = self.user
                    if not self.user.is_active:
                        raise forms.ValidationError('Your account is inactive please check your email and activate it',
                                                    code='inactive')
                else:
                    raise forms.ValidationError('Invalid username or password', code='invalid')
                self.user.backend = 'django.contrib.auth.backends.ModelBackend'
            else:
                raise forms.ValidationError('Invalid username or password', code='invalid')
        return self.cleaned_data

class AuthenticationForm(LoginFormMixin, CoreAuthenticationForm):
    username = forms.CharField(
        label='Email',
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'formControl'}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'formControl'}),
        required=True
    )

class RegistrationForm(forms.Form):

    email = forms.CharField(label='Email',max_length=60,min_length=5,required=True)
    phone_number = forms.CharField(label="Phone number", max_length=50, required=True,
                                   validators=[valdiate_numbersonly],
                                   widget=forms.TextInput(attrs={'class': 'formControl'}), )
    first_name = forms.CharField(label='Name', max_length=255, required=True, validators=[valdiate_lettersonly],
                           widget=forms.TextInput(attrs={'class': 'formControl'}), )
    last_name = forms.CharField(label='Surname', max_length=255, required=True, validators=[valdiate_lettersonly],
                           widget=forms.TextInput(attrs={'class': 'formControl'}), )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'formControl'}),
        required=True
    )

    confirmpassword = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'formControl'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        if 'form' in kwargs:
            if 'is_social' in kwargs['data']:
                self.fields['password'].required = False
                self.fields['confirmpassword'].required = False
                self.fields['phone_number'].required = False

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already taken")
        return email

    def clean_confirmpassword(self):
        password = self.cleaned_data.get('password','')
        confirmpassword = self.cleaned_data.get('confirmpassword','')
        if password != confirmpassword:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data
