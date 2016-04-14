import re

from django import forms
from django.forms import extras
from django.core.exceptions import ValidationError
import datetime

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