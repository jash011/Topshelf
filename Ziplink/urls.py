from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submitform', views.index_form, name='submitform'),
    path('get_clicks/<str:sl_id>/', views.get_clicks, name='get_clicks'),
    #path('zipped_url/', views.ajax_shorten, name='ajax_shorten'),  
]

