import logging
import traceback
from time import time

import requests
from django.conf import settings as project_settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import validate_email
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.utils.timezone import now

from .disposable_emails import disposable_emails
from .email_utility import token_generator, decrypt
from .forms import SubscriberForm, UnsubscriberForm
from .models import Subscriber


def newsletter_subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        post_data = request.POST.copy()
        email_of_subscriber = post_data.get("email_of_subscriber", None)
        check_disposability_of_email = email_of_subscriber.split('@')[-1] in disposable_emails
        try:
            validate_email(email_of_subscriber)
        except ValidationError:
            messages.error(request, "Enter a valid email address!")
        else:
            if Subscriber.objects.filter(email_of_subscriber=email_of_subscriber).exists():
                messages.warning(request, 'This email is already subscribed!')
                return redirect('about')
            if check_disposability_of_email:
                messages.error(request, 'This email is forbidden!')
                return redirect('about')
        if form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': project_settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' End reCAPTCHA validation '''

            if result['success']:
                instance = form.save(commit=False)
                instance.save()
                token = token_generator(email_of_subscriber)
                subscription_confirmation_url = request.build_absolute_uri(
                    reverse('newsletter:subscription_confirmation')) + "?token=" + token
                messages.success(request, 'You are almost subscribed to the newsletter!')
                print(subscription_confirmation_url)
                send_subscription_email(email_of_subscriber, subscription_confirmation_url)
                return redirect('about')
            # if bad reCaptcha
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')

        else:
            form = SubscriberForm()
    else:
        form = SubscriberForm()
    return render(request, 'newsletter/newsletter-subscribe.html', {'form': form})


def send_subscription_email(email, subscription_confirmation_url):
    data = dict()
    data["confirmation_url"] = subscription_confirmation_url
    data["subject"] = "Please confirm the subscription"
    data["email"] = email
    data["project_name"] = "Scientific Dev"
    data["site_url"] = "https://www.scientificdev.net"
    data["contact_us_url"] = "https://www.scientificdev.net/contact/"
    template = get_template("newsletters/subscription_mail.html")
    data["html_text"] = template.render(data)
    data["plain_text"] = strip_tags(data["html_text"])
    email_message = EmailMessage(data["subject"], data["plain_text"], 'artur@scientificdev.net',
                                 [data['email']])
    email_message.send(fail_silently=False)
    return True
