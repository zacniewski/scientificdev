from .base import *
DEBUG = False
ADMINS = (
    ('Artur Zacniewski', 'a.zacniewski@gmail.com'),
    )
ALLOWED_HOSTS = ['.scientificdev.net']

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

STATIC_ROOT = "/home/ubuntu/modernbusiness/staticfiles"
STATICFILES_DIRS = [
    LOWER_BASE_DIR / "static",
    '/home/ubuntu/scientificdev/static/',
]

