import braintree
from django.conf import settings


def payment_connection():

    braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id = settings.BRAINTREE_MERCHANT_ID,
                                  public_key = settings.BRAINTREE_PUBLIC_KEY,
                                  private_key = settings.BRAINTREE_PRIVATE_KEY)
