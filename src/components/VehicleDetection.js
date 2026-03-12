import React, { useState, useEffect } from 'react';
import './VehicleDetection.css';

const VehicleDetection = () => {
  const [detections, setDetections] = useState([
    { id: 1, type: 'Car', lane: 'A', confidence: 98, timestamp: '14:32:15' },
    { id: 2, type: 'Bike', lane: 'B', confidence: 95, timestamp: '14:32:16' },
    { id: 3, type: 'Car', lane: 'A', confidence: 97, timestamp: '14:32:17' },
    { id: 4, type: 'Truck', lane: 'C', confidence: 92, timestamp: '14:32:18' },
    { id: 5, type: 'Car', lane: 'D', confidence: 99, timestamp: '14:32:19' }
  ]);

  const [stats, setStats] = useState({
    total: 1247,
    cars: 892,
    bikes: 245,
    trucks: 110
  });

  useEffect(() => {
    const interval = setInterval(() => {
      const types = ['Car', 'Bike', 'Truck', 'Bus'];
      const lanes = ['A', 'B', 'C', 'D'];
      
      const newDetection = {
        id: Date.now(),
        type: types[Math.floor(Math.random() * types.length)],
        lane: lanes[Math.floor(Math.random() * lanes.length)],
        confidence: Math.floor(Math.random() * 10) + 90,
        timestamp: new Date().toLocaleTimeString('en-US', { hour12: false })
      };

      setDetections(prev => [newDetection, ...prev].slice(0, 10));
      setStats(prev => ({
        ...prev,
        total: prev.total + 1,
        [newDetection.type.toLowerCase() + 's']: prev[newDetection.type.toLowerCase() + 's'] + 1
      }));
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="vehicle-detection-section">
      <div className="section-header">
        <h1>Vehicle Detection</h1>
        <p>Real-time vehicle detection and classification using AI</p>
      </div>

      <div className="detection-stats">
        <div className="stat-box">
          <div className="stat-value">{stats.total.toLocaleString()}</div>
          <div className="stat-label">Total Detections</div>
        </div>
        <div className="stat-box">
          <div className="stat-value">{stats.cars}</div>
          <div className="stat-label">Cars</div>
        </div>
        <div className="stat-box">
          <div className="stat-value">{stats.bikes}</div>
          <div className="stat-label">Bikes</div>
        </div>
        <div className="stat-box">
          <div className="stat-value">{stats.trucks}</div>
          <div className="stat-label">Trucks</div>
        </div>
      </div>

      <div className="detection-grid">
        <div className="card detection-canvas">
          <h2>Live Detection Feed</h2>
          <div className="video-feed">
            <div className="video-placeholder">
              <div className="detection-overlay">
                <div className="detection-box car" style={{ top: '30%', left: '40%' }}>
                  <span>Car 98%</span>
                </div>
                <div className="detection-box bike" style={{ top: '50%', left: '60%' }}>
                  <span>Bike 95%</span>
                </div>
                <div className="detection-box car" style={{ top: '70%', left: '35%' }}>
                  <span>Car 97%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="card detection-log">
          <h2>Recent Detections</h2>
          <div className="detection-list">
            {detections.map(detection => (
              <div key={detection.id} className="detection-item">
                <div className="detection-type">{detection.type}</div>
                <div className="detection-lane">Lane {detection.lane}</div>
                <div className="detection-confidence">{detection.confidence}%</div>
                <div className="detection-time">{detection.timestamp}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default VehicleDetection;