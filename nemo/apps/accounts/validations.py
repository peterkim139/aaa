import re
import datetime
from django.core.exceptions import ValidationError
from django.conf import settings
from django import forms


def validate_file(value):
    content_type = value.content_type.split('/')[0]
    if content_type in settings.CONTENT_TYPES:
        if value._size > int(settings.MAX_UPLOAD_SIZE):
            raise forms.ValidationError('Please keep file size under 2 Mb')
    else:
        raise forms.ValidationError('Only .jpg/jpeg/png/gif files allowed.')


def validate_lettersonly(value):
    if not re.match("^[A-Za-z ]*$", value):
        raise ValidationError('Name field should contain only letters')


def validate_numbersonly(value):
    if not re.match("^[0-9]*$", value):
        raise ValidationError('Field should contain only numbers')

def validate_zipcode(value):

     if not re.match("^[0-9]*$", value) or len(value) != 5:
        raise ValidationError('Field should contain only 5 numbers')


def validate_email(value):

    if not re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", value):
        raise ValidationError('Please enter correct email')

def validate_month(value):
    if not re.match("^[0-9]*$", value) or (int(value) < 1 or int(value) > 12):
        raise ValidationError('Month value can be from 01 to 12')


def validate_year(value):

    if not re.match("^[0-9]*$", value) or (int(value) > 2050 or int(value) < datetime.datetime.now().year):
        raise ValidationError('Please enter a correct year')


def validate_price(value):

    if not (float(value) >= 1 or float(value) <= 999.99):
        raise ValidationError('Price field can accept values from 1 to 999.99 only.')


def has_numbers(value):
    if not any(char.isdigit() for char in value):
        raise ValidationError('Field should contain at least 1 digit')


def validate_length(value):
    if len(value) != 4:
        raise ValidationError('Field should contain Social Security Number last 4 digits')
