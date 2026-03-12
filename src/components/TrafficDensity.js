import React, { useState, useEffect } from 'react';
import './TrafficDensity.css';

const TrafficDensity = () => {
  const [densityData, setDensityData] = useState([
    { lane: 'Lane A', density: 65, status: 'Medium', vehicles: 45 },
    { lane: 'Lane B', density: 82, status: 'High', vehicles: 58 },
    { lane: 'Lane C', density: 35, status: 'Low', vehicles: 22 },
    { lane: 'Lane D', density: 48, status: 'Medium', vehicles: 34 }
  ]);

  const [overallDensity, setOverallDensity] = useState(57);

  useEffect(() => {
    const interval = setInterval(() => {
      setDensityData(prev => prev.map(item => ({
        ...item,
        density: Math.max(0, Math.min(100, item.density + Math.floor(Math.random() * 10) - 5)),
        vehicles: Math.max(0, Math.min(80, item.vehicles + Math.floor(Math.random() * 6) - 3))
      })));
      
      const avg = Math.round(
        densityData.reduce((sum, item) => sum + item.density, 0) / densityData.length
      );
      setOverallDensity(avg);
    }, 3000);

    return () => clearInterval(interval);
  }, [densityData]);

  const getStatusColor = (density) => {
    if (density < 40) return '#48bb78';
    if (density < 70) return '#f39c12';
    return '#f56565';
  };

  const getStatusText = (density) => {
    if (density < 40) return 'Low';
    if (density < 70) return 'Medium';
    return 'High';
  };

  return (
    <div className="traffic-density-section">
      <div className="section-header">
        <h1>Traffic Density</h1>
        <p>Real-time traffic density monitoring across all lanes</p>
      </div>

      <div className="density-overview">
        <div className="overall-density">
          <div className="density-gauge">
            <svg viewBox="0 0 200 120">
              <path
                d="M 20 100 A 80 80 0 0 1 180 100"
                fill="none"
                stroke="#e2e8f0"
                strokeWidth="20"
                strokeLinecap="round"
              />
              <path
                d="M 20 100 A 80 80 0 0 1 180 100"
                fill="none"
                stroke={getStatusColor(overallDensity)}
                strokeWidth="20"
                strokeLinecap="round"
                strokeDasharray={`${overallDensity * 2.51} 251`}
                style={{ transition: 'stroke-dasharray 0.5s ease' }}
              />
            </svg>
            <div className="density-value">{overallDensity}%</div>
            <div className="density-label">Overall Density</div>
          </div>
        </div>
      </div>

      <div className="density-grid">
        {densityData.map((item, index) => (
          <div key={index} className="card density-card">
            <div className="density-header">
              <h3>{item.lane}</h3>
              <span 
                className="density-status"
                style={{ background: getStatusColor(item.density) }}
              >
                {getStatusText(item.density)}
              </span>
            </div>
            <div className="density-bar-container">
              <div 
                className="density-bar"
                style={{ 
                  width: `${item.density}%`,
                  background: getStatusColor(item.density)
                }}
              ></div>
            </div>
            <div className="density-info">
              <span>Density: {item.density}%</span>
              <span>Vehicles: {item.vehicles}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="card density-chart">
        <h2>Density Over Time</h2>
        <div className="chart-container">
          <canvas id="densityChart"></canvas>
        </div>
      </div>
    </div>
  );
};

export default TrafficDensity;