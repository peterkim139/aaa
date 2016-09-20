from django import template
from django.core.cache import cache
from accounts.forms import BillingForm
register = template.Library()


@register.assignment_tag
def billing_form():

    billing_error = cache.get('billing_error')

    if billing_error:
        cache.delete('billing_error')
        return billing_error
    else:
        return BillingForm()

