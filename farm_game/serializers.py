from rest_framework import serializers
from .models import PlayerProfile, FarmPlot

class PlayerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerProfile
        fields = ['money', 'bot_expire_time']

class FarmPlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmPlot
        fields = '__all__'
