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
