import React, { useState } from 'react';
import './Signals.css';

const Signals = () => {
  const [intersections] = useState([
    { id: 'A', mode: 'Adaptive', cycleTime: 60 },
    { id: 'B', mode: 'Adaptive', cycleTime: 45 },
    { id: 'C', mode: 'Adaptive', cycleTime: 75 },
    { id: 'D', mode: 'Timed', cycleTime: 90 }
  ]);

  const handleSliderChange = (id, value) => {
    // Handle slider change logic
  };

  return (
    <div className="signals-section">
      <div className="section-header">
        <h1>Signal Control</h1>
        <p>Manage and monitor all traffic signals</p>
      </div>
      <div className="signals-grid">
        {intersections.map(intersection => (
          <div key={intersection.id} className="signal-control-card">
            <div className="signal-control-header">
              <h3>Intersection {intersection.id}</h3>
              <button className="btn-primary">Override</button>
            </div>
            <div className="signal-control-body">
              <div className="control-row">
                <span>Mode:</span>
                <select className="control-select">
                  <option>Adaptive</option>
                  <option>Manual</option>
                  <option>Timed</option>
                </select>
              </div>
              <div className="control-row">
                <span>Cycle Time:</span>
                <input
                  type="range"
                  min="30"
                  max="120"
                  defaultValue={intersection.cycleTime}
                  className="control-slider"
                  onChange={(e) => handleSliderChange(intersection.id, e.target.value)}
                />
                <span className="control-value">{intersection.cycleTime}s</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Signals;