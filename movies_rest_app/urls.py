"""moviest_rest URL Configuration

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
from django.urls import path, include
from rest_framework import routers

from movies_rest_app import views
from movies_rest_app.oscar_views_set import OscarViewSet

router_oscar = routers.DefaultRouter()
router_oscar.register(r'oscars', OscarViewSet)


urlpatterns = [
    path('movies/', views.movies),
    path('actors/', views.actors),
    path('movie/<int:movie_id>/actors', views.get_actors_by_movie),
    path('actor/<int:actor_id>', views.actor),
    path('movie/<int:movie_id>/actor/<int:actor_id>', views.actor_by_movie),
    # path('movies/<movie_id>/oscars/', views.oscar)
]
urlpatterns.extend(router_oscar.urls)