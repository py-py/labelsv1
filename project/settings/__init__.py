import os
from dotenv import load_dotenv

load_dotenv()
environment = os.getenv('ENVIRONMENT', 'dev')

from .base_settings import *

if environment == 'dev':
    from .local_settings import *
if environment == 'prod':
    from .prod_settings import *
