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

// ... (ฟังก์ชัน getCookie, pullGacha, syncFarm คงเดิม แต่เราจะปรับ syncFarm และเพิ่มฟังก์ชันใหม่) ...

function getCookie(name) { /* โค้ดเดิม */ ... }
async function pullGacha() { /* โค้ดเดิม */ ... }

let localPlots = []; // เก็บสถานะฟาร์มไว้ในเครื่องเพื่อทำ Game Loop

// โหลดข้อมูลครั้งแรก
async function syncFarm() {
    const response = await fetch('/farm/api/sync/');
    if (!response.ok) return;
    localPlots = await response.json();
    renderFarm();
}

// วาดแปลงผักใหม่บนจอ
function renderFarm() {
    const grid = document.getElementById('farm-grid');
    grid.innerHTML = '';

    localPlots.forEach(plot => {
        const div = document.createElement('div');
        div.className = `plot ${plot.is_unlocked ? '' : 'locked'} ${plot.is_dead ? 'dead' : ''}`;
        
        if (plot.plant_type) {
            let statusHTML = `<strong>${plot.plant_type.toUpperCase()}</strong><br>`;
            if (plot.is_dead) {
                statusHTML += `💀 ตายแล้ว`;
            } else if (plot.ticks_remaining > 0) {
                statusHTML += `⏳ ${plot.ticks_remaining}s`;
                if (plot.needs_water) statusHTML += `<br>💧 ต้องการน้ำ!`;
                if (plot.has_bug) statusHTML += `<br>🐛 แมลงลง!`;
            } else {
                statusHTML += `✅ พร้อมเก็บเกี่ยว`;
            }
            div.innerHTML = statusHTML;
            
            // ใส่ Event คลิก
            div.onclick = () => handlePlotClick(plot);
        } else {
            div.innerText = plot.is_unlocked ? '🌱 ว่าง (กดปลูก)' : '🔒';
        }
        grid.appendChild(div);
    });
}

// จัดการเมื่อผู้เล่นคลิกแปลงผัก
async function handlePlotClick(plot) {
    if (plot.is_dead || plot.ticks_remaining <= 0) {
        // เก็บเกี่ยว
        const res = await fetch('/farm/api/harvest/', {
            method: 'POST',
            headers: {'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json'},
            body: JSON.stringify({ plot_index: plot.plot_index })
        });
        const data = await res.json();
        if (res.ok) {
            alert(data.status);
            document.getElementById('money-display').innerText = data.current_money;
            syncFarm(); // โหลดข้อมูลใหม่
        }
    } else if (plot.needs_water) {
        await takeAction(plot.plot_index, 'water');
    } else if (plot.has_bug) {
        await takeAction(plot.plot_index, 'bug');
    }
}

// ส่งคำสั่งรดน้ำ/ฉีดยา
async function takeAction(index, action) {
    await fetch('/farm/api/action/', {
        method: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json'},
        body: JSON.stringify({ plot_index: index, action: action })
    });
    syncFarm();
}

// 🕹️ GAME LOOP: นับเวลาถอยหลัง (Tick) ทุกๆ 1 วินาทีในหน้าจอ
setInterval(() => {
    let needsRender = false;
    localPlots.forEach(plot => {
        if (plot.plant_type && !plot.is_dead && plot.ticks_remaining > 0) {
            plot.ticks_remaining -= 1;
            needsRender = true;
            
            // จำลองสุ่มอุปสรรคแบบขำๆ ในหน้าบ้าน (ความจริงควรทำฝั่ง Server เพื่อความชัวร์)
            if (plot.ticks_remaining % 10 === 0 && Math.random() < 0.2) {
                plot.needs_water = true;
            }
        }
    });
    if (needsRender) renderFarm();
}, 1000);

document.addEventListener("DOMContentLoaded", () => {
    syncFarm();
});
