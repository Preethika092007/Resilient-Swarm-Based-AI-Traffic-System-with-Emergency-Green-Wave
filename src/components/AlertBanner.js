import React from 'react';
import './AlertBanner.css';

const AlertBanner = () => {
  return (
    <div className="alert-banner">
      <div className="alert-pulse"></div>
      <div className="alert-content">
        <div className="alert-icon"></div>
        <div className="alert-text">
          <strong>Emergency Vehicle Detected – Green Wave Activated</strong>
          <div className="alert-route">
            <span className="route-badge">Route:</span>
            <span className="route-path">Intersection A</span>
            <span className="route-arrow">→</span>
            <span className="route-path">B</span>
            <span className="route-arrow">→</span>
            <span className="route-path">C</span>
            <span className="route-arrow">→</span>
            <span className="route-path">D</span>
          </div>
        </div>
        <button className="alert-action">View Details</button>
      </div>
    </div>
  );
};

export default AlertBanner;
