from django.test import TestCase, Client
from django.urls import reverse
from .models import SearchHistory


class WeatherViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_weather_view(self):
        response = self.client.get(reverse('get_weather_data'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Прогноз погоды')

    def test_post_weather_view(self):
        response = self.client.post(reverse('get_weather_data'), {'city': 'Гомель'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Данные для города')

    def test_search_history_api(self):
        SearchHistory.objects.create(city='Гомель', search_count=1)
        response = self.client.get(reverse('search_history_api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'Гомель': 1})
