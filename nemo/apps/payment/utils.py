import braintree
import logging
import mandrill
from decimal import Decimal
from django.template import Context
from django.template import loader
from django.conf import settings
from django.contrib import messages

mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

def payment_connection():

    braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id = settings.BRAINTREE_MERCHANT_ID,
                                  public_key = settings.BRAINTREE_PUBLIC_KEY,
                                  private_key = settings.BRAINTREE_PRIVATE_KEY)


def error_logging(e):
    logger = logging.getLogger('nemo')
    logger.error(e)


def new_rent_mail(request, email, client,item,seler,id):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'You have received a rental request!'
    from_email = settings.AUTO_REPLY
    to = [email]
    context = Context({
        'client': client,
        'item': item,
        'id':id,
        'seler': seler,
        'site_name': settings.ADMIN_EMAIL,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('payment/emails/new_rent.html', context)
    message = {
        'subject' : subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'NEMO',
        'html':content,
        'to': [{'email': email,
             'name': seler,
             'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')

def expired_rent_client(info):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)
    rent_date = info.rent_date.strftime('%Y-%m-%d')
    start_date = info.start_date.strftime('%Y-%m-%d')
    subject = 'Rent request has been expired'
    from_email = settings.AUTO_REPLY
    to = [info.user.email]
    context = Context({
        'client': info.user.first_name,
        'item': info.param.name,
        'seller': info.owner.first_name,
        'site_name': settings.ADMIN_EMAIL,
        'description':info.param.description,
        'price':str(info.price),
        'start_date':str(start_date),
        'rent_date':str(rent_date),
    })
    content = loader.render_to_string('payment/emails/expired_rent_client.html', context)
    message = {
        'subject' : subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'NEMO',
        'html':content,
        'to': [{'email': info.user.email,
             'name': info.user.first_name,
             'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')

def expired_rent_seller(info):

    rent_date = info.rent_date.strftime('%Y-%m-%d')
    start_date = info.start_date.strftime('%Y-%m-%d')
    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Rent request has been expired'
    from_email = settings.AUTO_REPLY
    to = [info.owner.email]
    context = Context({
        'client': info.user.first_name,
        'item': info.param.name,
        'seller': info.owner.first_name,
        'site_name': settings.ADMIN_EMAIL,
        'description':info.param.description,
        'price':str(info.price),
        'start_date':str(start_date),
        'rent_date':str(rent_date),
    })
    content = loader.render_to_string('payment/emails/expired_rent_seller.html', context)
    message = {
        'subject' : subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'NEMO',
        'html':content,
        'to': [{'email': info.owner.email,
             'name':  info.owner.first_name,
             'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')


def admin_cancel_rent_to_seller(info):

    rent_date = info.rent_date.strftime('%Y-%m-%d')
    start_date = info.start_date.strftime('%Y-%m-%d')
    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Rent request has been canceled by website administrator'
    from_email = settings.AUTO_REPLY
    to = [info.owner.email]
    context = Context({
        'client': info.user.first_name,
        'item': info.param.name,
        'seller': info.owner.first_name,
        'site_name': settings.ADMIN_EMAIL,
        'description':info.param.description,
        'price':str(info.price),
        'start_date':str(start_date),
        'rent_date':str(rent_date),
    })
    content = loader.render_to_string('payment/emails/admin_cancel_rent_to_seller.html', context)
    message = {
        'subject' : subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'NEMO',
        'html':content,
        'to': [{'email': info.owner.email,
             'name':  info.owner.first_name,
             'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')

def admin_cancel_rent_to_client(info):

    rent_date = info.rent_date.strftime('%Y-%m-%d')
    start_date = info.start_date.strftime('%Y-%m-%d')
    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Rent request has been expired'
    from_email = settings.AUTO_REPLY
    to = [info.owner.email]
    context = Context({
        'client': info.user.first_name,
        'item': info.param.name,
        'seller': info.owner.first_name,
        'site_name': settings.ADMIN_EMAIL,
        'description':info.param.description,
        'price':str(info.price),
        'start_date':str(start_date),
        'rent_date':str(rent_date),
    })
    content = loader.render_to_string('payment/emails/admin_cancel_rent_to_client.html', context)
    message = {
        'subject' : subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'NEMO',
        'html':content,
        'to': [{'email': info.owner.email,
             'name':  info.owner.first_name,
             'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')

def reminder_rent_client(info):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)
    subject = 'The rental date of your ' + info.param.name + ' starts tomorrow, please arrange for pickup soon'
    from_email = settings.AUTO_REPLY
    to = [info.user.email]
    context = Context({
        'client': info.user.first_name,
        'item': info.param.name,
        'seller': info.owner.first_name,
        'seller_fullName':info.owner.first_name + ' ' + info.owner.last_name,
        'site_name': settings.ADMIN_EMAIL,
    })
    content = loader.render_to_string('payment/emails/reminder_rent_client.html', context)
    message = {
        'subject' : subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'NEMO',
        'html':content,
        'to': [{'email':info.user.email,
             'name': info.user.first_name,
             'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')

def reminder_rent_seller(info):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Rent for your ' + info.param.name + ' starts tomorrow, please arrange for pickup soon'
    from_email = settings.AUTO_REPLY
    to = [info.owner.email]
    context = Context({
        'client': info.user.first_name,
        'client_fullname':info.user.first_name + ' ' + info.user.last_name,
        'item': info.param.name,
        'seller': info.owner.first_name,
        'site_name': settings.ADMIN_EMAIL,
    })
    content = loader.render_to_string('payment/emails/reminder_rent_seller.html', context)
    message = {
        'subject' : subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'NEMO',
        'html':content,
        'to': [{'email': info.owner.email,
             'name':  info.owner.first_name,
             'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')


def seller_transaction_email(info):

    rent_date = info.rent_date.strftime('%Y-%m-%d')
    start_date = info.start_date.strftime('%Y-%m-%d')
    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)
    TWOPLACES = Decimal(10) ** -2
    fee = Decimal(info.price)*Decimal(12.9/100)+Decimal('0.30')
    fee = fee.quantize(TWOPLACES)
    total = Decimal(info.price)-Decimal(fee)
    subject = 'A new payment has been credited to your account!'
    from_email = settings.AUTO_REPLY
    to = [info.owner.email]
    context = Context({
        'client': info.user.first_name,
        'item': info.param.name,
        'seller': info.owner.first_name,
        'fee' : str(fee),
        'total':str(total),
        'site_name': settings.ADMIN_EMAIL,
        'price':str(info.price),
        'start_date':str(start_date),
        'rent_date':str(rent_date),
    })
    content = loader.render_to_string('payment/emails/seller_transaction_email.html', context)
    message = {
        'subject' : subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'NEMO',
        'html':content,
        'to': [{'email': info.owner.email,
             'name':  info.owner.first_name,
             'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')

def return_rent_client(info):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Your rental of the ' + info.param.name + ' ends tomorrow, please remember to return the item to the owner'
    from_email = settings.AUTO_REPLY
    to = [info.user.email]
    context = Context({
        'client': info.user.first_name,
        'item': info.param.name,
        'seller': info.owner.first_name,
        'site_name': settings.ADMIN_EMAIL,
    })
    content = loader.render_to_string('payment/emails/return_rent_client.html', context)
    message = {
        'subject' : subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'NEMO',
        'html':content,
        'to': [{'email':info.user.email,
             'name': info.user.first_name,
             'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')

def show_errors(request,result):
    if type(result) is str:
        messages.error(request, result)
    else:
        for error in result.errors.deep_errors:
            error_message = error.message
        messages.error(request, error_message)
