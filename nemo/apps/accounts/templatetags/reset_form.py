from django import template
from django.core.cache import cache
from accounts.forms import ChangePasswordForm
register = template.Library()


@register.assignment_tag
def reset_form():

    reset_error = cache.get('reset_error')

    if reset_error:
        cache.delete('reset_error')
        return reset_error
    else:
        return ChangePasswordForm()