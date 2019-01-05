from .base_settings import *

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'corsheaders',
]

MIDDLEWARE.insert(2, 'corsheaders.middleware.CorsMiddleware')
CORS_ORIGIN_ALLOW_ALL = True
