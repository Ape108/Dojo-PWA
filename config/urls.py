"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings             # <-- 1. Add this import
from django.conf.urls.static import static # <-- 2. Add this import


urlpatterns = [
    path('admin/', admin.site.urls),
    # Include allauth's URLs for login, logout, etc.
    path('accounts/', include('allauth.urls')),
    # Include URLS from our belts app
    path('belts/', include('belts.urls')),
    # Include URLs from our core app (for home page, PWA files)
    path('', include('core.urls')),
]

# This pattern tells Django to serve media files during development.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
