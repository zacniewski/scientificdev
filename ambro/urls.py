from django.urls import path

from .views import about, index, contact, product

app_name = 'frontend'

urlpatterns = [
    path('', index, name='index'),
    path('kontakt/', contact, name='contact'),
    path('produkt/', product, name='product'),
    path('o-nas/', about, name='about')
]
