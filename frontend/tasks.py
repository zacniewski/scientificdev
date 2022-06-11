import requests

from bs4 import BeautifulSoup
from celery.schedules import crontab
from django.core.mail import EmailMessage

from sd.celery import app


@app.task
def task_send_email_about_ebook():
    page = requests.get('https://www.packtpub.com/free-learning')
    soup = BeautifulSoup(page.content, 'html.parser')
    book_title = soup.find('h3', attrs={'class': 'product-info__title'}).text.split('-', 1)[1].strip()
    subject = "Your free e-book from PacktPub is available!"
    message = f"Your new e-book is '{book_title}'. \n"
    message += f"Book is available at <a href='https://www.packtpub.com/packt/offers/free-learning'>Free Learning</a>."
    email = EmailMessage(subject,
                         message,
                         'artur@scientificdev.net',
                         ['a.zacniewski@interia.eu'])
    # email.content_subtype = "html"
    email.send(fail_silently=False)


@app.task
def task_send_chf_rate():
    page = requests.get('https://internetowykantor.pl/kurs-franka/')
    soup = BeautifulSoup(page.content, 'html.parser')
    kurs_chf = soup.find('span', attrs={'data-rates-direction': 'sell'}).text.strip()
    subject = "Kurs CHF"
    message = f"Kurs CHF na dzisiaj to {kurs_chf} zł. \n"
    email = EmailMessage(subject,
                         message,
                         'artur@scientificdev.net',
                         ['a.zacniewski@interia.eu'])
    email.content_subtype = "html"
    email.send(fail_silently=False)


app.conf.beat_schedule = {
    "task_send_email_about_ebook": {
        "task": "frontend.tasks.task_send_email_about_ebook",
        "schedule": crontab(hour=7, minute=5)
        },
    "task_send_chf_rate": {
        "task": "frontend.tasks.task_send_chf_rate",
        "schedule": crontab(hour=7, minute=10)
        }
    }
