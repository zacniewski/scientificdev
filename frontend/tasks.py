from datetime import datetime
import requests

from bs4 import BeautifulSoup
from celery.schedules import crontab
from django.core.mail import EmailMessage

from sd.celery import app

weather_codes = {
    (0,): "czyste niebo",
    (1,): "głównie bezchmurnie",
    (2,): "częściowo pochmurno",
    (3,): "pochmurno",

    (45,): "mgła",
    (48,): "opadająca mgła szronowa",

    (51,): "mżawka lekka",
    (53,): "mżawka umiarkowana",
    (55,): "mżawka gęsta",

    (56,): "zamrażająca mżawka: lekka",
    (57,): "zamrażająca mżawka: gęsta intensywność",

    (61,): "deszcz słaby",
    (63,): "deszcz umiarkowany",
    (65,): "deszcz intensywny",

    (66,): "marznący deszcz: intensywność lekka",
    (67,): "marznący deszcz: intensywność ciężka",

    (71,): "opady śniegu: intensywność niewielka",
    (73,): "opady śniegu: intensywność umiarkowana",
    (75,): "opady śniegu: intensywność duża",

    (77,): "ziarna śniegu",
    (80,): "przelotne opady deszczu: słabe",
    (81,): "przelotne opady deszczu: umiarkowane",
    (82,): "przelotne opady deszczu: gwałtowne",

    (85,): "opady śniegu lekkie",
    (86,): "opady śniegu intensywne",

    (95,): "burza: Słaba lub umiarkowana",
    (96,): "burza z lekkim gradem",
    (99,): "burza z silnym gradem"
}

trash_set_nr_1 = ("Odpady zmieszane", "Odpady bio", "Plastik i metal", "Makulatura")

# klucz - miesiąc, wartość - dzień miesiąca
dates_for_trash_set_nr_1 = {
    4: 26,  # test
    5: 8,
    6: 5,
    7: 3,
    8: 14,
    9: 11,
    10: 9,
    11: 6,
    12: 4
}
trash_set_nr_2 = ("Odpady zmieszane", "Odpady bio", "Szkło", "Popiół", "Odpady zielone")
trash_set_nr_3 = ("Odpady wielkogabarytowe", )


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
                         ['artur.zacniewski@proton.me'])
    email.send(fail_silently=False)


@app.task
def task_send_weather_data():
    weather_data = requests.get('https://api.open-meteo.com/v1/forecast?latitude=54.57&longitude=18.20'
                                '&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m').json()

    subject = f"Pogoda na {weather_data['current_weather']['time'].split('T')[0]}"
    current_weather_code = weather_data['current_weather']['weathercode']
    current_weather_description = ""
    for key in weather_codes.keys():
        if current_weather_code in key:
            current_weather_description = weather_codes[key]
    message = (
        f"I. Temperatura:  \n"
        f"- o 6.00: {weather_data['hourly']['temperature_2m'][6]} °C \n"
        f"- o 12.00: {weather_data['hourly']['temperature_2m'][12]} °C \n"
        f"- o 18.00: {weather_data['hourly']['temperature_2m'][18]} °C \n\n"
        f"II. Prędkość wiatru:  \n"
        f"- o 6.00: {weather_data['hourly']['windspeed_10m'][6]} km/h \n"
        f"- o 12.00: {weather_data['hourly']['windspeed_10m'][12]} km/h \n"
        f"- o 18.00: {weather_data['hourly']['windspeed_10m'][18]} km/h \n\n"
        f"III. Wilgotność:  \n"
        f"- o 6.00: {weather_data['hourly']['relativehumidity_2m'][6]}% \n"
        f"- o 12.00: {weather_data['hourly']['relativehumidity_2m'][12]}% \n"
        f"- o 18.00: {weather_data['hourly']['relativehumidity_2m'][18]}% \n\n"
        f"IV. Pogoda o 6.00: {current_weather_description}."
    )
    email = EmailMessage(subject,
                         message,
                         'artur@scientificdev.net',
                         ['artur.zacniewski@proton.me', 'joanna.zacniewska@gmail.com'])
    email.send(fail_silently=False)


@app.task
def task_trash_reminder_set_1():
    today = datetime.now()
    month = today.month
    day = today.day

    subject = "Jutro wywóz śmieci"
    message = "Śmieci do wystawienia na jutro to: \n"

    if dates_for_trash_set_nr_1[month] == day:
        for trash in trash_set_nr_1:
            message += f"- {trash} \n"

        email = EmailMessage(subject,
                             message,
                             'artur@scientificdev.net',
                             ['artur.zacniewski@proton.me'])
        email.send(fail_silently=False)


# SCHEDULE
app.conf.beat_schedule = {
    "task_send_email_about_ebook": {
        "task": "frontend.tasks.task_send_email_about_ebook",
        "schedule": crontab(hour=6, minute=5)
    },
    "task_send_weather_data": {
        "task": "frontend.tasks.task_send_weather_data",
        "schedule": crontab(hour=6, minute=0)
    },
    "task_trash_reminder_set_1": {
        "task": "frontend.tasks.task_trash_reminder_set_1",
        "schedule": crontab(hour=7, minute=0)
    },
}
