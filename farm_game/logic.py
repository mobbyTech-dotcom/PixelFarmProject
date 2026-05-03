import random

def calculate_gacha_result():
    # เรทกาชาที่คุณตั้งไว้ (60/30/9/1)
    r = random.random()
    if r < 0.01: 
        tier = 'god'
    elif r < 0.10: 
        tier = 'gold'
    elif r < 0.40: 
        tier = 'silver'
    else: 
        tier = 'bronze'
    
    # สุ่มเลขพืชย่อย เช่น b1 - b5
    sub_id = f"{tier[0]}{random.randint(1, 5)}"
    return tier, sub_id
