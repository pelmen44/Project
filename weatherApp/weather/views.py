import requests
import pyowm
from django.shortcuts import render
from .models import City
from .forms import CityForm
from pyowm.owm import OWM
from PIL import Image
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pyowm.utils.config import get_default_config
import time

config_dict = get_default_config()
config_dict['language'] = 'ua'
owm = pyowm.OWM('xxx', config_dict)
#                     <label for= " name ">Місто</label>


def index(request):
    global g
    url = 'http://api.openweathermap.org/data/2.5/weather?q=lviv&appid=2b5a48283b2900ae51bba48f15efce8e'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()
    cities = City.objects.all()
    all_cities = []
    for city in cities:
        place = city.name
        owm = pyowm.OWM('2b5a48283b2900ae51bba48f15efce8e')
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(place)
        w = observation.weather
        temp = w.temperature('celsius')['temp']
        stat = w.detailed_status
        city_info = {
            'city': city.name,
            'temp': temp,
            'stat': stat
        }
        if city.name == 'lviv':
            sendMail(temp, w)
        all_cities.append(city_info)
    context = {'all_info': all_cities, 'form': form}
    return render(request, 'weather/index.html', context)


def sendMail(temp, w):
    stat = w.detailed_status
    msg = MIMEMultipart()
    to_email = 'ovodroman1@gmail.com '
    message = 'Сьогодні у львові жарко(' + str(temp) + ' градус)  \nCтатус: ' + stat
    message1 = 'Сьогодні у Львові тепло(' + str(temp) + ' градус) \nCтатус: ' + stat
    message2 = 'Сьогодні у Львові холодно(' + str(temp) + ' градус) \nCтатус: ' + stat
    from_email = 'roman.ovod.knm.2020@lpnu.ua'
    password = '10.10.2001'
    if temp > 10:
        msg.attach(MIMEText(message, 'plain'))
    elif 10 > temp > 0:
        msg.attach(MIMEText(message1, 'plain'))
    elif temp < 0:
        msg.attach(MIMEText(message2, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()
