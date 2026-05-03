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
