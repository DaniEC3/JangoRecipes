"""
URL configuration for jangorecipes project.

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
from django.urls import path
from django.urls import include
from .view import login_view, logout_view, register_view

from django.conf import settings # Allows you to access the MEDIA_URL and MEDIA_ROOT variables
from django.conf.urls.static import static # Allows you to create URLs from local folder names.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('login/', login_view, name='login'),
    path("logout/", logout_view, name='logout'), 
    path('register/', register_view, name='register'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
