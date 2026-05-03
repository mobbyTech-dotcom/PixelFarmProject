// static/js/game.js
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function pullGacha() {
    const response = await fetch('/farm/api/gacha/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    });

    if (response.ok) {
        const data = await response.json();
        alert(`🎉 ยินดีด้วย! คุณได้รับพืชระดับ: ${data.tier} (${data.sub_id})`);
        document.getElementById('money-display').innerText = data.current_money;
    } else {
        const err = await response.json();
        alert(`❌ ${err.error}`);
    }
}

async function syncFarm() {
    const response = await fetch('/farm/api/sync/');
    if (!response.ok) return; // ถ้ายังไม่ Login ไม่ต้องดึงข้อมูล
    const plots = await response.json();
    const grid = document.getElementById('farm-grid');
    grid.innerHTML = '';

    plots.forEach(plot => {
        const div = document.createElement('div');
        div.className = `plot ${plot.is_unlocked ? '' : 'locked'}`;
        div.innerText = plot.plant_type ? `${plot.plant_type}\n(${plot.ticks_remaining}s)` : (plot.is_unlocked ? 'ว่าง' : '🔒');
        grid.appendChild(div);
    });
}

// รันครั้งแรกเมื่อโหลดหน้าเว็บเสร็จ
document.addEventListener("DOMContentLoaded", () => {
    syncFarm();
});
