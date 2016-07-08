from django.contrib.auth.forms import AuthenticationForm as CoreAuthenticationForm
from accounts.models import User
from django import forms
from django.forms import extras
from django.utils.safestring import mark_safe
import datetime
from accounts.validations import *


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

    email = forms.CharField(label='Email', max_length=60, min_length=5, required=True, validators=[validate_email])
    first_name = forms.CharField(label='Name', max_length=255, required=True, validators=[validate_lettersonly],
                                 widget=forms.TextInput(attrs={'class': 'formControl'}), )
    last_name = forms.CharField(label='Surname', max_length=255, required=True, validators=[validate_lettersonly],
                                widget=forms.TextInput(attrs={'class': 'formControl'}), )


class ProfileForm(forms.Form):

    def __init__(self, *args, **kwargs):
            super(ProfileForm, self).__init__(*args, **kwargs)
            self.fields['image_file'].widget.attrs.update({'class': 'formControl'})

    email = forms.CharField(label='Email', max_length=60, min_length=5, required=True, widget=forms.TextInput(attrs={'class': 'formControl'}), validators=[validate_email])
    phone_number = forms.CharField(label="Phone Number - Numbers only", min_length=10, max_length=10, required=True,
                                   validators=[validate_numbersonly],
                                   widget=forms.TextInput(attrs={'class': 'formControl'}), )
    zip_code = forms.CharField(label="Zip Code", min_length=5, max_length=5, required=True,
                               validators=[validate_zipcode],
                               widget=forms.TextInput(attrs={'class': 'formControl'}), )
    first_name = forms.CharField(label='First Name', min_length=2, max_length=255, required=True, validators=[validate_lettersonly],
                                 widget=forms.TextInput(attrs={'class': 'formControl'}), )
    last_name = forms.CharField(label='Last Name', min_length=2, max_length=255, required=True, validators=[validate_lettersonly],
                                widget=forms.TextInput(attrs={'class': 'formControl'}), )
    image_file = forms.FileField(label='Select an Image', required=False, validators=[validate_file])

    user = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'id': 'user', 'class': 'formControl', 'type': 'hidden'}), )

    def clean(self):
        email = self.cleaned_data['email']
        user = self.cleaned_data['user']
        phone_number = self.cleaned_data['phone_number']
        if User.objects.filter(email=email).exclude(id=user).exists():
            raise forms.ValidationError("This email is already taken")
        if User.objects.filter(phone_number=phone_number).exclude(id=user).exists():
            raise forms.ValidationError("This phone number is already taken")
        return self.cleaned_data


class RegistrationForm(forms.Form):


    def __init__(self, *args, **kwargs):
            super(RegistrationForm, self).__init__(*args, **kwargs)
            self.fields['birthdate'].widget.attrs.update({'class': 'formControl'})


    MONTHS = {
        '':('Month'),
        1:('January'), 2:('February'), 3:('March'), 4:('April'),
        5:('May'), 6:('June'), 7:('July'), 8:('August'),
        9:('September'), 10:('October'), 11:('November'), 12:('December')
    }

    first_name = forms.CharField(label='FIRST NAME', max_length=255, required=True, validators=[validate_lettersonly],
                                 widget=forms.TextInput(attrs={'class': 'formControl'}), )
    last_name = forms.CharField(label='Last NAME', max_length=255, required=True, validators=[validate_lettersonly],
                                widget=forms.TextInput(attrs={'class': 'formControl'}), )

    email = forms.CharField(label='Email', max_length=60, min_length=5, required=True,
                            validators=[validate_email], widget=forms.TextInput(attrs={'class': 'formControl'}))

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'id': 'id_password_reg', 'class': 'formControl'}),
        required=True
    )

    zip_code = forms.CharField(label="Zip Code", min_length=5, max_length=5, required=True,
                               validators=[validate_zipcode],
                               widget=forms.TextInput(attrs={'class': 'formControl'}), )



    birthdate = forms.DateField(label="BIRTHDATE:(To verify you are over 18 years old)",widget=extras.SelectDateWidget(years=range(1998, 1923, -1), months=MONTHS))

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
            error = mark_safe("This email is already taken <a class='txtBtn popupBtn forgot_tub' href='#forgot_popup'>Forgot your password? Click here.</a>")
            raise forms.ValidationError(error)
        return email



    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:  # must be changed
            raise forms.ValidationError("Password too short.")
        return password



class ResetForm(forms.Form):
    email = forms.CharField(label='Email', max_length=255, required=True, validators=[validate_email],
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

    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'id': 'id_password_change','class': 'formControl'}),
                               required=True)
    password2 = forms.CharField(label="Repeat Password:",
                                widget=forms.PasswordInput(attrs={'class': 'formControl'}), required=True)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:  # must be changed
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
        return password

class BillingForm(forms.Form):

    def __init__(self, *args, **kwargs):
            super(BillingForm, self).__init__(*args, **kwargs)

    first_name = forms.CharField(label='Cardholder name', max_length=255, required=True, validators=[validate_lettersonly],
                                 widget=forms.TextInput(attrs={'class': 'formControl'}), )

    card_number = forms.CharField(label="Card Number", max_length=16, min_length=15, required=True,
                                  validators=[validate_numbersonly],
                                  widget=forms.TextInput(attrs={'class': 'formControl', 'autocomplete': 'off'}), )

    cvv = forms.CharField(label="Cvv", max_length=4, min_length=3, required=True,
                          validators=[validate_numbersonly],
                          widget=forms.TextInput(attrs={'class': 'formControl', 'autocomplete': 'off'}), )



    year = forms.CharField(label="Year", max_length=4, min_length=2, required=True,
                           validators=[validate_year],
                           widget=forms.TextInput(attrs={'class': 'formControl', 'autocomplete': 'off'}), )

    month = forms.CharField(label="Month", max_length=2, min_length=2, required=True,
                            validators=[validate_month],
                            widget=forms.TextInput(attrs={'class': 'formControl', ' autocomplete': 'off'}), )


    def clean_month(self):

        month = self.cleaned_data.get('month')
        year = self.cleaned_data.get('year')
        now = datetime.datetime.now()
        if year is not None:
            if now.year == int(year) and int(month) < now.month:
                raise forms.ValidationError("Invalid Month")
            return month