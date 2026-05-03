from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PlayerProfile, FarmPlot
import random

class GachaView(APIView):
    permission_classes = [IsAuthenticated] # ต้อง Login ถึงจะสุ่มได้

    def post(self, request):
        profile = PlayerProfile.objects.get(user=request.user)
        cost = 50 # ราคาสุ่มกาชาต่อครั้ง
        
        if profile.money < cost:
            return Response({"error": "เงินไม่พอสุ่มกาชา!"}, status=400)
        
        # หักเงินบน Server ทันที
        profile.money -= cost
        profile.save()

        # Logic การสุ่มเรท (60/30/9/1)
        r = random.random()
        if r < 0.01: tier = 'god'
        elif r < 0.10: tier = 'gold'
        elif r < 0.40: tier = 'silver'
        else: tier = 'bronze'

        # สุ่มเลขพืช (เช่น b1 - b5)
        sub_id = f"{tier[0]}{random.randint(1, 5)}"

        return Response({
            "tier": tier,
            "sub_id": sub_id,
            "current_money": profile.money
        })

from django.utils import timezone

class PlantView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # รับข้อมูลจากหน้าบ้าน: index ของแปลง, ประเภทพืช, sub_id
        plot_index = request.data.get('plot_index')
        plant_type = request.data.get('plant_type')
        sub_id = request.data.get('sub_id')
        ticks = request.data.get('ticks')

        try:
            plot = FarmPlot.objects.get(owner=request.user, plot_index=plot_index)
            if plot.plant_type:
                return Response({"error": "แปลงนี้มีพืชปลูกอยู่แล้ว!"}, status=400)
            
            # บันทึกข้อมูลการปลูกลง Database
            plot.plant_type = plant_type
            plot.sub_id = sub_id
            plot.ticks_remaining = ticks
            plot.is_dead = False
            plot.save()
            
            return Response({"status": "ปลูกพืชเรียบร้อย!"})
        except FarmPlot.DoesNotExist:
            return Response({"error": "ไม่พบแปลงผัก"}, status=404)

class SyncFarmView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # ดึงข้อมูลทุกแปลงของผู้เล่นคนนี้ส่งกลับไปที่หน้าบ้าน
        plots = FarmPlot.objects.filter(owner=request.user).order_index('plot_index')
        serializer = FarmPlotSerializer(plots, many=True)
        return Response(serializer.data)

# ... (โค้ดเดิม GachaView, PlantView, SyncFarmView) ...

class HarvestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plot_index = request.data.get('plot_index')
        try:
            plot = FarmPlot.objects.get(owner=request.user, plot_index=plot_index)
            profile = PlayerProfile.objects.get(user=request.user)
            
            if not plot.plant_type:
                return Response({"error": "ไม่มีพืชให้เก็บเกี่ยว!"}, status=400)
            
            if plot.ticks_remaining > 0:
                return Response({"error": "พืชยังไม่โตเต็มที่!"}, status=400)

            # ระบบราคาพืช (High Risk, High Return)
            reward = 0
            if not plot.is_dead:
                tier_rewards = {'god': 1000, 'gold': 500, 'silver': 150, 'bronze': 60}
                # สกัดชื่อ tier ออกมาจาก plant_type
                tier = plot.plant_type
                reward = tier_rewards.get(tier, 50)
                
                # โบนัสดินทอง
                if plot.is_rich_soil:
                    reward = int(reward * 1.5)
            else:
                reward = 5 # ขายซากพืชตายได้นิดหน่อย

            # รับเงินและล้างแปลงผัก
            profile.money += reward
            profile.save()
            
            plot.plant_type = None
            plot.sub_id = None
            plot.is_dead = False
            plot.needs_water = False
            plot.has_bug = False
            plot.save()

            return Response({"status": f"เก็บเกี่ยวสำเร็จ ได้รับ {reward} 💰", "current_money": profile.money})

        except FarmPlot.DoesNotExist:
            return Response({"error": "ไม่พบแปลงผัก"}, status=404)

class ActionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plot_index = request.data.get('plot_index')
        action_type = request.data.get('action') # 'water' หรือ 'bug'
        
        try:
            plot = FarmPlot.objects.get(owner=request.user, plot_index=plot_index)
            if action_type == 'water' and plot.needs_water:
                plot.needs_water = False
                plot.save()
                return Response({"status": "รดน้ำชุ่มฉ่ำแล้ว! 💦"})
            elif action_type == 'bug' and plot.has_bug:
                plot.has_bug = False
                plot.save()
                return Response({"status": "กำจัดแมลงเรียบร้อย! 🐛🔨"})
            
            return Response({"error": "ไม่จำเป็นต้องทำสิ่งนี้"}, status=400)
        except FarmPlot.DoesNotExist:
            return Response({"error": "ไม่พบแปลงผัก"}, status=404)
