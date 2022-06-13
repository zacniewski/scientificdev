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
                return redirect('newsletter:newsletter_subscribe')
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
                messages.success(request, 'You are almost subscribed to the newsletter, check your mailbox!')
                print(subscription_confirmation_url)
                send_subscription_email(email_of_subscriber, subscription_confirmation_url)
                return redirect('newsletter:newsletter_subscribe')
            # if bad reCaptcha
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')

        else:
            form = SubscriberForm()
    else:
        form = SubscriberForm()
    return render(request, 'newsletter/newsletter-subscribe.html', {'form': form})


def subscription_confirmation(request):
    if request.method == "POST":
        raise Http404

    token = request.GET.get("token", None)

    if not token:
        logging.getLogger("warning").warning("Invalid Link ")
        messages.error(request, "Invalid Link")
        return HttpResponseRedirect(reverse('newsletter:newsletter_subscribe'))

    token = decrypt(token)
    if token:
        token = token.split('SEPARATOR')
        email = token[0]
        initiate_time = token[1]  # time when email was sent , in epoch format. can be used for later calculations
        current_time = time()
        print("initiate_time =", type(float(initiate_time)))
        print("current time =", type(current_time))
        print("Difference in seconds = ", current_time - float(initiate_time))
        try:
            subscribe_model_instance = Subscriber.objects.get(email_of_subscriber=email)
            # if user clicks confirmation link again
            if subscribe_model_instance.status == "Confirmed":
                messages.success(request, "Your subscription is already confirmed!")
            else:
                subscribe_model_instance.status = "Confirmed"
                subscribe_model_instance.updated_date = now()
                subscribe_model_instance.save()
                messages.success(request, "Subscription confirmed!")
                return HttpResponseRedirect(reverse('newsletter:newsletter_confirmation', args=[email]))

        except ObjectDoesNotExist as e:
            logging.getLogger("warning").warning(traceback.format_exc())
            messages.error(request, "Invalid Link")
    else:
        logging.getLogger("warning").warning("Invalid token ")
        messages.error(request, "Invalid Link")
    return redirect('newsletter:newsletter_subscribe')


def send_subscription_email(email, subscription_confirmation_url):
    data = dict()
    data["confirmation_url"] = subscription_confirmation_url
    data["subject"] = "Please confirm the subscription"
    data["email"] = email
    data["project_name"] = "Scientific Dev"
    data["site_url"] = "https://www.scientificdev.net"
    data["contact_us_url"] = "https://www.scientificdev.net/contact/"
    template = get_template("newsletter/subscription_mail.html")
    data["html_text"] = template.render(data)
    data["plain_text"] = strip_tags(data["html_text"])
    email_message = EmailMessage(data["subject"], data["plain_text"], 'artur@scientificdev.net',
                                 [data['email']])
    email_message.send(fail_silently=False)
    return True


def newsletter_confirmation(request, email):
    return render(request, 'newsletter/confirmation_thanks.html', {'email': email})
