import requests

from django.conf import settings as project_settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render

from .forms import ContactForm


def index(request):
    return render(request, 'frontend/index.html')


def contact(request):
    # messages.info(request, "Processing ...")

    if request.method == 'POST':
        form = ContactForm(request.POST)

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
                messages.success(request, 'Email sent successfully!')
                subject = 'Message from Scientific Dev'
                name = form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                message = form.cleaned_data.get('message')
                message += 2 * '\r\n' + 'Name: ' + name
                email_message = EmailMessage(subject, message, 'artur@scientificdev.net',
                                             ['a.zacniewski@gmail.com', 'a.zacniewski@interia.eu'],
                                             headers={'Reply-To': email})
                email_message.send(fail_silently=False)
                form = ContactForm()

            # if bad reCaptcha
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')

        # if form not valid
        else:
            messages.error(request, 'Something went wrong!!!')

    # if GET method
    else:
        form = ContactForm()
    return render(request, 'frontend/contact.html', {'form': form})
