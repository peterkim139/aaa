import re
import datetime
from django import forms
from django.contrib.auth.forms import AuthenticationForm as CoreAuthenticationForm,UserCreationForm
from django.core.exceptions import ValidationError
from accounts.models import User
from django.conf import settings

def validate_file(value):
    content_type = value.content_type.split('/')[0]
    if content_type in settings.CONTENT_TYPES:
        if value._size > int(settings.MAX_UPLOAD_SIZE):
            raise forms.ValidationError('Please keep file size under 2 Mb')
    else:
        raise forms.ValidationError('Only .jpg/jpeg/png/gif files allowed.')

def valdiate_lettersonly(value):
    if not re.match("^[A-Za-z ]*$", value):
        raise ValidationError('Name field should contain only letters')


def valdiate_numbersonly(value):
    if not re.match("^[0-9]*$", value):
        raise ValidationError('Please enter a valid phone number')

def validate_zipcodeonly(value):
    if not re.match("^[0-9]*$", value):
        raise ValidationError('Please enter a valid zip code')

def validate_billing_numbersonly(value):
    if not re.match("^[0-9]*$", value):
        raise ValidationError('Field should contain only numbers')

def validate_month(value):
    if not re.match("^[0-9]*$", value) or (int(value) < 1 or int(value) > 12):
        raise ValidationError('Month value can be from 01 to 12')

def validate_year(value):

    if not re.match("^[0-9]*$", value) or ( int(value) > 2050 or int(value) < datetime.datetime.now().year):
        raise ValidationError('Please enter a correct year')


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

class SocialForm(forms.Form):

    email = forms.CharField(label='Email',max_length=60,min_length=5,required=True)
    first_name = forms.CharField(label='Name', max_length=255, required=True, validators=[valdiate_lettersonly],
                           widget=forms.TextInput(attrs={'class': 'formControl'}), )
    last_name = forms.CharField(label='Surname', max_length=255, required=True, validators=[valdiate_lettersonly],
                           widget=forms.TextInput(attrs={'class': 'formControl'}), )

class ProfileForm(forms.Form):

    def __init__(self, *args, **kwargs):
            super(ProfileForm, self).__init__(*args, **kwargs)
            self.fields['image_file'].widget.attrs.update({'class': 'formControl'})

    email = forms.CharField(label='Email',max_length=60,min_length=5,required=True,widget=forms.TextInput(attrs={'class': 'formControl'}))
    phone_number = forms.CharField(label="Phone Number - Numbers only", max_length=50, required=True,
                                   validators=[valdiate_numbersonly],
                                   widget=forms.TextInput(attrs={'class': 'formControl'}), )
    zip_code = forms.CharField(label="Zip Code", min_length=5, max_length=5, required=True,
                                   validators=[validate_zipcodeonly],
                                   widget=forms.TextInput(attrs={'class': 'formControl'}), )
    first_name = forms.CharField(label='First Name', min_length=2, max_length=255, required=True, validators=[valdiate_lettersonly],
                           widget=forms.TextInput(attrs={'class': 'formControl'}), )
    last_name = forms.CharField(label='Last Name', min_length=2, max_length=255, required=True, validators=[valdiate_lettersonly],
                           widget=forms.TextInput(attrs={'class': 'formControl'}), )
    image_file = forms.FileField(label='Select an Image',required=False,validators=[validate_file])

    user = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'id': 'user', 'class': 'formControl', 'type': 'hidden'}), )

    def clean(self):
        email = self.cleaned_data['email']
        user = self.cleaned_data['user']
        if User.objects.filter(email=email).exclude(id = user).exists():
             raise forms.ValidationError("This email is already taken")
        return self.cleaned_data

class RegistrationForm(forms.Form):

    email = forms.CharField(label='Email',max_length=60,min_length=5,required=True)
    phone_number = forms.CharField(label="Phone number", max_length=50, required=True,
                                   validators=[valdiate_numbersonly],
                                   widget=forms.TextInput(attrs={'class': 'formControl'}), )
    zip_code = forms.CharField(label="Zip Code", min_length=5, max_length=5, required=True,
                                   validators=[validate_zipcodeonly],
                                   widget=forms.TextInput(attrs={'class': 'formControl'}), )
    first_name = forms.CharField(label='Name', max_length=255, required=True, validators=[valdiate_lettersonly],
                           widget=forms.TextInput(attrs={'class': 'formControl'}), )
    last_name = forms.CharField(label='Surname', max_length=255, required=True, validators=[valdiate_lettersonly],
                           widget=forms.TextInput(attrs={'class': 'formControl'}), )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'id': 'id_password', 'class': 'formControl'}),
        required=True
    )

    confirmpassword = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'formControl'}),
        required=True
    )

    # def __init__(self, *args, **kwargs):
    #     super(RegistrationForm, self).__init__(*args, **kwargs)
    #     if 'form' in kwargs:
    #         if 'is_social' in kwargs['data']:
    #             self.fields['password'].required = False
    #             self.fields['confirmpassword'].required = False
    #             self.fields['phone_number'].required = False

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

class ResetForm(forms.Form):
    email = forms.CharField(label='Email', max_length=255, required=True,
                            widget=forms.TextInput(attrs={'class': 'formControl'}), )

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if not User.objects.filter(email=email).exists():
            not_exists = 'The email account that you tried to reach does not exist'
            raise forms.ValidationError(not_exists, code='not_exists')
        return email


class ChangePasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
        'password_length': "Password too short.",
    }

    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'formControl'}),
                               required=True)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput(attrs={'class': 'formControl'}), required=True)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 2:  # must be changed
            raise forms.ValidationError(
                self.error_messages['password_length'],
                code='password_length',
            )
        return password

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

class BillingForm(forms.Form):

    first_name = forms.CharField(label='Cardholder name', max_length=255, required=True, validators=[valdiate_lettersonly],
                           widget=forms.TextInput(attrs={'class': 'formControl'}), )

    card_number = forms.CharField(label="Card Number", max_length=16,min_length=15, required=True,
                               validators=[validate_billing_numbersonly],
                               widget=forms.TextInput(attrs={'class': 'formControl','autocomplete':'off'}), )

    cvv = forms.CharField(label="Cvv", max_length=4,min_length=3, required=True,
                               validators=[validate_billing_numbersonly],
                               widget=forms.TextInput(attrs={'class': 'formControl','autocomplete':'off'}), )

    month = forms.CharField(label="Month", max_length=2,min_length=2,required=True,
                               validators=[validate_month],
                               widget=forms.TextInput(attrs={'class': 'formControl','autocomplete':'off'}), )

    year = forms.CharField(label="Year", max_length=4,min_length=2, required=True,
                               validators=[validate_year],
                               widget=forms.TextInput(attrs={'class': 'formControl','autocomplete':'off'}), )
