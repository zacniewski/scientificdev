from django.forms import ModelForm, TextInput, Form, EmailField
from .models import Subscriber


class SubscriberForm(ModelForm):
    class Meta:
        model = Subscriber
        fields = ('email_of_subscriber',)
        widgets = {
            'email_of_subscriber': TextInput(attrs={'placeholder': 'Enter your e-mail',
                                                    'class': 'newsletter-field input-lg round',
                                                    'type': 'email',
                                                    'pattern': '.{5,100}',
                                                    'required': 'true',
                                                    'aria-required': 'true'
                                                    }),
        }


class UnsubscriberForm(Form):
    email_of_subscriber = EmailField()
