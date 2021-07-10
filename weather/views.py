from django.shortcuts import render
import requests
from .models import City
from django.shortcuts import redirect


# Create your views here.

def index(request):
    url = "https://api.weatherapi.com/v1/current.json?key=b485dc224d674bd6a8155010212506&q={}&aqi=yes"



    if request.method == 'POST':
        city = request.POST.get('inputi')
        if not city in City.objects.all():
            r = requests.get(url.format(city)).json()
            if not r.__contains__('error'):
                City.objects.create(name=city)

    weather_data = []
    cities = City.objects.all()
    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            'region': r['location']['region'],
            'temperature': r['current']['temp_c'],
            'image_icon': r['current']['condition']['icon'],
            'description': r['current']['condition']['text'],
        }
        weather_data.append(city_weather)

    context = {'weather_data': weather_data}
    return render(request, "weather/index.html", context)
