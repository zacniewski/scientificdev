from datetime import datetime
import requests

from bs4 import BeautifulSoup
from celery.schedules import crontab
from django.core.mail import EmailMessage

from sd.celery import app

# Kody pogodowe dla API z open-meteo
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
    (99,): "burza z silnym gradem",
}

# Obsługa informacji przypominających o wystawieniu śmieci
trash_set_nr_1 = ("Odpady zmieszane", "Odpady bio", "Plastik i metal", "Makulatura")

# klucz - miesiąc, wartość - dzień miesiąca
dates_for_trash_set_nr_1 = {
    1: (15,),
    2: (12,),
    3: (13,),
    4: (11,),
    5: (8,),
    6: (5,),
    7: (3, 31),
    8: (14,),
    9: (25,),
    10: (23,),
    11: (20,),
    12: (18,),
}

trash_set_nr_2 = ("Odpady zmieszane", "Odpady bio", "Szkło", "Popiół", "Odpady zielone")
dates_for_trash_set_nr_2 = {
    1: (2, 29),
    2: (26,),
    3: (27,),
    4: (24,),
    5: (22,),
    6: (19,),
    7: (17,),
    8: (28,),
    9: (11,),
    10: (9,),
    11: (6,),
    12: (4,),
}

trash_set_nr_3 = ("Odpady wielkogabarytowe",)
dates_for_trash_set_nr_3 = {3: (4,), 9: (2,)}

trash_set_nr_4 = ("Odpady bio",)
dates_for_trash_set_nr_4 = {6: (12, 26), 7: (10, 24), 8: (7, 21)}

trash_dates_relations = {
    trash_set_nr_1: dates_for_trash_set_nr_1,
    trash_set_nr_2: dates_for_trash_set_nr_2,
    trash_set_nr_3: dates_for_trash_set_nr_3,
    trash_set_nr_4: dates_for_trash_set_nr_4,
}


@app.task
def task_send_email_about_ebook():
    page = requests.get("https://www.packtpub.com/free-learning")
    soup = BeautifulSoup(page.content, "html.parser")
    book_title = (
        soup.find("h3", attrs={"class": "product-info__title"})
        .text.split("-", 1)[1]
        .strip()
    )
    subject = "Your free e-book from PacktPub is available!"
    message = f"Your new e-book is '{book_title}'. \n"
    message += f"Book is available at <a href='https://www.packtpub.com/packt/offers/free-learning'>Free Learning</a>."
    email = EmailMessage(
        subject, message, "artur@scientificdev.net", ["artur.zacniewski@proton.me"]
    )
    email.send(fail_silently=False)


@app.task
def task_send_weather_data_full_hours():
    weather_data = requests.get(
        "https://api.open-meteo.com/v1/forecast?latitude=54.57&longitude=18.20"
        "&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
    ).json()

    subject = f"Pogoda na {weather_data['current_weather']['time'].split('T')[0]}"
    current_weather_code = weather_data["current_weather"]["weathercode"]
    current_weather_description = ""
    for key in weather_codes.keys():
        if current_weather_code in key:
            current_weather_description = weather_codes[key]

    message = ""
    message += f"I. Temperatura:  \n"
    for i in range(24):
        message += f"- o godz. {i}.00: {weather_data['hourly']['temperature_2m'][i]} °C \n"
    message += "\n"

    message += f"II. Prędkość wiatru:  \n"
    for i in range(24):
        message += f"- o godz. {i}.00: {weather_data['hourly']['windspeed_10m'][i]} km/h \n"
    message += "\n"

    message += f"III. Wilgotność:  \n"
    for i in range(24):
        message += f"- o godz. {i}.00: {weather_data['hourly']['relativehumidity_2m'][i]}% \n"
    message += "\n"

    message += f"IV. Pogoda o 6.00: {current_weather_description}."

    email = EmailMessage(
        subject,
        message,
        "artur@scientificdev.net",
        ["artur.zacniewski@proton.me"],
    )
    email.send(fail_silently=False)


@app.task
def task_send_weather_data_four_hours():
    weather_data_four_hours = requests.get(
        "https://api.open-meteo.com/v1/forecast?latitude=54.57&longitude=18.20"
        "&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
    ).json()

    subject = f"Pogoda na {weather_data_four_hours['current_weather']['time'].split('T')[0]}"
    current_weather_code = weather_data_four_hours["current_weather"]["weathercode"]
    current_weather_description = ""
    for key in weather_codes.keys():
        if current_weather_code in key:
            current_weather_description = weather_codes[key]

    message = (
        f"I. Temperatura:  \n"
        f"- o 6.00: {weather_data_four_hours['hourly']['temperature_2m'][6]} °C \n"
        f"- o 12.00: {weather_data_four_hours['hourly']['temperature_2m'][12]} °C \n"
        f"- o 18.00: {weather_data_four_hours['hourly']['temperature_2m'][18]} °C \n\n"
        f"II. Prędkość wiatru:  \n"
        f"- o 6.00: {weather_data_four_hours['hourly']['windspeed_10m'][6]} km/h \n"
        f"- o 12.00: {weather_data_four_hours['hourly']['windspeed_10m'][12]} km/h \n"
        f"- o 18.00: {weather_data_four_hours['hourly']['windspeed_10m'][18]} km/h \n\n"
        f"III. Wilgotność:  \n"
        f"- o 6.00: {weather_data_four_hours['hourly']['relativehumidity_2m'][6]}% \n"
        f"- o 12.00: {weather_data_four_hours['hourly']['relativehumidity_2m'][12]}% \n"
        f"- o 18.00: {weather_data_four_hours['hourly']['relativehumidity_2m'][18]}% \n\n"
        f"IV. Pogoda o 6.00: {current_weather_description}."
    )

    email = EmailMessage(
        subject,
        message,
        "artur@scientificdev.net",
        ["artur@scientificdev.net", "joanna.zacniewska@gmail.com"],
    )
    email.send(fail_silently=False)


@app.task
def task_trash_reminder():
    today = datetime.now()
    number_of_month = today.month
    number_of_day = today.day

    subject = "Jutro wywóz śmieci"
    message = "Śmieci do wystawienia na jutro to: \n"

    for key in trash_dates_relations:
        if number_of_day + 1 in trash_dates_relations[key].get(
                number_of_month, (1000,)
        ):
            for trash in key:
                message += f"- {trash} \n"
            email = EmailMessage(
                subject,
                message,
                "artur@scientificdev.net",
                ["artur.zacniewski@proton.me", "joanna.zacniewska@gmail.com"],
            )
            email.send(fail_silently=False)


@app.task
def task_home_filters():
    subject = "Filtry rekuperatora, okapu i filtry wody"
    message = f"Czas na wymianę filtrów rekuperatora, okapu i filtrów wody. \n\n"
    message += f"Filtry rekuperatora dostępne są <a href='https://cennik24.pl/'>tutaj</a>.\n\n"
    message += f"Filtry okapu dostępne sa na Allegro! \n\n"
    message += f"Filtry wody, które aktualnie używasz to: filtr 25 um, filtr z węglem aktywnym oraz filtr 5 um \n\n"
    message += (f"Pamiętaj o przepłukaniu filtra z węglem aktywnym po wymianie, z założonym filtrem 25 um, "
                f"ale bez założonego jeszcze filtra 5 um!")
    email = EmailMessage(
        subject, message, "artur@scientificdev.net", ["artur.zacniewski@proton.me"]
    )
    email.send(fail_silently=False)


@app.task
def task_car_oil_exchange():
    subject = "Wymiana oleju w samochodzie"
    message = f"Czas na wymianę oleju w Twoim aucie. \n\n"
    message += f"Umów się ze swoim mechanikiem!"
    email = EmailMessage(
        subject, message, "artur@scientificdev.net", ["artur.zacniewski@proton.me"]
    )
    email.send(fail_silently=False)


# SCHEDULE
app.conf.beat_schedule = {
    "task_send_email_about_ebook": {
        "task": "frontend.tasks.task_send_email_about_ebook",
        "schedule": crontab(hour=6, minute=5),
    },
    "task_send_weather_data_full_hours": {
        "task": "frontend.tasks.task_send_weather_data_full_hours",
        "schedule": crontab(hour=6, minute=0),
    },
    "task_send_weather_data_four_hours": {
        "task": "frontend.tasks.task_send_weather_data_four_hours",
        "schedule": crontab(hour=6, minute=1),
    },
    "task_trash_reminder": {
        "task": "frontend.tasks.task_trash_reminder",
        "schedule": crontab(hour=19, minute=0),
    },
    "task_home_filters": {
        "task": "frontend.tasks.task_home_filters",
        "schedule": crontab(
            month_of_year="3, 6, 9, 12", day_of_month=29, hour=8, minute=10
        ),
    },
    "task_car_oil_exchange": {
        "task": "frontend.tasks.task_car_oil_exchange",
        "schedule": crontab(
            month_of_year="3, 9", day_of_month=28, hour=18, minute=10
        ),
    },
}
