/**
 * Traffic Density & Lane Analysis Module
 * Core Simulation Engine - Refined for realistic density
 */

const canvas = document.getElementById('trafficCanvas');
const ctx = canvas.getContext('2d');

// Simulation Constants
const CANV_WIDTH = 800;
const CANV_HEIGHT = 400;
const LANE_WIDTH = 200;

// Requested Improvements
const SPAWN_INTERVAL_RANGE = [30, 90]; // 0.5s to 1.5s at 60fps
const SPEED_REDUCTION_FACTOR = 0.65; // ~35% reduction from original speeds

const VEHICLE_TYPES = {
    car: { width: 30, height: 50, speed: 1.0 * SPEED_REDUCTION_FACTOR, color: '#38bdf8' },
    bike: { width: 15, height: 30, speed: 1.4 * SPEED_REDUCTION_FACTOR, color: '#fb7185' },
    bus: { width: 45, height: 90, speed: 0.6 * SPEED_REDUCTION_FACTOR, color: '#fbbf24' },
    truck: { width: 40, height: 80, speed: 0.5 * SPEED_REDUCTION_FACTOR, color: '#a78bfa' }
};

// Application State
let vehicles = [];
let vehicleCounter = 0;
let lastAnalysisTime = 0;
let nextSpawnFrames = [0, 0, 0, 0]; // Frames until next spawn for each lane

let analysisData = {
    LaneA: 0,
    LaneB: 0,
    LaneC: 0,
    LaneD: 0,
    TotalVehicles: 0,
    DensityStatus: {
        LaneA: "LOW",
        LaneB: "LOW",
        LaneC: "LOW",
        LaneD: "LOW"
    }
};

class Vehicle {
    constructor(id, type, x, y) {
        this.id = id;
        this.type = type;
        this.config = VEHICLE_TYPES[type];
        this.width = this.config.width;
        this.height = this.config.height;
        this.x = x;
        this.y = y;
        this.speed = this.config.speed * (0.8 + Math.random() * 0.4);
        this.baseSpeed = this.speed;
        this.color = this.config.color;
    }

    update() {
        this.y += this.speed;

        // Reset speed if slowed down
        if (this.speed < this.baseSpeed) {
            this.speed += 0.02;
        }

        // Keep distance from vehicle ahead (simple collision avoidance)
        for (let other of vehicles) {
            if (other.id !== this.id && 
                Math.abs(other.x - this.x) < 30 && 
                other.y > this.y && 
                other.y - this.y < this.height + 25) {
                this.speed = Math.max(0, other.speed - 0.05);
            }
        }
    }

    draw() {
        // Draw shadowed body
        ctx.fillStyle = 'rgba(0,0,0,0.3)';
        ctx.fillRect(this.x - this.width/2 + 4, this.y + 4, this.width, this.height);

        // Draw main body
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x - this.width/2, this.y, this.width, this.height);

        // Details (windshield)
        ctx.fillStyle = 'rgba(255,255,255,0.2)';
        ctx.fillRect(this.x - this.width/2 + 2, this.y + 5, this.width - 4, this.height * 0.15);
        
        // ID Label
        ctx.fillStyle = 'rgba(255,255,255,0.7)';
        ctx.font = '600 10px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(this.id, this.x, this.y - 5);
    }
}

function getLaneName(x) {
    if (x < 200) return 'LaneA';
    if (x < 400) return 'LaneB';
    if (x < 600) return 'LaneC';
    return 'LaneD';
}

function spawnVehicles() {
    for (let lane = 0; lane < 4; lane++) {
        if (nextSpawnFrames[lane] <= 0) {
            const laneCenter = (lane * 200) + 100;
            
            // Allow spawn if the previous vehicle has cleared the -40px mark
            const isClear = vehicles
                .filter(v => Math.abs(v.x - laneCenter) < 10)
                .every(v => v.y > -40); 
            
            if (isClear) {
                const types = Object.keys(VEHICLE_TYPES);
                const type = types[Math.floor(Math.random() * types.length)];
                vehicleCounter++;
                vehicles.push(new Vehicle(vehicleCounter, type, laneCenter, -100));
                
                // Set next spawn time with randomness
                nextSpawnFrames[lane] = SPAWN_INTERVAL_RANGE[0] + Math.random() * (SPAWN_INTERVAL_RANGE[1] - SPAWN_INTERVAL_RANGE[0]);
            }
        } else {
            nextSpawnFrames[lane]--;
        }
    }
}

function calculateDensity(count) {
    // Thresholds: 0-4 LOW, 5-9 MEDIUM, 10+ HIGH
    if (count <= 4) return 'LOW';
    if (count <= 9) return 'MEDIUM';
    return 'HIGH';
}

function runAnalysis() {
    const counts = { LaneA: 0, LaneB: 0, LaneC: 0, LaneD: 0 };
    
    vehicles.forEach(v => {
        if (v.y > 0 && v.y < CANV_HEIGHT) {
            const lane = getLaneName(v.x);
            counts[lane]++;
        }
    });

    analysisData = {
        LaneA: counts.LaneA,
        LaneB: counts.LaneB,
        LaneC: counts.LaneC,
        LaneD: counts.LaneD,
        TotalVehicles: counts.LaneA + counts.LaneB + counts.LaneC + counts.LaneD,
        DensityStatus: {
            LaneA: calculateDensity(counts.LaneA),
            LaneB: calculateDensity(counts.LaneB),
            LaneC: calculateDensity(counts.LaneC),
            LaneD: calculateDensity(counts.LaneD)
        }
    };

    updateUI();
}

function updateUI() {
    ['LaneA', 'LaneB', 'LaneC', 'LaneD'].forEach(lane => {
        const laneId = lane.toLowerCase().replace('lane', 'lane-');
        const statElem = document.getElementById(`${laneId}-stat`);
        if (!statElem) return;

        const countElem = statElem.querySelector('.vehicle-count');
        const chipElem = statElem.querySelector('.density-chip');
        
        const count = analysisData[lane];
        const status = analysisData.DensityStatus[lane];
        
        if (countElem) countElem.innerHTML = `${count} <small>veh</small>`;
        if (chipElem) {
            chipElem.textContent = status;
            chipElem.className = `density-chip status-${status.toLowerCase()}`;
        }
    });

    const totalElem = document.getElementById('totalVehicles');
    if (totalElem) totalElem.textContent = analysisData.TotalVehicles;
    
    const jsonElem = document.getElementById('jsonOutput');
    if (jsonElem) jsonElem.textContent = JSON.stringify(analysisData, null, 2);
}

function drawRoad() {
    // Asphalt
    ctx.fillStyle = '#1e293b';
    ctx.fillRect(0, 0, CANV_WIDTH, CANV_HEIGHT);

    // Density Overlays
    const overlayColors = {
        'LOW': 'rgba(16, 185, 129, 0.05)',
        'MEDIUM': 'rgba(245, 158, 11, 0.12)',
        'HIGH': 'rgba(239, 68, 68, 0.2)'
    };

    ['LaneA', 'LaneB', 'LaneC', 'LaneD'].forEach((lane, idx) => {
        const status = analysisData.DensityStatus[lane];
        ctx.fillStyle = overlayColors[status] || overlayColors.LOW;
        ctx.fillRect(idx * 200, 0, 200, CANV_HEIGHT);
        
        ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.font = '700 14px Outfit, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(lane.replace('Lane', 'LANE '), idx * 200 + 100, 30);
    });

    // Lane Markings
    ctx.strokeStyle = 'rgba(255,255,255,0.1)';
    ctx.setLineDash([20, 20]);
    ctx.lineWidth = 2;
    for (let i = 1; i < 4; i++) {
        ctx.beginPath();
        ctx.moveTo(i * 200, 0);
        ctx.lineTo(i * 200, CANV_HEIGHT);
        ctx.stroke();
    }
    ctx.setLineDash([]);
}

function loop(timestamp) {
    ctx.clearRect(0, 0, CANV_WIDTH, CANV_HEIGHT);
    
    drawRoad();
    spawnVehicles();

    // Filter off-screen vehicles
    vehicles = vehicles.filter(v => v.y < CANV_HEIGHT + 150);

    vehicles.forEach(v => {
        v.update();
        v.draw();
    });

    if (timestamp - lastAnalysisTime > 1000) {
        runAnalysis();
        lastAnalysisTime = timestamp;
    }

    requestAnimationFrame(loop);
}

requestAnimationFrame(loop);
