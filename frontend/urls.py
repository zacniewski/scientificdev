from django.contrib import admin
from django.urls import path

from .views import index, contact

app_name = 'frontend'

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact')
]
