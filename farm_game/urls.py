from django.urls import path
from .views import GachaView, PlantView, SyncFarmView

urlpatterns = [
    path('api/gacha/', GachaView.as_view(), name='gacha_api'),
    path('api/plant/', PlantView.as_view(), name='plant_api'),
    path('api/sync/', SyncFarmView.as_view(), name='sync_api'),
]
