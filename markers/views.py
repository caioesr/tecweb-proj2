from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
import requests
import time
import json
from .models import Story

def marker(request):

    if request.method == 'POST':

        code = request.get_full_path().split('&')[-1].split('=')[-1]
        tld = code
        comment = request.POST.get('comment')
        
        story = Story(code=code, comment=comment)
        story.save()

        # pega clima

        url_weather = "https://yahoo-weather5.p.rapidapi.com/weather"

        latlng = request.get_full_path().split('&')[1].split('=')[-1]
        lat = latlng[7:13]
        lng = latlng[15:21]

        querystring = {"lat":lat,"long":lng,"format":"json","u":"c"}

        headers = {
            'x-rapidapi-key': "a561d89e46msh27f740727d63098p13524ajsnd1e7e7e124cb",
            'x-rapidapi-host': "yahoo-weather5.p.rapidapi.com"
            }

        response = requests.request("GET", url_weather, headers=headers, params=querystring)
        ans = response.json()

        city = ans['location']['city']
        country = ans['location']['country']
        wind = ans['current_observation']['wind']['speed']
        rain = ans['current_observation']['atmosphere']['humidity']
        region = ans['location']['region']
        today = ans['forecasts'][0]['day']
        todayDateDay = time.ctime(ans['forecasts'][0]['date'])[8:10]
        todayDateMonth = time.ctime(ans['forecasts'][0]['date'])[4:7]
        temperature = ans['current_observation']['condition']['temperature']

        todayData = {
            'city': city,
            'country': country,
            'wind': wind,
            'rain': rain,
            'region': region,
            'today': today,
            'todayDateDay': todayDateDay,
            'todayDateMonth': todayDateMonth,
            'temperature': temperature
        }

        days = []
        for day in ans['forecasts'][1:]:
            days.append({
                'day': day['day'],
                'low': day['low'],
                'high': day['high']
            })

        # pega radios

        url_radio = "https://radio-world-50-000-radios-stations.p.rapidapi.com/v1/radios/getTopByCountry"

        querystring = {"query":tld}

        headers = {
            'x-rapidapi-key': "a561d89e46msh27f740727d63098p13524ajsnd1e7e7e124cb",
            'x-rapidapi-host': "radio-world-50-000-radios-stations.p.rapidapi.com"
            }

        # response = requests.request("GET", url_radio, headers=headers, params=querystring)

        # uri = response.json()['radios'][0]['uri']

        uri = 'https://icecast.rtl.fr/rtl-1-44-128?listen=webDQcCCwwIBwMFBgUABAwDDg'

        radio = {
            'uri': uri,
            'tld': 'fr'
        }

        return render(request, 'mapAndRadio.html', {'comments':Story.objects.all().filter(code=tld),'radios': [radio], 'today':[todayData], 'days':days})

    elif (request.GET.__contains__('latlng') and request.GET.__contains__('tld')):

        # pega clima

        url_weather = "https://yahoo-weather5.p.rapidapi.com/weather"

        latlng = request.GET.get('latlng')
        lat = latlng[7:13]
        lng = latlng[15:20]

        querystring = {"lat":lat,"long":lng,"format":"json","u":"c"}

        headers = {
            'x-rapidapi-key': "a561d89e46msh27f740727d63098p13524ajsnd1e7e7e124cb",
            'x-rapidapi-host': "yahoo-weather5.p.rapidapi.com"
            }

        response = requests.request("GET", url_weather, headers=headers, params=querystring)
        ans = response.json()

        city = ans['location']['city']
        country = ans['location']['country']
        wind = ans['current_observation']['wind']['speed']
        rain = ans['current_observation']['atmosphere']['humidity']
        region = ans['location']['region']
        today = ans['forecasts'][0]['day']
        todayDateDay = time.ctime(ans['forecasts'][0]['date'])[8:10]
        todayDateMonth = time.ctime(ans['forecasts'][0]['date'])[4:7]
        temperature = ans['current_observation']['condition']['temperature']

        todayData = {
            'city': city,
            'country': country,
            'wind': wind,
            'rain': rain,
            'region': region,
            'today': today,
            'todayDateDay': todayDateDay,
            'todayDateMonth': todayDateMonth,
            'temperature': temperature
        }

        days = []
        for day in ans['forecasts'][1:]:
            days.append({
                'day': day['day'],
                'low': day['low'],
                'high': day['high']
            })

        # pega radios

        url_radio = "https://radio-world-50-000-radios-stations.p.rapidapi.com/v1/radios/getTopByCountry"

        tld = request.GET.get('tld')

        querystring = {"query":tld}

        headers = {
            'x-rapidapi-key': "a561d89e46msh27f740727d63098p13524ajsnd1e7e7e124cb",
            'x-rapidapi-host': "radio-world-50-000-radios-stations.p.rapidapi.com"
            }

        # response = requests.request("GET", url_radio, headers=headers, params=querystring)

        # uri = response.json()['radios'][0]['uri']

        uri = 'https://icecast.rtl.fr/rtl-1-44-128?listen=webDQcCCwwIBwMFBgUABAwDDg'

        radio = {
            'uri': uri,
            'tld': 'fr'
        }

        return render(request, 'mapAndRadio.html', {'comments':Story.objects.all().filter(code=tld),'radios': [radio], 'today':[todayData], 'days':days})

    return render(request, 'map.html')