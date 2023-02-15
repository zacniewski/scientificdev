import requests

from bs4 import BeautifulSoup
from celery.schedules import crontab
from django.core.mail import EmailMessage

from sd.celery import app

weather_codes = {
    (0,): "Clear sky",
    (1, 2, 3): "Mainly clear, partly cloudy, and overcast",
    (45, 48): "Fog and depositing rime fog",
    (51, 53, 55): "Drizzle: Light, moderate, and dense intensity",
    (56, 57): "Freezing Drizzle: Light and dense intensity",
    (61, 63, 65): "Rain: Slight, moderate and heavy intensity",
    (66, 67): "Freezing Rain: Light and heavy intensity",
    (71, 73, 75): "Snow fall: Slight, moderate, and heavy intensity",
    (77,): "Snow grains",
    (80, 81, 82): "Rain showers: Slight, moderate, and violent",
    (85, 86): "Snow showers slight and heavy",
    (95,): "Thunderstorm: Slight or moderate",
    (96, 99): "Thunderstorm with slight and heavy hail"
}


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
def task_send_chf_rate():
    page = requests.get('https://www.bankier.pl/waluty/kursy-walut/nbp/CHF')
    soup = BeautifulSoup(page.content, 'html.parser')
    kurs_chf = soup.find('div', attrs={'class': 'profilLast'}).get_text()
    subject = "Średni kurs CHF wg NBP"
    message = f"Kurs CHF na dzisiaj to {kurs_chf}. \n"
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
        f"Temperatura:  \n"
        f"- o 6.00: {weather_data['hourly']['temperature_2m'][6]} °C \n"
        f"- o 12.00: {weather_data['hourly']['temperature_2m'][12]} °C \n"
        f"- o 18.00: {weather_data['hourly']['temperature_2m'][18]} °C \n\n"
        f"Prędkość wiatru:  \n"
        f"- o 6.00: {weather_data['hourly']['windspeed_10m'][6]} km/h \n"
        f"- o 12.00: {weather_data['hourly']['windspeed_10m'][12]} km/h \n"
        f"- o 18.00: {weather_data['hourly']['windspeed_10m'][18]} km/h \n\n"
        f"Wilgotność:  \n"
        f"- o 6.00: {weather_data['hourly']['relativehumidity_2m'][6]}% \n"
        f"- o 12.00: {weather_data['hourly']['relativehumidity_2m'][12]}% \n"
        f"- o 18.00: {weather_data['hourly']['relativehumidity_2m'][18]}% \n\n"
        f"Opis pogody o 6.00: {current_weather_description}."
    )
    email = EmailMessage(subject,
                         message,
                         'artur@scientificdev.net',
                         ['artur.zacniewski@proton.me'])
    email.send(fail_silently=False)


app.conf.beat_schedule = {
    "task_send_email_about_ebook": {
        "task": "frontend.tasks.task_send_email_about_ebook",
        "schedule": crontab(hour=7, minute=5)
    },
    "task_send_chf_rate": {
        "task": "frontend.tasks.task_send_chf_rate",
        "schedule": crontab(hour=7, minute=10)
    },
    "task_send_weather_data": {
        "task": "frontend.tasks.task_send_weather_data",
        "schedule": crontab(hour=12, minute=0)
    }
}
