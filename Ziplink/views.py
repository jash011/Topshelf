from django.shortcuts import render, redirect
import requests
from .models import Link
from django.contrib.auth.models import User
from django.http import JsonResponse
from decouple import config
from .helpers import shorten_url_helper, get_clicks_helper
from django.core.paginator import Paginator

ACCESS_TOKEN = config('URL_ACCESS_TOKEN')

print("🔐 Access Token:", "LOADED" if ACCESS_TOKEN else "NOT LOADED")

def index(request):
    link_list = Link.objects.only('short_url', 'original_url', 'clicks', 'status', 'created_at', 'sl_id').order_by('-created_at')
    paginator = Paginator(link_list, 4)
    page_number = request.GET.get('page')
    links = paginator.get_page(page_number)
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
    # Moved to helpers.py
    return shorten_url_helper(long_url)
    
def get_clicks(request, sl_id):
    # Moved to helpers.py
    return get_clicks_helper(request, sl_id)
