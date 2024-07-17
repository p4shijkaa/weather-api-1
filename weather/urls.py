from django.urls import path
from .views import get_weather_data
from .views import search_history_api

urlpatterns = [
    path('', get_weather_data, name='get_weather_data'),
    path('api/search-history/', search_history_api, name='search_history_api'),
]