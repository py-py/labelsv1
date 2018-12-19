from .base_settings import *

ALLOWED_HOSTS += ['localhost', '127.0.0.1']

INSTALLED_APPS += [
    'corsheaders',
]

MIDDLEWARE.insert(2, 'corsheaders.middleware.CorsMiddleware')
