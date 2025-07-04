from django.shortcuts import render, redirect
import requests
from .models import Link
from django.contrib.auth.models import User
from django.http import JsonResponse
from decouple import config

ACCESS_TOKEN = config('URL_ACCESS_TOKEN')

print("🔐 Access Token:", "LOADED" if ACCESS_TOKEN else "NOT LOADED")

def index(request):
    links = Link.objects.all().order_by('-created_at')[:10]  # latest 10
    return render(request, 'index.html', {'links': links})

def index_form(request):
    if request.method == 'POST':
        long_url = request.POST.get('long_url')

        if not long_url or not long_url.startswith("http"):
            error = "Please enter a valid URL that starts with http or https."
            return render(request, 'new_url.html', {'error': error})
    
        shorten_data, error = shorten_url(long_url)

        if error:
            return render(request, 'new_url.html', {'error': error})
        
        try:
            default_user = User.objects.get(id=1)
        except User.DoesNotExist:
            default_user = None 
        
        Link.objects.create(
            user=default_user,
            original_url=long_url,
            short_url=shorten_data['short_url'],
            status="Active",
            clicks=0,
            sl_id=shorten_data['sl_id']
        )

        return render(request, 'new_url.html', {
                    'shortened_url': shorten_data['short_url'],
                    'sl_id': shorten_data['sl_id']
                    })
    else :
        return redirect('index')

def shorten_url(long_url):
    url = 'https://api.rebrandly.com/v1/links'
    headers = {
        'apikey': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    data = {
        "destination": long_url,
        # Optional: set a custom slug
        # "slashtag": "custom-alias"
    }

    response = requests.post(url, headers=headers, json=data)

    print("📡 status code:", response.status_code)
    print("🧾 response:", response.text)

    if response.status_code == 200:
        response_data = response.json()
        print("✅ sl_id:", response_data.get("id"))
        return {
            "short_url": "https://" + response_data.get("shortUrl", "rebrand.ly/fallback"),
            "sl_id": response_data.get("id")
        }, None
    elif response.status_code == 403:
        return None, "Invalid API token."
    else:
        return None, "Ziplink couldn't shorten your URL. Please try again."
