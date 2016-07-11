from django import template
from django.core.cache import cache
from accounts.forms import RegistrationForm
register = template.Library()


@register.assignment_tag
def registration_form():

    registartion_error = cache.get('registartion_error')

    if registartion_error:
        cache.delete('registartion_error')
        return registartion_error
    else:
        return RegistrationForm()




