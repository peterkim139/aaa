from .base import *



ALLOWED_HOSTS = ['*', ]


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nemo',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': ''
    }
}

# FACEBOOK_APP_ID = '423057731224981'
# FACEBOOK_API_SECRET = '199b5a1f0a4a5f9649e8c68ce16e1b19',

