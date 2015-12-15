from .base import *


DEBUG = True
THUMBNAIL_DEBUG = True


ALLOWED_HOSTS = ['*', ]


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env_variable('DJANGO_DATABASE_NAME'),
        'USER': get_env_variable('DJANGO_USER'),
        'PASSWORD': get_env_variable('DJANGO_PASSWORD'),
        'HOST': get_env_variable('DJANGO_DATABASE_HOST'),
        'PORT': ''
    }
}

# FACEBOOK_APP_ID = '423057731224981'
# FACEBOOK_API_SECRET = '199b5a1f0a4a5f9649e8c68ce16e1b19',

