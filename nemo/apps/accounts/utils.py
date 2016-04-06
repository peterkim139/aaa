
import hashlib
import random
import mandrill
from django.template import Context
from django.template import loader
from django.conf import settings

mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

def generate_activation_key(email):
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    if isinstance(email, unicode):
        email = email.encode('utf-8')
    activation_key = hashlib.sha1(salt + email).hexdigest()
    return activation_key


def reset_mail(request, email, first_name, reset_key):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Reset account password'
    from_email = settings.AUTO_REPLY
    to = [email]
    context = Context({
        'username': first_name,
        'reset_key': reset_key,
        'site_name': settings.ADMIN_EMAIL,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('accounts/emails/password_reset_email.html', context)
    message = {
        'subject' : 'Reset account password',
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'NEMO',
        'html':content,
        'to': [{'email': email,
             'name': first_name,
             'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')

def confirm_register_mail(request, email, first_name, last_name, zip_code):

    mandrill_client = mandrill.Mandrill(settings.MANDRILL_KEY)

    subject = 'Thanks for registering'
    from_email = settings.AUTO_REPLY
    to = [email]
    context = Context({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'zip_code': zip_code,
        'site_name': settings.ADMIN_EMAIL,
        'absolute_url': request.META['HTTP_HOST']
    })
    content = loader.render_to_string('accounts/emails/confirm_register_email.html', context)
    message = {
        'subject' : subject,
        'bcc_address': 'message.bcc_address@example.com',
        'from_email': 'message.from_email@example.com',
        'from_name': 'NEMO',
        'html':content,
        'to': [{'email': email,
             'name': first_name,
             'type': 'to'}],
        'return_path_domain': 'nemo.codebnb.me',
        'signing_domain': 'nemo.codebnb.me',
        'tracking_domain': 'nemo.codebnb.me',
    }
    result = mandrill_client.messages.send(message=message, async=False, ip_pool='', send_at='')

