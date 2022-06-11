from django.db import models


class Subscriber(models.Model):
    STATUSES_OF_SUBSCRIBER = [
        ('Unconfirmed', 'Unconfirmed'),
        ('Confirmed', 'Confirmed'),
        ('Unsubscribed', 'Unsubscribed'),
        ]
    email_of_subscriber = models.EmailField(max_length=200,
                                            unique=True)
    status = models.CharField(max_length=64,
                              blank=True,
                              choices=STATUSES_OF_SUBSCRIBER,
                              default='Unconfirmed')
    saving_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-saving_date',)

    def __str__(self):
        return self.email_of_subscriber
