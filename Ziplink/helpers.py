import requests
from django.http import JsonResponse
from .models import Link
from django.contrib.auth.models import User
from decouple import config

ACCESS_TOKEN = config('URL_ACCESS_TOKEN')

def shorten_url_helper(long_url):
    url = 'https://api.rebrandly.com/v1/links'
    headers = {
        'apikey': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }
    data = {
        "destination": long_url,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_data = response.json()
        return {
            "short_url": "https://" + response_data.get("shortUrl", "rebrand.ly/fallback"),
            "sl_id": response_data.get("id")
        }, None
    elif response.status_code == 403:
        return None, "Invalid API token."
    else:
        return None, "Ziplink couldn't shorten your URL. Please try again."

def get_clicks_helper(request, sl_id):
    if not sl_id:
        return JsonResponse({'error': 'Invalid sl_id'}, status=400)
    url = f'https://api.rebrandly.com/v1/links/{sl_id}'
    headers = {
        'apikey': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        click_count = data.get('clicks', 0)
        try:
            link = Link.objects.get(sl_id=sl_id)
            link.clicks = click_count
            link.save()
        except Link.DoesNotExist:
            pass
        return JsonResponse({'clicks': click_count})
    else:
        return JsonResponse({'error': 'Failed to fetch clicks'}, status=500)