# core/urls.py
from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # Paths to serve PWA files from the root
    path('manifest.json', views.manifest_json, name='manifest'),
    path('service-worker.js', views.service_worker, name='service-worker'),
]