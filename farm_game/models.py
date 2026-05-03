from django.db import models
from django.contrib.auth.models import User

# เก็บข้อมูลโปรไฟล์ผู้เล่น (เงิน และ บอท)
class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.BigIntegerField(default=200) # เริ่มต้นเงิน 200 ตามที่คุณต้องการ
    bot_expire_time = models.DateTimeField(null=True, blank=True) # เวลาหมดอายุของบอท
    
    def __str__(self):
        return self.user.username

# เก็บข้อมูลแปลงผัก (8 แปลงต่อคน)
class FarmPlot(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    plot_index = models.IntegerField() # ลำดับแปลง 0-7
    is_unlocked = models.BooleanField(default=False)
    
    # ข้อมูลพืชที่ปลูก
    plant_type = models.CharField(max_length=50, null=True, blank=True) # เช่น bronze, gold
    sub_id = models.CharField(max_length=50, null=True, blank=True) # เช่น b1, g5
    ticks_remaining = models.IntegerField(default=0) # เวลาที่เหลือในการโต
    
    # สถานะความเสี่ยงและการตาย
    is_dead = models.BooleanField(default=False) # สถานะพืชตาย
    is_rich_soil = models.BooleanField(default=False) # ดินทอง
    needs_water = models.BooleanField(default=False) # ต้องการน้ำ
    has_bug = models.BooleanField(default=False) # แมลงกิน

    class Meta:
        unique_together = ('owner', 'plot_index')
