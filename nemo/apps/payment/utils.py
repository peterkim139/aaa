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



def cancel_transaction(price,orderer):

    result = braintree.Transaction.sale({
        "amount": price,
        "merchant_account_id": orderer.merchant_id,
        "customer_id": settings.CUSTOMER_ID,
        "options": {
        "submit_for_settlement": True,
        "hold_in_escrow": False,
        },
        "service_fee_amount": 0
    })

    return  result

def seller_approve(requests,current_user,customer_id,fee):

    result = braintree.Transaction.sale({
        "amount": requests.price,
        "merchant_account_id": current_user.merchant_id,
        "customer_id": customer_id,
        "options": {
        "submit_for_settlement": True,
        "hold_in_escrow": True,
        },
        "service_fee_amount": fee
    })

    return result