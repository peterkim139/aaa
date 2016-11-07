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
        'site_name': settings.BRAND,
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
        'return_path_domain': settings.MANDRILL_DOMAIN,
        'signing_domain': settings.MANDRILL_DOMAIN,
        'tracking_domain': settings.MANDRILL_DOMAIN,
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
        'site_name': settings.BRAND,
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
        'return_path_domain': settings.MANDRILL_DOMAIN,
        'signing_domain': settings.MANDRILL_DOMAIN,
        'tracking_domain': settings.MANDRILL_DOMAIN,
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
        'site_name': settings.BRAND,
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
        'return_path_domain': settings.MANDRILL_DOMAIN,
        'signing_domain': settings.MANDRILL_DOMAIN,
        'tracking_domain': settings.MANDRILL_DOMAIN,
    }
    mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')


def seller_canceled_request_before(request, client, email, item):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Your  request for ' + item + ' has been cancelled by the owner'
    from_email = settings.AUTO_REPLY
    context = Context({
        'client': client,
        'item': item,
        'site_name': settings.BRAND,
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
        'return_path_domain': settings.MANDRILL_DOMAIN,
        'signing_domain': settings.MANDRILL_DOMAIN,
        'tracking_domain': settings.MANDRILL_DOMAIN,
    }
    mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')


def seller_canceled_request_after(request, client, email, item):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Your request for ' + item + ' has been cancelled by the owner and we have given a $2 credit to use on NEMO'
    from_email = settings.AUTO_REPLY
    context = Context({
        'client': client,
        'item': item,
        'site_name': settings.BRAND,
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
        'return_path_domain': settings.MANDRILL_DOMAIN,
        'signing_domain': settings.MANDRILL_DOMAIN,
        'tracking_domain': settings.MANDRILL_DOMAIN,
    }
    mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')


def seller_declined_request(request, client, email, item, category):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Your request has been declined'
    from_email = settings.AUTO_REPLY
    context = Context({
        'client': client,
        'item': item,
        'category' : category,
        'site_name': settings.BRAND,
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
        'return_path_domain': settings.MANDRILL_DOMAIN,
        'signing_domain': settings.MANDRILL_DOMAIN,
        'tracking_domain': settings.MANDRILL_DOMAIN,
    }
    mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')


def seller_approved_request(request, client, seller, email, item, price, item_id, owner_id):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Your request has been approved'
    from_email = settings.AUTO_REPLY
    context = Context({
        'client': client,
        'item': item,
        'price': price,
        'seller': seller,
        'site_name': settings.BRAND,
        'item_id': item_id,
        'owner_id' : owner_id,
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
        'return_path_domain': settings.MANDRILL_DOMAIN,
        'signing_domain': settings.MANDRILL_DOMAIN,
        'tracking_domain': settings.MANDRILL_DOMAIN,
    }
    mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')



def new_message(request, pratner_email, partner_name, item_name, message, item_id):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'You have new message on NEMO'
    from_email = settings.AUTO_REPLY
    context = Context({
        'partner_name': partner_name,
        'user_id': request.user.id,
        'item_name':item_name,
        'user_name': request.user.first_name,
        'site_name': settings.BRAND,
        'message': message,
        'item_id': item_id,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('pages/emails/new_message.html', context)
    message = {
        'subject': subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': from_email,
        'from_name': 'NEMO',
        'html': content,
        'to': [{'email': pratner_email,
                'type': 'to'}],
        'return_path_domain': settings.MANDRILL_DOMAIN,
        'signing_domain': settings.MANDRILL_DOMAIN,
        'tracking_domain': settings.MANDRILL_DOMAIN,
    }
    mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')

def send_support_email(email, name, comments):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'New Message from Support form'
    context = Context({
        'comments': comments
    })
    context = loader.render_to_string('pages/emails/send_support_email.html', context)
    message = {
        'subject': subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': settings.AUTO_REPLY,
        'from_name': name,
        'html': context,
        'to': [{'email': settings.ADMIN_EMAIL,
                'type': 'to'}],
        "headers": {
            "Reply-To": email
        },
        'return_path_domain': settings.MANDRILL_DOMAIN,
        'signing_domain': settings.MANDRILL_DOMAIN,
        'tracking_domain': settings.MANDRILL_DOMAIN,
    }
    mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')
