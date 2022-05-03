from celery.schedules import crontab
from django.core.mail import EmailMessage

from sd.celery import app


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='*/2'),
        task_send_email_about_ebook(),
    )


@app.task
def task_send_email_about_ebook():
    subject = 'Your free e-book from PacktPub is available!'
    message = "Your new e-book is"
    message += " available at <a href='https://www.packtpub.com/packt/offers/free-learning'>Free Learning</a>."
    email = EmailMessage(subject,
                         message,
                         'artur@scientificdev.net',
                         ['a.zacniewski@interia.eu'])
    # email.content_subtype = "html"
    email.send(fail_silently=False)
