from datetime import datetime
import requests
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import CityForm
from .api_key import openweather_api_key
from .models import SearchHistory

current_date = datetime.now().strftime('%Y-%m-%d')
current_time = datetime.now().time()


@api_view(['GET'])
def search_history_api(request):
    search_history = SearchHistory.objects.all()
    data = {history.city: history.search_count for history in search_history}
    return Response(data)


def get_weather_data(request):
    weather_dict = None
    city = ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            search_history, created = SearchHistory.objects.get_or_create(city=city)
            search_history.search_count += 1
            search_history.save()
            openweather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweather_api_key}'
            response = requests.get(openweather_url)
            if response.status_code == 200:
                data = response.json()
                latitude = data['coord']['lat']
                longitude = data['coord']['lon']
                open_meteo_url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude=' \
                                 f'{longitude}&hourly=temperature_2m,wind_speed_10m'
                weather_response = requests.get(open_meteo_url)
                if weather_response.status_code == 200:
                    weather_dict = weather_response.json()

    else:
        form = CityForm()

    return render(request, 'weather/weather.html', {'form': form,
                                                    'weather_dict': weather_dict,
                                                    'city': city,
                                                    'current_date': current_date,
                                                    'current_time': current_time})
