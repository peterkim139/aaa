import braintree
import logging
from django.conf import settings
from django.contrib import messages


def payment_connection():

    braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id = settings.BRAINTREE_MERCHANT_ID,
                                  public_key = settings.BRAINTREE_PUBLIC_KEY,
                                  private_key = settings.BRAINTREE_PRIVATE_KEY)


def error_logging(e):
    logger = logging.getLogger('nemo')
    logger.error(e)



def show_errors(request,result):
    if type(result) is str:
        messages.error(request, result)
    else:
        for error in result.errors.deep_errors:
            error_message = error.message
        messages.error(request, error_message)
