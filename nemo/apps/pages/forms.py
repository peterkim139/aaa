from category.models import SubCategory
from .models import Message
from django import forms
from accounts.validations import *



class RentForm(forms.Form):

    card_number = forms.CharField(label="Card Number", max_length=16, min_length=15, required=True,
                                  validators=[validate_numbersonly],
                                  widget=forms.TextInput(attrs={'class': 'formControl', 'autocomplete': 'off'}), )

    cvv = forms.CharField(label="Cvv", max_length=4, min_length=3, required=True,
                          validators=[validate_numbersonly],
                          widget=forms.TextInput(attrs={'class': 'formControl', 'autocomplete': 'off'}), )

    month = forms.CharField(label="Month", max_length=2, min_length=2, required=True,
                            validators=[validate_month],
                            widget=forms.TextInput(attrs={'class': 'formControl', 'autocomplete': 'off'}), )

    year = forms.CharField(label="Year", max_length=4, min_length=4, required=True,
                           validators=[validate_year],
                           widget=forms.TextInput(attrs={'class': 'formControl', 'autocomplete': 'off'}), )


class AddListingForm(forms.Form):

    CHOICES = (
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
        ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District Of Columbia'), ('FL', 'Florida'),
        ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'),
        ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'),
        ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
        ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'),
        ('OH', 'New Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
        ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'),
        ('WY', 'Wyoming')
    )

    street_address = forms.CharField(label='Address', max_length=255, required=True, validators=[has_numbers],
                                     widget=forms.TextInput(attrs={'id': 'street_address', 'class': 'formControl'}), )
    city = forms.CharField(label='City', max_length=255, required=True, validators=[validate_lettersonly],
                           widget=forms.TextInput(attrs={'id': 'city', 'class': 'formControl'}), )

    state = forms.CharField(max_length=2,
                            widget=forms.Select(choices=CHOICES, attrs={'class': 'formControl'}), required=True)

    postal_code = forms.CharField(label="Zip Code", max_length=5, min_length=5, required=True,
                                  validators=[validate_numbersonly],
                                  widget=forms.TextInput(attrs={'id': 'postal_code', 'class': 'formControl'}), )

    name = forms.CharField(label='Title', max_length=255, required=True,
                           widget=forms.TextInput(attrs={'id': 'name', 'class': 'formControl'}), )
    subcategory = forms.ModelChoiceField(label='Category', queryset=SubCategory.objects.all(), widget=forms.Select(attrs={'class': 'formControl'}))
    description = forms.CharField(label='Description', required='True', widget=forms.Textarea(attrs={'id': 'description', 'class': 'formControl'}))
    price = forms.CharField(label="Price", required=True, max_length=6,
                            validators=[validate_price],
                            widget=forms.TextInput(attrs={'id': 'price', 'class': 'formControl', 'autocomplete': 'off'}),)
    image_file = forms.CharField(required=True,
                                 widget=forms.TextInput(attrs={'id': 'filename', 'class': 'formControl', 'type': 'hidden'}), )
    latitude = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'id': 'latitudes', 'class': 'formControl', 'type': 'hidden'}), )
    longitude = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'id': 'longitudes', 'class': 'formControl', 'type': 'hidden'}), )
    street = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'id': 'street', 'class': 'formControl', 'type': 'hidden'}), )
    item_id = forms.CharField(required=False,
                                widget=forms.TextInput(attrs={'id': 'item_id', 'class': 'formControl', 'type': 'hidden'}), )

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            "message",
        ]

class SupportForm(forms.Form):

    email = forms.CharField(label='Email', max_length=60, min_length=5, required=True, widget=forms.TextInput(attrs={'class': 'formControl'}), validators=[validate_email])
    name = forms.CharField(label='Name', min_length=2, max_length=255, required=True,
                           validators=[validate_lettersonly],
                           widget=forms.TextInput(attrs={'class': 'formControl'}), )
    comments = forms.CharField(label='Message', required='True', widget=forms.Textarea(attrs={'id': 'comments', 'class': 'formControl'}))

