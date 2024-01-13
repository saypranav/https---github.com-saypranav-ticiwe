"""ticiwe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from geoapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('geo_locations/', views.geo_locations),
    path('tasks/', views.tasks),
    path('notes/', views.notes),
    # path('user/', views.user),
    # path('files/', views.files),
    # path('user_group/', views.user_group),
    # path('settings/', views.settings),
]
