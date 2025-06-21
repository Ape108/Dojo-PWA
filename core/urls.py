# core/urls.py
from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    # The root URL now points to our new landing page.
    path('', views.LandingPageView.as_view(), name='landing'),
    
    # The new, secure dashboard for logged-in users.
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # Paths to serve PWA files from the root
    path('manifest.json', views.manifest_json, name='manifest'),
    path('service-worker.js', views.service_worker, name='service-worker'),
]