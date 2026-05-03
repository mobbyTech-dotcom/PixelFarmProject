from django.urls import path
from .views import GachaView

urlpatterns = [
    path('api/gacha/', GachaView.as_view(), name='gacha_api'),
]
