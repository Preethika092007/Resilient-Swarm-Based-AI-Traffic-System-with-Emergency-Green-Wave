import React from 'react';
import './Emergency.css';

const Emergency = () => {
  const emergencyVehicles = [
    { id: 'A-247', type: 'Ambulance', route: 'A → B → C → D', eta: '4 minutes', status: 'Active' },
    { id: 'F-103', type: 'Fire Truck', route: 'E → F → G', eta: '7 minutes', status: 'Active' }
  ];

  return (
    <div className="emergency-section">
      <div className="section-header">
        <h1>Emergency Management</h1>
        <p>Emergency vehicle tracking and green wave control</p>
      </div>
      <div className="emergency-grid">
        <div className="card emergency-card">
          <div className="card-header">
            <h2>Active Emergency Vehicles</h2>
            <span className="count-badge">2</span>
          </div>
          <div className="emergency-list">
            {emergencyVehicles.map((vehicle, index) => (
              <div key={index} className="emergency-item active">
                <div className={`emergency-icon ${vehicle.type.toLowerCase().replace(' ', '-')}`}></div>
                <div className="emergency-info">
                  <div className="emergency-title">{vehicle.type} #{vehicle.id}</div>
                  <div className="emergency-route">Route: {vehicle.route}</div>
                  <div className="emergency-eta">ETA: {vehicle.eta}</div>
                </div>
                <div className="emergency-status">
                  <span className="status-badge active">{vehicle.status}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="card">
          <div className="card-header">
            <h2>Green Wave Status</h2>
          </div>
          <div className="green-wave-visual">
            <div className="wave-path">
              <div className="wave-node active">A</div>
              <div className="wave-connector active"></div>
              <div className="wave-node active">B</div>
              <div className="wave-connector active"></div>
              <div className="wave-node active">C</div>
              <div className="wave-connector"></div>
              <div className="wave-node">D</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Emergency;