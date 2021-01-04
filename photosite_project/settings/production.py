from . import *

SECRET_KEY = '-~aO;| F;rE[??/w^zcumh(9'
DEBUG = False
ALLOWED_HOSTS = ['167.99.46.208']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'photosite',
        'USER': 'stephaned',
        'PASSWORD': 'SD059693',
        'HOST': '',
        'PORT': '5432',
    }
}