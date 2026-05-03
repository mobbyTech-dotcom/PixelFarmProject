from django.db import models
from django.contrib.auth.models import User

# เก็บข้อมูลโปรไฟล์ผู้เล่น (เงิน, บอท)
class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.BigIntegerField(default=200) # เริ่มต้น 200💰 ตามที่คุณต้องการ
    bot_expire_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username

# เก็บสถานะของแต่ละแปลงผัก (8 แปลงต่อ 1 คน)
class FarmPlot(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    plot_index = models.IntegerField() # 0-7
    is_unlocked = models.BooleanField(default=False)
    
    # ข้อมูลพืช
    plant_type = models.CharField(max_length=50, null=True, blank=True) # เช่น bronze, gold
    sub_id = models.CharField(max_length=50, null=True, blank=True) # เช่น b1, g5
    ticks_remaining = models.IntegerField(default=0)
    
    # สถานะความเสี่ยงและการตาย
    is_dead = models.BooleanField(default=False)
    is_rich_soil = models.BooleanField(default=False)
    hazard_ticks = models.IntegerField(default=0)
    needs_water = models.BooleanField(default=False)
    has_bug = models.BooleanField(default=False)

    class Meta:
        unique_together = ('owner', 'plot_index') # ป้องกันข้อมูลซ้ำในแปลงเดิม
