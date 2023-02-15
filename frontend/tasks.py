import requests

from bs4 import BeautifulSoup
from celery.schedules import crontab
from django.core.mail import EmailMessage

from sd.celery import app

weather_codes = {
    (0,): "Czyste niebo",
    (1,): "Głównie bezchmurnie",
    (2,): "Częściowo pochmurno",
    (3,): "Pochmurno",

    (45,): "Mgła",
    (48,): "Opadająca mgła szronowa",

    (51,): "Mżawka lekka",
    (53,): "Mżawka umiarkowana",
    (55,): "Mżawka gęsta",

    (56,): "Zamrażająca mżawka: lekka",
    (57,): "Zamrażająca mżawka: gęsta intensywność",

    (61,): "Deszcz słaby",
    (63,): "Deszcz umiarkowany",
    (65,): "Deszcz intensywny",

    (66,): "Marznący deszcz: intensywność lekka",
    (67,): "Marznący deszcz: intensywność ciężka",

    (71,): "Opady śniegu: Intensywność niewielka",
    (73,): "Opady śniegu: Intensywność umiarkowana",
    (75,): "Opady śniegu: Intensywność duża",

    (77,): "Ziarna śniegu",
    (80,): "Przelotne opady deszczu: słabe",
    (81,): "Przelotne opady deszczu: umiarkowane",
    (82,): "Przelotne opady deszczu: gwałtowne",

    (85,): "Opady śniegu lekkie",
    (86,): "Opady śniegu intensywne",

    (95,): "Burza: Słaba lub umiarkowana",
    (96,): "Burza z lekkim gradem",
    (99,): "Burza z silnym gradem"
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
        f"IV. Opis pogody o 6.00: {current_weather_description}."
    )
    email = EmailMessage(subject,
                         message,
                         'artur@scientificdev.net',
                         ['artur.zacniewski@proton.me', 'joanna.zacniewska@gmail.com'])
    email.send(fail_silently=False)


app.conf.beat_schedule = {
    "task_send_email_about_ebook": {
        "task": "frontend.tasks.task_send_email_about_ebook",
        "schedule": crontab(hour=6, minute=5)
    },
    "task_send_chf_rate": {
        "task": "frontend.tasks.task_send_chf_rate",
        "schedule": crontab(hour=6, minute=10)
    },
    "task_send_weather_data": {
        "task": "frontend.tasks.task_send_weather_data",
        "schedule": crontab(hour=12, minute=24)
    }
}
