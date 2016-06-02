import re

from django import forms
from django.forms import extras
from django.core.exceptions import ValidationError
import datetime

def validate_lettersonly(value):
    if not re.match("^[A-Za-z ]*$", value):
        raise ValidationError('Name field should contain only letters')

def validate_numbersonly(value):
    if not re.match("^[0-9]*$", value):
        raise ValidationError('Field should contain only numbers')

def validate_phone(value):
    if not re.match("^[0-9 \+\-\(\)]*$", value):
        raise ValidationError('Field should contain only numbers')

def validate_month(value):
    if not re.match("^[0-9]*$", value) or (int(value) < 1 or int(value) > 12):
        raise ValidationError('Month value can be from 01 to 12')

def validate_year(value):

    if not re.match("^[0-9]*$", value) or ( int(value) > 2050 or int(value) < datetime.datetime.now().year):
        raise ValidationError('Please enter a correct year')

def has_numbers(value):
    if not any(char.isdigit() for char in value):
        raise ValidationError('Field should contain at least 1 digit')

def validate_length(value):
    if len(value) != 4:
        raise ValidationError('Field should contain Social Security Number last 4 digits')


class ConnectForm(forms.Form):


    CHOICES = (('', ''),
        ('AL', 'Alabama'),('AK', 'Alaska'),('AZ', 'Arizona'),('AR', 'Arkansas'),('CA', 'California'),
        ('CO', 'Colorado'),('CT', 'Connecticut'),('DE', 'Delaware'),('DC', 'District Of Columbia'),('FL', 'Florida'),
        ('GA', 'Georgia'),('HI', 'Hawaii'),('ID', 'Idaho'),('IL', 'Illinois'),('IN', 'Indiana'),
        ('IA', 'Iowa'),('KS', 'Kansas'),('KY', 'Kentucky'),('LA', 'Louisiana'),('ME', 'Maine'),
        ('MD', 'Maryland'),('MA', 'Massachusetts'),('MI', 'Michigan'),('MN', 'Minnesota'),('MS', 'Mississippi'),
        ('MO', 'Missouri'),('MT', 'Montana'),('NE', 'Nebraska'),('NV', 'Nevada'),('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'),('NM', 'New Mexico'),('NY', 'New York'),('NC', 'North Carolina'),('ND', 'North Dakota'),
        ('OH', 'New Ohio'),('OK', 'Oklahoma'),('OR', 'Oregon'),('PA', 'Pennsylvania'),('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),('SD', 'South Dakota'),('TN', 'Tennessee'),('TX', 'Texas'),('UT', 'Utah'),
        ('VT', 'Vermont'),('VA', 'Virginia'),('WA', 'Washington'),('WV', 'West Virginia'),('WI', 'Wisconsin'),
        ('WY', 'Wyoming')
    )
    phone_number = forms.CharField(label="Phone number", max_length=15, required=True,
                                   validators=[validate_phone],
                                   widget=forms.TextInput(attrs={'class': 'formControl'}), )

    birthdate = forms.DateField(widget = extras.SelectDateWidget(years = range(1998, 1923, -1)),required=True)

    account_number = forms.CharField(label="Account Number", max_length=16, required=True,
                                   validators=[validate_numbersonly],
                                   widget=forms.TextInput(attrs={'class': 'formControl'}), )

    routing_number = forms.CharField(label="Routing Number", max_length=9,min_length=9, required=True,
                                   validators=[validate_numbersonly],
                                   widget=forms.TextInput(attrs={'class': 'formControl'}), )

    street_address = forms.CharField(label='Street Adress', max_length=255, required=True,validators=[has_numbers],
                           widget=forms.TextInput(attrs={'class': 'formControl'}), )

    locality = forms.CharField(label='Locality', max_length=255, required=True, validators=[validate_lettersonly],
                           widget=forms.TextInput(attrs={'class': 'formControl'}), )

    postal_code = forms.CharField(label="Postal Code", max_length=9,min_length=5, required=True,
                                   validators=[validate_numbersonly],
                                   widget=forms.TextInput(attrs={'class': 'formControl'}), )

    region = forms.CharField(max_length=2,
                widget=forms.Select(choices=CHOICES),required=True)

    terms = forms.BooleanField(
        error_messages={'required': 'You must accept the terms and conditions'},
        label="Terms and Conditions"
    )

class RentForm(forms.Form):

      card_number = forms.CharField(label="Card Number", max_length=16,min_length=15, required=True,
                                   validators=[validate_numbersonly],
                                   widget=forms.TextInput(attrs={'class': 'formControl','autocomplete':'off'}), )

      cvv = forms.CharField(label="Cvv", max_length=4,min_length=3, required=True,
                                   validators=[validate_numbersonly],
                                   widget=forms.TextInput(attrs={'class': 'formControl','autocomplete':'off'}), )

      month = forms.CharField(label="Month", max_length=2,min_length=2,required=True,
                                   validators=[validate_month],
                                   widget=forms.TextInput(attrs={'class': 'formControl','autocomplete':'off'}), )

      year = forms.CharField(label="Year", max_length=4,min_length=2, required=True,
                                   validators=[validate_year],
                                   widget=forms.TextInput(attrs={'class': 'formControl','autocomplete':'off'}), )

      start_date = forms.CharField(label='Start Date', max_length=255, required=True,
                           widget=forms.TextInput(attrs={'class': '','type': 'hidden'}), )

      rent_date = forms.CharField(label='Rent Date', max_length=255, required=True,
                           widget=forms.TextInput(attrs={'class': '','type': 'hidden'}), )