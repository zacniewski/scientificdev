from django.forms import CharField, EmailField, Form, \
    Textarea, TextInput, ValidationError


class ContactForm(Form):
    name = CharField(
        max_length=50,
        required=True,
        widget=TextInput(
            attrs={
                'placeholder': 'Enter your name',
                'class': 'input-lg round form-control',
                'pattern': '.{3,100}',
                'aria-required': 'true'
                }
            )
    )
    email = EmailField(
        max_length=254,
        required=True,
        widget=TextInput(
            attrs={
                'placeholder': 'Enter your email',
                'class': 'input-lg round form-control',
                'pattern': '.{5,100}',
                'aria-required': 'true'

            }
        )
    )

    message = CharField(
        max_length=2000,
        required=True,
        widget=Textarea(
            attrs={
                'placeholder': 'Enter your message',
                'class': 'input-lg round form-control',
                'style': 'height: 130px;'
            }
        ),
        help_text='Write here your message!'
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise ValidationError('You have to write something!')
