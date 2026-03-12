// Global variables
let isSimulationRunning = true;
let vehicles = [];
let signalTimers = { A: 45, B: 30, C: 15, D: 60 };

// Initialize on load
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeIntersection();
    initializeCityMap();
    initializeCharts();
    startSignalTimers();
    startDataUpdates();
    initializeSliders();
    initializeLogFilters();
});

// Navigation
function initializeNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.content-section');
    const mobileToggle = document.getElementById('mobileToggle');
    const navMenu = document.getElementById('navMenu');
    
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const sectionId = item.getAttribute('data-section');
            
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            
            sections.forEach(section => section.classList.remove('active'));
            document.getElementById(sectionId).classList.add('active');
            
            // redraw charts when analytics section become active
            if (sectionId === 'analytics') {
                initializeCharts();
            }
            navMenu.classList.remove('active');
        });
    });
    
    mobileToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });
}

// Intersection Canvas
function initializeIntersection() {
    const canvas = document.getElementById('intersectionCanvas');
    const ctx = canvas.getContext('2d');
    
    // Initialize vehicles
    vehicles = [
        { x: 240, y: 100, lane: 'A', color: '#e74c3c', speed: 2, direction: 'down' },
        { x: 400, y: 240, lane: 'B', color: '#95a5a6', speed: 2, direction: 'left' },
        { x: 260, y: 400, lane: 'C', color: '#95a5a6', speed: 2, direction: 'up' },
        { x: 100, y: 260, lane: 'D', color: '#95a5a6', speed: 2, direction: 'right' }
    ];
    
    animateIntersection(ctx, canvas);
}

function animateIntersection(ctx, canvas) {
    if (!isSimulationRunning) {
        requestAnimationFrame(() => animateIntersection(ctx, canvas));
        return;
    }
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw roads
    ctx.fillStyle = '#e0e0e0';
    ctx.fillRect(200, 0, 100, 500);
    ctx.fillRect(0, 200, 500, 100);
    
    // Draw lane markings
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 3;
    ctx.setLineDash([15, 15]);
    
    ctx.beginPath();
    ctx.moveTo(250, 0);
    ctx.lineTo(250, 200);
    ctx.moveTo(250, 300);
    ctx.lineTo(250, 500);
    ctx.moveTo(0, 250);
    ctx.lineTo(200, 250);
    ctx.moveTo(300, 250);
    ctx.lineTo(500, 250);
    ctx.stroke();
    ctx.setLineDash([]);
    
    // Draw center hub
    ctx.fillStyle = '#2c3e50';
    ctx.fillRect(200, 200, 100, 100);
    
    // Draw traffic light
    ctx.fillStyle = '#667eea';
    ctx.beginPath();
    ctx.arc(250, 250, 20, 0, Math.PI * 2);
    ctx.fill();
    
    // Draw and update vehicles
    vehicles.forEach(vehicle => {
        ctx.fillStyle = vehicle.color;
        ctx.fillRect(vehicle.x - 15, vehicle.y - 15, 30, 30);
        
        // Move vehicles
        switch(vehicle.direction) {
            case 'down':
                vehicle.y += vehicle.speed;
                if (vehicle.y > 500) vehicle.y = 50;
                break;
            case 'up':
                vehicle.y -= vehicle.speed;
                if (vehicle.y < 0) vehicle.y = 450;
                break;
            case 'left':
                vehicle.x -= vehicle.speed;
                if (vehicle.x < 0) vehicle.x = 450;
                break;
            case 'right':
                vehicle.x += vehicle.speed;
                if (vehicle.x > 500) vehicle.x = 50;
                break;
        }
    });
    
    // Draw lane labels
    ctx.fillStyle = '#2d3748';
    ctx.font = 'bold 16px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('Lane A', 250, 40);
    ctx.fillText('Lane B', 460, 255);
    ctx.fillText('Lane C', 250, 480);
    ctx.fillText('Lane D', 40, 255);
    
    requestAnimationFrame(() => animateIntersection(ctx, canvas));
}

function toggleSimulation() {
    isSimulationRunning = !isSimulationRunning;
    const icon = document.getElementById('playPauseIcon');
    const text = document.getElementById('playPauseText');
    
    if (isSimulationRunning) {
        icon.textContent = '⏸️';
        text.textContent = 'Pause';
    } else {
        icon.textContent = '▶️';
        text.textContent = 'Play';
    }
}

function resetSimulation() {
    vehicles = [
        { x: 240, y: 100, lane: 'A', color: '#e74c3c', speed: 2, direction: 'down' },
        { x: 400, y: 240, lane: 'B', color: '#95a5a6', speed: 2, direction: 'left' },
        { x: 260, y: 400, lane: 'C', color: '#95a5a6', speed: 2, direction: 'up' },
        { x: 100, y: 260, lane: 'D', color: '#95a5a6', speed: 2, direction: 'right' }
    ];
}

// City Map Canvas
function initializeCityMap() {
    const canvas = document.getElementById('cityMapCanvas');
    const ctx = canvas.getContext('2d');
    
    drawCityMap(ctx, canvas);
}

function drawCityMap(ctx, canvas) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Background
    ctx.fillStyle = '#f7fafc';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw grid of streets
    ctx.strokeStyle = '#cbd5e0';
    ctx.lineWidth = 2;
    
    for (let i = 0; i < 6; i++) {
        // Vertical streets
        ctx.beginPath();
        ctx.moveTo(200 * i, 0);
        ctx.lineTo(200 * i, canvas.height);
        ctx.stroke();
        
        // Horizontal streets
        ctx.beginPath();
        ctx.moveTo(0, 100 * i);
        ctx.lineTo(canvas.width, 100 * i);
        ctx.stroke();
    }
    
    // Draw intersections with traffic density
    const intersections = [
        { x: 200, y: 100, density: 'low', label: 'A' },
        { x: 400, y: 100, density: 'medium', label: 'B' },
        { x: 600, y: 100, density: 'high', label: 'C' },
        { x: 800, y: 100, density: 'medium', label: 'D' },
        { x: 200, y: 300, density: 'medium', label: 'E' },
        { x: 400, y: 300, density: 'low', label: 'F' },
        { x: 600, y: 300, density: 'medium', label: 'G' },
        { x: 800, y: 300, density: 'high', label: 'H' }
    ];
    
    intersections.forEach(intersection => {
        let color;
        switch(intersection.density) {
            case 'low': color = '#27ae60'; break;
            case 'medium': color = '#f39c12'; break;
            case 'high': color = '#e74c3c'; break;
        }
        
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(intersection.x, intersection.y, 15, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.fillStyle = '#2d3748';
        ctx.font = 'bold 14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(intersection.label, intersection.x, intersection.y + 35);
    });
    
    // Draw emergency route
    ctx.strokeStyle = '#9b59b6';
    ctx.lineWidth = 4;
    ctx.setLineDash([10, 5]);
    ctx.beginPath();
    ctx.moveTo(200, 100);
    ctx.lineTo(400, 100);
    ctx.lineTo(600, 100);
    ctx.lineTo(800, 100);
    ctx.stroke();
    ctx.setLineDash([]);
}

// Charts
function initializeCharts() {
    drawTrafficChart(true);
    drawDensityChart(true);
}

function drawTrafficChart(useHistory=false) {
    const canvas = document.getElementById('trafficChart');
    const ctx = canvas.getContext('2d');
    
    canvas.width = canvas.offsetWidth;
    canvas.height = 300;
    
    let data;
    if (useHistory && trafficHistory.length) {
        data = {
            labels: trafficHistory.map(pt => pt.time.toLocaleTimeString()),
            values: trafficHistory.map(pt => pt.value)
        };
    } else {
        data = {
            labels: ['10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30'],
            values: [180, 220, 195, 240, 280, 260, 290, 270, 250, 247]
        };
    }
    
    drawLineChart(ctx, canvas.width, canvas.height, data);
}

function drawLineChart(ctx, width, height, data) {
    const padding = 50;
    const chartWidth = width - padding * 2;
    const chartHeight = height - padding * 2;
    
    ctx.clearRect(0, 0, width, height);
    
    // Grid
    ctx.strokeStyle = '#e2e8f0';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 5; i++) {
        const y = padding + (chartHeight / 5) * i;
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(width - padding, y);
        ctx.stroke();
    }
    
    // Axes
    ctx.strokeStyle = '#718096';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, height - padding);
    ctx.lineTo(width - padding, height - padding);
    ctx.stroke();
    
    // Y-axis labels
    ctx.fillStyle = '#4a5568';
    ctx.font = '12px Arial';
    ctx.textAlign = 'right';
    const maxValue = Math.max(...data.values);
    for (let i = 0; i <= 5; i++) {
        const value = Math.round((maxValue / 5) * (5 - i));
        const y = padding + (chartHeight / 5) * i;
        ctx.fillText(value, padding - 10, y + 4);
    }
    
    // X-axis labels
    ctx.textAlign = 'center';
    const step = chartWidth / (data.labels.length - 1);
    data.labels.forEach((label, i) => {
        const x = padding + step * i;
        ctx.fillText(label, x, height - padding + 20);
    });
    
    // Draw gradient area
    const gradient = ctx.createLinearGradient(0, padding, 0, height - padding);
    gradient.addColorStop(0, 'rgba(102, 126, 234, 0.3)');
    gradient.addColorStop(1, 'rgba(102, 126, 234, 0.05)');
    
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.moveTo(padding, height - padding);
    data.values.forEach((value, i) => {
        const x = padding + (chartWidth / (data.values.length - 1)) * i;
        const y = height - padding - (value / maxValue) * chartHeight;
        ctx.lineTo(x, y);
    });
    ctx.lineTo(width - padding, height - padding);
    ctx.closePath();
    ctx.fill();
    
    // Draw line
    ctx.strokeStyle = '#667eea';
    ctx.lineWidth = 3;
    ctx.beginPath();
    data.values.forEach((value, i) => {
        const x = padding + (chartWidth / (data.values.length - 1)) * i;
        const y = height - padding - (value / maxValue) * chartHeight;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });
    ctx.stroke();
    
    // Draw points
    ctx.fillStyle = '#667eea';
    data.values.forEach((value, i) => {
        const x = padding + (chartWidth / (data.values.length - 1)) * i;
        const y = height - padding - (value / maxValue) * chartHeight;
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fill();
    });
}

function drawDensityChart(useHistory=false) {
    const canvas = document.getElementById('densityChart');
    const ctx = canvas.getContext('2d');
    
    canvas.width = canvas.offsetWidth;
    canvas.height = 300;
    
    let data;
    if (useHistory && densityHistory.length) {
        // compute distribution percentages
        const counts = {Low:0,Medium:0,High:0};
        densityHistory.forEach(pt=>{ counts[pt.value] = (counts[pt.value]||0)+1; });
        const total = densityHistory.length;
        data = [
            { label: 'Low', value: Math.round((counts.Low/total)*100), color: '#48bb78' },
            { label: 'Medium', value: Math.round((counts.Medium/total)*100), color: '#ed8936' },
            { label: 'High', value: Math.round((counts.High/total)*100), color: '#f56565' }
        ];
    } else {
        data = [
            { label: 'Low', value: 35, color: '#48bb78' },
            { label: 'Medium', value: 45, color: '#ed8936' },
            { label: 'High', value: 20, color: '#f56565' }
        ];
    }
    
    drawBarChart(ctx, canvas.width, canvas.height, data);
}

function drawBarChart(ctx, width, height, data) {
    const padding = 50;
    const chartWidth = width - padding * 2;
    const chartHeight = height - padding * 2;
    
    ctx.clearRect(0, 0, width, height);
    
    // Axes
    ctx.strokeStyle = '#718096';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, height - padding);
    ctx.lineTo(width - padding, height - padding);
    ctx.stroke();
    
    // Draw bars
    const barWidth = chartWidth / data.length - 40;
    const maxValue = 100;
    
    data.forEach((item, i) => {
        const x = padding + (chartWidth / data.length) * i + 20;
        const barHeight = (item.value / maxValue) * chartHeight;
        const y = height - padding - barHeight;
        
        // Bar
        ctx.fillStyle = item.color;
        ctx.fillRect(x, y, barWidth, barHeight);
        
        // Label
        ctx.fillStyle = '#4a5568';
        ctx.font = '14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(item.label, x + barWidth / 2, height - padding + 20);
        
        // Value
        ctx.fillStyle = '#2d3748';
        ctx.font = 'bold 16px Arial';
        ctx.fillText(item.value + '%', x + barWidth / 2, y - 10);
    });
}

// Signal Timers
function startSignalTimers() {
    setInterval(() => {
        Object.keys(signalTimers).forEach(lane => {
            signalTimers[lane]--;
            if (signalTimers[lane] <= 0) {
                signalTimers[lane] = Math.floor(Math.random() * 30) + 30;
            }
            
            const timerEl = document.getElementById(`timer${lane}`);
            const progressEl = document.getElementById(`progress${lane}`);
            
            if (timerEl) timerEl.textContent = signalTimers[lane] + 's';
            if (progressEl) {
                const percentage = (signalTimers[lane] / 60) * 100;
                progressEl.style.width = percentage + '%';
            }
        });
    }, 1000);
}

// Data Updates - fetch from backend API
async function fetchSystemState() {
    const statusEl = document.getElementById('backendStatus');
    try {
        const url = `http://localhost:5000/api/system-state`;
        const res = await fetch(url);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        updateDashboard(data);
        if (statusEl) {
            statusEl.textContent = 'Connected';
            statusEl.classList.remove('disconnected');
            statusEl.classList.add('connected');
        }
    } catch (err) {
        console.warn('Could not fetch system state from API, trying direct file', err);
        if (statusEl) {
            statusEl.textContent = 'Disconnected';
            statusEl.classList.remove('connected');
            statusEl.classList.add('disconnected');
        }
        // try loading JSON file directly (served by same http server)
        try {
            const res2 = await fetch('system_state.json');
            if (res2.ok) {
                const data2 = await res2.json();
                updateDashboard(data2);
                return;
            }
        } catch (e) {
            console.warn('Direct file fetch failed', e);
        }
        // still here? use random fallback
        simulateDataUpdate();
    }
}

function startDataUpdates() {
    // initial fetch
    fetchSystemState();
    setInterval(fetchSystemState, 5000);
}

// keep the original random-updater as a fallback
function simulateDataUpdate() {
    const vehicleCount = Math.floor(Math.random() * 200) + 1100;
    const densities = ['Low', 'Medium', 'High'];
    const randomDensity = densities[Math.floor(Math.random() * densities.length)];

    // sometimes simulate an emergency event
    const isEmergency = Math.random() < 0.1; // 10% chance
    const dummy = {
        vehicle_count: vehicleCount,
        traffic_density: randomDensity,
        emergency_detected: isEmergency,
        emergency_type: isEmergency ? 'ambulance' : null,
        green_wave_route: isEmergency ? ['A','B','C','D'] : [],
        signal_timings: {
            A: { green_time: isEmergency ? 90 : 30, is_priority: true },
            B: { green_time: 45, is_priority: false },
            C: { green_time: 20, is_priority: false },
            D: { green_time: 60, is_priority: false }
        },
        lane_distribution: { 'Lane A': 2, 'Lane B': 1, 'Lane C': 0, 'Lane D': 0 }
    };

    updateDashboard(dummy);
    addLogEntry();
}

// analytics history
let trafficHistory = [];
let densityHistory = [];

function updateAnalytics(data) {
    const now = new Date();
    trafficHistory.push({time: now, value: data.vehicle_count});
    densityHistory.push({time: now, value: data.traffic_density});
    if (trafficHistory.length > 20) trafficHistory.shift();
    if (densityHistory.length > 20) densityHistory.shift();
    drawTrafficChart(true);
    drawDensityChart(true);
}

function updateEmergency(data) {
    const list = document.querySelector('.emergency-list');
    const countBadge = document.querySelector('.count-badge');
    if (!list) return;
    list.innerHTML = '';
    if (data.emergency_detected) {
        const item = document.createElement('div');
        item.className = 'emergency-item active';
        item.innerHTML = `
            <div class="emergency-icon">🚑</div>
            <div class="emergency-info">
                <div class="emergency-title">${data.emergency_type || 'Unknown'}</div>
                <div class="emergency-route">Route: ${data.green_wave_route ? data.green_wave_route.join(' → ') : 'N/A'}</div>
                <div class="emergency-eta">ETA: --</div>
            </div>
            <div class="emergency-status">
                <span class="status-badge active">Active</span>
            </div>
        `;
        list.appendChild(item);
        if (countBadge) countBadge.textContent = '1';
        // update green wave visual nodes based on route
        const pathContainer = document.querySelector('.wave-path');
        if (pathContainer && data.green_wave_route) {
            pathContainer.innerHTML = '';
            data.green_wave_route.forEach((node, idx) => {
                const nodeEl = document.createElement('div');
                nodeEl.className = 'wave-node active';
                nodeEl.textContent = node;
                pathContainer.appendChild(nodeEl);
                if (idx < data.green_wave_route.length - 1) {
                    const conn = document.createElement('div');
                    conn.className = 'wave-connector active';
                    pathContainer.appendChild(conn);
                }
            });
        }
    } else {
        const noEl = document.createElement('div');
        noEl.textContent = 'No active emergencies';
        noEl.style.padding = '1rem';
        list.appendChild(noEl);
        if (countBadge) countBadge.textContent = '0';
    }
}

function updateDashboard(data) {
    // update KPIs
    document.getElementById('vehicles').textContent = data.vehicle_count.toLocaleString();
    document.getElementById('density').textContent = data.traffic_density;
    document.getElementById('emergency').textContent = data.emergency_detected ? 'Active' : 'None';
    // update signal mode
    const modeEl = document.getElementById('mode');
    if (modeEl) {
        modeEl.textContent = data.emergency_detected ? 'Emergency' : 'Adaptive';
    }

    // update lane distribution list if available
    const laneList = document.getElementById('laneDistributionList');
    if (laneList && data.lane_distribution) {
        laneList.innerHTML = '';
        Object.entries(data.lane_distribution).forEach(([lane,count]) => {
            const li = document.createElement('li');
            li.textContent = `${lane}: ${count}`;
            laneList.appendChild(li);
        });
    }
    // update signal timers from backend timings
    if (data.signal_timings) {
        Object.keys(data.signal_timings).forEach(lane => {
            const timing = data.signal_timings[lane];
            const timerEl = document.getElementById(`timer${lane}`);
            const progressEl = document.getElementById(`progress${lane}`);
            if (timerEl) timerEl.textContent = timing.green_time + 's';
            if (progressEl) {
                const percentage = Math.min((timing.green_time / 90) * 100, 100);
                progressEl.style.width = percentage + '%';
            }
        });
    }

    // emergency banner
    const banner = document.getElementById('alertBanner');
    if (data.emergency_detected) {
        banner.style.display = 'flex';
        const routeSpan = banner.querySelector('.route-path');
        if (routeSpan && data.green_wave_route) {
            // rebuild route text
            const pathHtml = data.green_wave_route.map((p, idx) => {
                return `<span class=\"route-path\">${p}</span>${idx < data.green_wave_route.length-1 ? '<span class=\"route-arrow\">→</span>' : ''}`;
            }).join('');
            banner.querySelector('.alert-route').innerHTML = `<span class=\"route-badge\">Route:</span> ${pathHtml}`;
        }
    } else {
        banner.style.display = 'none';
    }

    addLogEntry();
}

// Sliders
function initializeSliders() {
    const sliders = document.querySelectorAll('.control-slider');
    sliders.forEach(slider => {
        const valueDisplay = slider.nextElementSibling;
        slider.addEventListener('input', (e) => {
            valueDisplay.textContent = e.target.value + 's';
        });
    });
}

// Log Filters
function initializeLogFilters() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const logEntries = document.querySelectorAll('.log-entry');
    
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const filter = btn.getAttribute('data-filter');
            
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            logEntries.forEach(entry => {
                if (filter === 'all' || entry.classList.contains(filter)) {
                    entry.style.display = 'flex';
                } else {
                    entry.style.display = 'none';
                }
            });
        });
    });
}

// Add Log Entry
function addLogEntry() {
    const logsContainer = document.getElementById('logsContainer');
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', { hour12: false });
    
    const types = ['emergency', 'signal', 'system'];
    const messages = {
        emergency: ['Emergency vehicle detected', 'Green wave activated', 'Priority route cleared'],
        signal: ['Signal timing adjusted', 'Lane status updated', 'Traffic flow optimized'],
        system: ['System health check completed', 'AI optimization applied', 'Data synchronized']
    };
    
    const randomType = types[Math.floor(Math.random() * types.length)];
    const randomMessage = messages[randomType][Math.floor(Math.random() * messages[randomType].length)];
    
    const icons = { emergency: '🚨', signal: '🚥', system: '⚙️' };
    
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${randomType}`;
    logEntry.innerHTML = `
        <span class="log-icon">${icons[randomType]}</span>
        <span class="log-time">${timeString}</span>
        <span class="log-type">${randomType.toUpperCase()}</span>
        <span class="log-message">${randomMessage}</span>
    `;
    
    logsContainer.insertBefore(logEntry, logsContainer.firstChild);
    
    while (logsContainer.children.length > 20) {
        logsContainer.removeChild(logsContainer.lastChild);
    }
}

// Window resize handler
window.addEventListener('resize', () => {
    initializeCharts();
});
