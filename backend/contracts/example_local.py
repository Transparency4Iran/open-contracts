DATABASES_LOCAL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # 'HOST':'crowdlaw.ir',
        'NAME': 'contracts',
        'USER': 'omid',
        'PASSWORD': 'YOUR_PASSWORD',

    }
}

MEDIA_ROOT_LOCAL = '/home/omid/contracts/media/'

proxies = {}

FRONT_DOMAIN = 'cdb.tp4.ir'
BACK_DOMAIN = 'api.cdb.tp4.ir'
PROTOCOL = 'https'

STATIC_ROOT_LOCAL = '/home/omid/contracts/static/'
DEBUG_LOCAL = True
