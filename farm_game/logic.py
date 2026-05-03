import random

def pull_gacha_logic(tier_type='normal'):
    # เรทกาชาที่คุณตั้งไว้ (60/30/9/1)
    if tier_type == 'normal':
        r = random.random()
        if r < 0.01: return 'god'
        if r < 0.10: return 'gold'
        if r < 0.40: return 'silver'
        return 'bronze'
    return 'bronze'
