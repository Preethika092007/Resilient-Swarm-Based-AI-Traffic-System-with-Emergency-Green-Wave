import React, { useState, useEffect } from 'react';
import './GreenWave.css';

const GreenWave = () => {
  const [route, setRoute] = useState({
    start: 'A',
    end: 'D',
    path: ['A', 'B', 'C', 'D'],
    status: 'active',
    eta: '2.5 min'
  });

  const [signalStates, setSignalStates] = useState({
    A: 'green',
    B: 'green',
    C: 'yellow',
    D: 'red'
  });

  const [vehiclePosition, setVehiclePosition] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setSignalStates(prev => {
        const newStates = { ...prev };
        const keys = Object.keys(newStates);
        const currentIndex = keys.findIndex(k => newStates[k] === 'green');
        
        if (currentIndex >= 0 && currentIndex < keys.length - 1) {
          newStates[keys[currentIndex]] = 'red';
          newStates[keys[currentIndex + 1]] = 'green';
        } else if (currentIndex === keys.length - 1) {
          newStates[keys[currentIndex]] = 'red';
          newStates[keys[0]] = 'green';
        }
        
        return newStates;
      });

      setVehiclePosition(prev => (prev + 1) % 4);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const intersections = [
    { id: 'A', name: 'Main Street', coordinates: '12.9716, 77.5946' },
    { id: 'B', name: 'Central Ave', coordinates: '12.9721, 77.5951' },
    { id: 'C', name: 'Oak Boulevard', coordinates: '12.9726, 77.5956' },
    { id: 'D', name: 'Pine Road', coordinates: '12.9731, 77.5961' }
  ];

  return (
    <div className="green-wave-section">
      <div className="section-header">
        <h1>Green Wave Route Simulation</h1>
        <p>Emergency vehicle green wave corridor management</p>
      </div>

      <div className="route-overview">
        <div className="card route-card">
          <h2>Active Route</h2>
          <div className="route-path">
            {intersections.map((intersection, index) => (
              <React.Fragment key={intersection.id}>
                <div className={`route-node ${signalStates[intersection.id]}`}>
                  <div className="node-id">{intersection.id}</div>
                  <div className="node-signal">
                    <span className={`signal-dot ${signalStates[intersection.id]}`}></span>
                  </div>
                  <div className="node-name">{intersection.name}</div>
                </div>
                {index < intersections.length - 1 && (
                  <div className="route-connector">
                    <div className="connector-line"></div>
                    <div className="connector-vehicle"></div>
                  </div>
                )}
              </React.Fragment>
            ))}
          </div>
          <div className="route-info">
            <div className="info-item">
              <span className="info-label">Status</span>
              <span className="info-value active">{route.status.toUpperCase()}</span>
            </div>
            <div className="info-item">
              <span className="info-label">ETA</span>
              <span className="info-value">{route.eta}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Distance</span>
              <span className="info-value">1.2 km</span>
            </div>
          </div>
        </div>
      </div>

      <div className="wave-grid">
        <div className="card signal-control">
          <h2>Signal Timing</h2>
          <div className="timing-list">
            {intersections.map(intersection => (
              <div key={intersection.id} className="timing-item">
                <div className="timing-header">
                  <span className="timing-id">{intersection.id}</span>
                  <span className="timing-name">{intersection.name}</span>
                </div>
                <div className="timing-controls">
                  <button className="timing-btn">-</button>
                  <span className="timing-value">45s</span>
                  <button className="timing-btn">+</button>
                </div>
                <div className={`timing-status ${signalStates[intersection.id]}`}>
                  {signalStates[intersection.id].toUpperCase()}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="card wave-map">
          <h2>Route Map</h2>
          <div className="map-container">
            <div className="map-visual">
              <div className="map-road vertical"></div>
              <div className="map-road horizontal"></div>
              {intersections.map((intersection, index) => (
                <div 
                  key={intersection.id}
                  className={`map-intersection ${signalStates[intersection.id]} ${index === vehiclePosition ? 'active' : ''}`}
                  style={{
                    top: index % 2 === 0 ? '20%' : '60%',
                    left: index % 2 === 0 ? '30%' : '70%'
                  }}
                >
                  <span className="intersection-label">{intersection.id}</span>
                </div>
              ))}
              <div className="emergency-vehicle"></div>
            </div>
          </div>
        </div>
      </div>

      <div className="card history-log">
        <h2>Recent Activations</h2>
        <div className="history-list">
          <div className="history-item">
            <span className="history-time">14:32:15</span>
            <span className="history-route">A → B → C → D</span>
            <span className="history-type">Ambulance</span>
            <span className="history-status completed">Completed</span>
          </div>
          <div className="history-item">
            <span className="history-time">13:15:42</span>
            <span className="history-route">B → C → D</span>
            <span className="history-type">Fire Truck</span>
            <span className="history-status completed">Completed</span>
          </div>
          <div className="history-item">
            <span className="history-time">11:45:23</span>
            <span className="history-route">A → B</span>
            <span className="history-type">Police</span>
            <span className="history-status completed">Completed</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GreenWave;