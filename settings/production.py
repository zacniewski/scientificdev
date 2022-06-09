from .base import *

DEBUG = False
ADMINS = (
    ('Artur Zacniewski', 'a.zacniewski@gmail.com'),
    )
ALLOWED_HOSTS = ['.scientificdev.net']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
    }
}

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CELERY_BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'rpc://'
# Celery Data Format
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Warsaw'

STATIC_ROOT = "/home/ubuntu/scientificdev/static"
STATICFILES_DIRS = [
    BASE_DIR / "staticfiles",
    '/home/ubuntu/scientificdev/staticfiles/',
]

