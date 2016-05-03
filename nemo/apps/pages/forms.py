import re

from django import forms
from category.models import SubCategory
from django.forms import extras
from django.core.exceptions import ValidationError
import datetime

def validate_lettersonly(value):
    if not re.match("^[A-Za-z ]*$", value):
        raise ValidationError('Name field should contain only letters')

def has_numbers(value):
    if not any(char.isdigit() for char in value):
        raise ValidationError('Field should contain at least 1 digit')

def validate_numbersonly(value):
    if not re.match("^[0-9]*$", value):
        raise ValidationError('Field should contain only number')

def validate_month(value):
    if not re.match("^[0-9]*$", value) or (int(value) < 1 or int(value) > 12):
        raise ValidationError('Month value can be from 01 to 12')

def validate_year(value):
    if not re.match("^[0-9]*$", value) or ( int(value) > 2050 or int(value) < datetime.datetime.now().year):
        raise ValidationError('Please enter a correct year')


class RentForm(forms.Form):

      card_number = forms.CharField(label="Card Number", max_length=16,min_length=15, required=True,
                                   validators=[validate_numbersonly],
                                   widget=forms.TextInput(attrs={'class': '','autocomplete':'off'}), )

      cvv = forms.CharField(label="Cvv", max_length=4,min_length=3, required=True,
                                   validators=[validate_numbersonly],
                                   widget=forms.TextInput(attrs={'class': '','autocomplete':'off'}), )

      month = forms.CharField(label="Month", max_length=2,min_length=2,required=True,
                                   validators=[validate_month],
                                   widget=forms.TextInput(attrs={'class': '','autocomplete':'off'}), )

      year = forms.CharField(label="Year", max_length=4,min_length=4, required=True,
                                   validators=[validate_year],
                                   widget=forms.TextInput(attrs={'class': '','autocomplete':'off'}), )


class AddListingForm(forms.Form):

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

    street_address = forms.CharField(label='Address', max_length=255, required=True,validators=[has_numbers],
                           widget=forms.TextInput(attrs={'id':'street_address','class': 'formControl'}), )
    city = forms.CharField(label='City', max_length=255, required=True, validators=[validate_lettersonly],
                           widget=forms.TextInput(attrs={'id': 'city','class': 'formControl'}), )

    state = forms.CharField(max_length=2,
                widget=forms.Select(choices=CHOICES),required=True)

    postal_code = forms.CharField(label="Zip Code", max_length=5,min_length=5, required=True,
                                   validators=[validate_numbersonly],
                                   widget=forms.TextInput(attrs={'id':'postal_code', 'class': 'formControl'}), )

    name = forms.CharField(label='Title', max_length=255, required=True,
                           widget=forms.TextInput(attrs={'id': 'name','class': 'formControl'}), )
    subcategory = forms.ModelChoiceField(label='Category',queryset=SubCategory.objects.all())
    description = forms.CharField(label='Description', required='True', widget=forms.Textarea(attrs={'id':'description', 'class': 'formControl'}))
    price = forms.CharField(label="Price", required=True, max_length=3,
                                   validators=[validate_numbersonly],
                                   widget=forms.TextInput(attrs={'id':'price', 'class': '','autocomplete':'off'}), )
    image_file = forms.CharField(required=True,
                                 widget=forms.TextInput(attrs={'id':'filename', 'class': 'formControl', 'type': 'hidden'}), )

    latitude = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'id': 'latitudes', 'class': 'formControl', 'type': 'hidden'}), )
    longitude = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'id': 'longitudes', 'class': 'formControl', 'type': 'hidden'}), )
