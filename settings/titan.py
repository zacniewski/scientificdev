from sri import Algorithm
from .base import *

DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATIC_ROOT = "/home/artur/Desktop/PROJECTS/scientificdev/staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
    '/home/artur/Desktop/PROJECTS/scientificdev/static',
]

# SRI
# https://pypi.org/project/django-sri/

USE_SRI = True
SRI_ALGORITHM = Algorithm.SHA256
