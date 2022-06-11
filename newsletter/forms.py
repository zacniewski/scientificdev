from django.forms import ModelForm, TextInput, Form, EmailField
from .models import Subscriber


class SubscriberForm(ModelForm):
    class Meta:
        model = Subscriber
        fields = ('email_of_subscriber',)
        widgets = {
            'email_of_subscriber': TextInput(attrs={'placeholder': 'Enter your e-mail',
                                                    'class': 'uk-input uk-form-large uk-width-1-1',
                                                    'type': 'email',
                                                    }),
        }


class UnsubscriberForm(Form):
    email_of_subscriber = EmailField()
