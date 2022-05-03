from celery.schedules import crontab
from django.core.mail import EmailMessage

from sd.celery import app


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


@app.task
def check():
    print("I am checking your stuff")


app.conf.beat_schedule = {
    "run-me-every-ten-seconds": {
        "task": "frontend.tasks.check",
        "schedule": 10.0
        },
    "task_send_email_about_ebook": {
        "task": "frontend.tasks.task_send_email_about_ebook",
        "schedule": crontab(minute='*/2')
        }
    }
