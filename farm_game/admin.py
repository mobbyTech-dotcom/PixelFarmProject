from django.contrib import admin
from .models import PlayerProfile, FarmPlot

@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'money', 'bot_expire_time')

@admin.register(FarmPlot)
class FarmPlotAdmin(admin.ModelAdmin):
    list_display = ('owner', 'plot_index', 'plant_type', 'is_dead')
    list_filter = ('is_dead', 'plant_type')
