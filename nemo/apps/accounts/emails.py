import mandrill
from django.template import Context
from django.template import loader
from django.conf import settings


mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)


def reset_mail(request, email, first_name, reset_key):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Reset account password'
    from_email = settings.AUTO_REPLY
    context = Context({
        'username': first_name,
        'reset_key': reset_key,
        'site_name': settings.BRAND,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('accounts/emails/password_reset_email.html', context)
    message = {
        'subject': subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': from_email,
        'from_name': 'NEMO',
        'html': content,
        'to': [{'email': email,
                'name': first_name,
                'type': 'to'}],
        'return_path_domain': settings.MANDRILL_DOMAIN,
        'signing_domain': settings.MANDRILL_DOMAIN,
        'tracking_domain': settings.MANDRILL_DOMAIN,
    }
    mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')


def confirm_register_mail(request, email, first_name, last_name, zip_code):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Thanks for registering'
    from_email = settings.AUTO_REPLY
    context = Context({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'zip_code': zip_code,
        'site_name': settings.BRAND,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('accounts/emails/confirm_register_email.html', context)
    message = {
        'subject': subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': from_email,
        'from_name': 'NEMO',
        'html': content,
        'to': [{'email': email,
                'name': first_name,
                'type': 'to'}],
        'return_path_domain': settings.MANDRILL_DOMAIN,
        'signing_domain': settings.MANDRILL_DOMAIN,
        'tracking_domain': settings.MANDRILL_DOMAIN,
    }
    mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')
