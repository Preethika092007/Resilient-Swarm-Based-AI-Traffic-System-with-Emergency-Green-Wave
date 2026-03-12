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
    drawTrafficChart();
    drawDensityChart();
}

function drawTrafficChart() {
    const canvas = document.getElementById('trafficChart');
    const ctx = canvas.getContext('2d');
    
    canvas.width = canvas.offsetWidth;
    canvas.height = 300;
    
    const data = {
        labels: ['10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30'],
        values: [180, 220, 195, 240, 280, 260, 290, 270, 250, 247]
    };
    
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

function drawDensityChart() {
    const canvas = document.getElementById('densityChart');
    const ctx = canvas.getContext('2d');
    
    canvas.width = canvas.offsetWidth;
    canvas.height = 300;
    
    const data = [
        { label: 'Low', value: 35, color: '#48bb78' },
        { label: 'Medium', value: 45, color: '#ed8936' },
        { label: 'High', value: 20, color: '#f56565' }
    ];
    
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

// Data Updates
function startDataUpdates() {
    setInterval(() => {
        const vehicleCount = Math.floor(Math.random() * 200) + 1100;
        document.getElementById('vehicles').textContent = vehicleCount.toLocaleString();
        
        const densities = ['Low', 'Medium', 'High'];
        const randomDensity = densities[Math.floor(Math.random() * densities.length)];
        document.getElementById('density').textContent = randomDensity;
        
        addLogEntry();
    }, 5000);
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
