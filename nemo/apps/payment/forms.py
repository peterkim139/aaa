import re
from django import forms
from django.forms import extras
from accounts.validations import *
from accounts.models import User


class ConnectForm(forms.Form):

    def __init__(self, *args, **kwargs):
            super(ConnectForm, self).__init__(*args, **kwargs)
            self.fields['region'].widget.attrs.update({'class': 'formControl'})
            self.fields['birthdate'].widget.attrs.update({'class': 'formControl'})

    CHOICES = (('', ''),
               ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'),
               ('AR', 'Arkansas'), ('CA', 'California'),
               ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),
               ('DC', 'District Of Columbia'), ('FL', 'Florida'),
               ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
               ('IL', 'Illinois'), ('IN', 'Indiana'),
               ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'),
               ('LA', 'Louisiana'), ('ME', 'Maine'),
               ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'),
               ('MN', 'Minnesota'), ('MS', 'Mississippi'),
               ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'),
               ('NV', 'Nevada'), ('NH', 'New Hampshire'),
               ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
               ('NC', 'North Carolina'), ('ND', 'North Dakota'),
               ('OH', 'New Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'),
               ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
               ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'),
               ('WY', 'Wyoming')
              )
    phone_number = forms.CharField(label="Phone number", min_length=10, max_length=10, required=True,
                                   validators=[validate_numbersonly],
                                   widget=forms.TextInput(attrs={'class': 'formControl'}), )

    birthdate = forms.DateField(widget=extras.SelectDateWidget(years=range(1998, 1923, -1)), required=True)

    account_number = forms.CharField(label="Account Number", max_length=16, required=True,
                                     validators=[validate_numbersonly],
                                     widget=forms.TextInput(attrs={'class': 'formControl'}), )

    routing_number = forms.CharField(label="Routing Number", max_length=9, min_length=9, required=True,
                                     validators=[validate_numbersonly],
                                     widget=forms.TextInput(attrs={'class': 'formControl'}), )

    street_address = forms.CharField(label='Street Adress', max_length=255, required=True, validators=[has_numbers],
                                     widget=forms.TextInput(attrs={'class': 'formControl'}), )

    locality = forms.CharField(label='City', max_length=255, required=True, validators=[validate_lettersonly],
                               widget=forms.TextInput(attrs={'class': 'formControl'}), )

    postal_code = forms.CharField(label="Postal Code", max_length=5, min_length=5, required=True,
                                  validators=[validate_zipcode],
                                  widget=forms.TextInput(attrs={'class': 'formControl'}), )

    region = forms.CharField(label='State', max_length=2,
                             widget=forms.Select(choices=CHOICES), required=True)

    terms = forms.BooleanField(
        error_messages={'required': 'You must accept the terms and conditions'},
        widget=forms.CheckboxInput(attrs={'class': 'chboxRadio', 'id': 'TermCheckBox'}),
    )


class RentForm(forms.Form):

    start_date = forms.CharField(label='Start Date', max_length=255, required=True,
                                 widget=forms.TextInput(attrs={'class': '', 'type': 'hidden'}), )

    rent_date = forms.CharField(label='Rent Date', max_length=255, required=True,
                                widget=forms.TextInput(attrs={'class': '', 'type': 'hidden'}), )
