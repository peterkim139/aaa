from django import template
from django.core.cache import cache
from accounts.forms import ResetForm
register = template.Library()


@register.simple_tag
def forgot_form():

    forgot_error = cache.get('forgot_error')

    if forgot_error:
        cache.delete('forgot_error')
        return forgot_error
    else:
        return ResetForm()