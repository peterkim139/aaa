import re

from django import forms
from django.forms import extras
from django.core.exceptions import ValidationError

def valdiate_lettersonly(value):
    if not re.match("^[A-Za-z ]*$", value):
        raise ValidationError('Name field should contain only letters')


def valdiate_numbersonly(value):
    if not re.match("^[0-9 \+\-\(\)]*$", value):
        raise ValidationError('Field should contain only number')

def has_numbers(value):
    if not any(char.isdigit() for char in value):
        raise ValidationError('Field should contain at least 1 digit')

def valdiate_length(value):
    if len(value) != 4:
        raise ValidationError('Field should contain Social Security Number last 4 digits')

class RentForm(forms.Form):

      card_number = forms.CharField(label="Card Number", max_length=16,min_length=15, required=True,
                                   validators=[valdiate_numbersonly],
                                   widget=forms.TextInput(attrs={'class': '','autocomplete':'off'}), )

      cvv = forms.CharField(label="Cvv", max_length=4,min_length=3, required=True,
                                   validators=[valdiate_numbersonly],
                                   widget=forms.TextInput(attrs={'class': '','autocomplete':'off'}), )

      month = forms.CharField(label="Month", max_length=2,min_length=2,required=True,
                                   validators=[valdiate_numbersonly],
                                   widget=forms.TextInput(attrs={'class': '','autocomplete':'off'}), )

      year = forms.CharField(label="Year", max_length=4,min_length=2, required=True,
                                   validators=[valdiate_numbersonly],
                                   widget=forms.TextInput(attrs={'class': '','autocomplete':'off'}), )