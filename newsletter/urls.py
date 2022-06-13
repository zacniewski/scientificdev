from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('unsubscribe/', views.newsletter_unsubscribe, name='unsubscribe'),
    path('subscribe-confirmed/<email>', views.newsletter_confirmation, name='newsletter_confirmation'),
    path('unsubscribe-confirmed/<email>', views.unsubscribe_confirmation_email, name='unsubscribe_confirmation_email'),
    path('subscription-confirmation/', views.subscription_confirmation, name='subscription_confirmation'),
    path('unsubscribe-confirmation/', views.unsubscribe_confirmation, name='unsubscribe_confirmation'),
]
