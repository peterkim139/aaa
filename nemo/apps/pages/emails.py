import mandrill
from django.template import Context
from django.template import loader
from django.conf import settings


mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)


def cancel_before_approving(request, email, client, seller, item):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'The request for ' + item + ' has been cancelled by your neighbor'
    from_email = settings.AUTO_REPLY
    context = Context({
        'client': client,
        'seller': seller,
        'item': item,
        'site_name': settings.ADMIN_EMAIL,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('pages/emails/cancel_before_approving.html', context)
    message = {
        'subject': subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': from_email,
        'from_name': 'NEMO',
        'html': content,
        'to': [{'email': email,
                'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')


def cancel_after_approving(request, email, client, item, seller, amount):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'The request for ' + item + ' has been cancelled'
    from_email = settings.AUTO_REPLY
    context = Context({
        'client': client,
        'seller': seller,
        'amount': amount,
        'item': item,
        'site_name': settings.ADMIN_EMAIL,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('pages/emails/cancel_after_approving.html', context)
    message = {
        'subject': subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': from_email,
        'from_name': 'NEMO',
        'html': content,
        'to': [{'email': email,
                'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')


def seller_penalize_email(request, seller, item, amount, email):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Your case has been resolved'
    from_email = settings.AUTO_REPLY

    context = Context({
        'seller': seller,
        'amount': amount,
        'item': item,
        'site_name': settings.ADMIN_EMAIL,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('pages/emails/seller_penalize_email.html', context)
    message = {
        'subject': subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': from_email,
        'from_name': 'NEMO',
        'html': content,
        'to': [{'email': email,
                'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')


def seller_canceled_request_before(request, client, email, item):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Your  request for ' + item + ' has been cancelled by the owner'
    from_email = settings.AUTO_REPLY
    context = Context({
        'client': client,
        'item': item,
        'site_name': settings.ADMIN_EMAIL,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('pages/emails/seller_canceled_request_before.html', context)
    message = {
        'subject': subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': from_email,
        'from_name': 'NEMO',
        'html': content,
        'to': [{'email': email,
                'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')


def seller_canceled_request_after(request, client, email, item):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Your request for ' + item + ' has been cancelled by the owner and we have given a $2 credit to use on NEMO'
    from_email = settings.AUTO_REPLY
    context = Context({
        'client': client,
        'item': item,
        'site_name': settings.ADMIN_EMAIL,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('pages/emails/seller_canceled_request_after.html', context)
    message = {
        'subject': subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': from_email,
        'from_name': 'NEMO',
        'html': content,
        'to': [{'email': email,
                'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')


def seller_declined_request(request, client, email, item):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Your request has been declined'
    from_email = settings.AUTO_REPLY
    context = Context({
        'client': client,
        'item': item,
        'site_name': settings.ADMIN_EMAIL,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('pages/emails/seller_declined_request.html', context)
    message = {
        'subject': subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': from_email,
        'from_name': 'NEMO',
        'html': content,
        'to': [{'email': email,
                'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')


def seller_approved_request(request, client, seller, email, item, price):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Your request has been approved'
    from_email = settings.AUTO_REPLY
    context = Context({
        'client': client,
        'item': item,
        'price': price,
        'seller': seller,
        'site_name': settings.ADMIN_EMAIL,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('pages/emails/seller_approved_request.html', context)
    message = {
        'subject': subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': from_email,
        'from_name': 'NEMO',
        'html': content,
        'to': [{'email': email,
                'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')
