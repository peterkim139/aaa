import mandrill
import braintree
from decimal import Decimal
from django.template import Context
from django.template import loader
from django.conf import settings

mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

def payment_connection():

    braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id = settings.BRAINTREE_MERCHANT_ID,
                                  public_key = settings.BRAINTREE_PUBLIC_KEY,
                                  private_key = settings.BRAINTREE_PRIVATE_KEY)

def cancel_before_approving(request,email,client,seller):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'The rent request has been cancelled'
    from_email = settings.AUTO_REPLY
    to = [email]
    context = Context({
        'client': client,
        'seller':seller,
        'site_name': settings.ADMIN_EMAIL,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('pages/emails/cancel_before_approving.html', context)
    message = {
        'subject' : subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'Nemo',
        'html':content,
        'to': [{'email': email,
             'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')


def cancel_after_approving(request, email, client,item,seller,amount):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'The rent request has been cancelled'
    from_email = settings.AUTO_REPLY
    to = [email]
    context = Context({
        'client': client,
        'seller':seller,
        'amount' :amount,
        'item' : item,
        'site_name': settings.ADMIN_EMAIL,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('pages/emails/cancel_after_approving.html', context)
    message = {
        'subject' : subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'Nemo',
        'html':content,
        'to': [{'email': email,
             'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')

def refund_price(price):

    TWOPLACES = Decimal(10) ** -2
    list = {}
    if price > 20:
        amount = Decimal(price*100-970)/Decimal(97.1)
        list['amount'] = amount.quantize(TWOPLACES)
        list['credit'] = Decimal(price*50/100).quantize(TWOPLACES)
    else:
        amount = Decimal(price*50+30)/Decimal(97.1)
        list['amount'] = amount.quantize(TWOPLACES)
        list['credit'] = Decimal(price*25/100).quantize(TWOPLACES)

    return list

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

def seller_penalize_email(request,seller,amount,email):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'You have been penalized'
    from_email = settings.AUTO_REPLY
    to = [email]
    context = Context({
        'seller': seller,
        'amount':amount,
        'site_name': settings.ADMIN_EMAIL,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('pages/emails/cancel_before_approving.html', context)
    message = {
        'subject' : subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'Nemo',
        'html':content,
        'to': [{'email': email,
             'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')

def seller_canceled_request_before(request,client,email,item):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Your  request has been cancelled'
    from_email = settings.AUTO_REPLY
    to = [email]
    context = Context({
        'client': client,
        'item':item,
        'site_name': settings.ADMIN_EMAIL,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('pages/emails/seller_canceled_request_before.html', context)
    message = {
        'subject' : subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'Nemo',
        'html':content,
        'to': [{'email': email,
             'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')


def seller_canceled_request_after(request,client,email,item):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Your  request has been cancelled'
    from_email = settings.AUTO_REPLY
    to = [email]
    context = Context({
        'client': client,
        'item':item,
        'site_name': settings.ADMIN_EMAIL,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('pages/emails/seller_canceled_request_after.html', context)
    message = {
        'subject' : subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'Nemo',
        'html':content,
        'to': [{'email': email,
             'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')


def seller_declined_request(request,client,email,item):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Your request has been declined'
    from_email = settings.AUTO_REPLY
    to = [email]
    context = Context({
        'client': client,
        'item':item,
        'site_name': settings.ADMIN_EMAIL,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('pages/emails/seller_declined_request.html', context)
    message = {
        'subject' : subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'Nemo',
        'html':content,
        'to': [{'email': email,
             'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')

def seller_approved_request(request,client,seller,email,item,price):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Your request has been approved'
    from_email = settings.AUTO_REPLY
    to = [email]
    context = Context({
        'client': client,
        'item':item,
        'price':price,
        'seller':seller,
        'site_name': settings.ADMIN_EMAIL,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('pages/emails/seller_declined_request.html', context)
    message = {
        'subject' : subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'Nemo',
        'html':content,
        'to': [{'email': email,
             'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')