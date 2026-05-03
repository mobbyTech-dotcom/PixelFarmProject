"""
URL configuration for pixel_farm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from .views import GachaView, PlantView, SyncFarmView, HarvestView, ActionView

urlpatterns = [
    path('api/gacha/', GachaView.as_view(), name='gacha_api'),
    path('api/plant/', PlantView.as_view(), name='plant_api'),
    path('api/sync/', SyncFarmView.as_view(), name='sync_api'),
    path('api/harvest/', HarvestView.as_view(), name='harvest_api'), # เพิ่มบรรทัดนี้
    path('api/action/', ActionView.as_view(), name='action_api'),    # เพิ่มบรรทัดนี้
]
