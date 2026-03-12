import React from 'react';
import './Landing.css';

const Landing = ({ onGetStarted }) => {
  return (
    <div className="landing-page">
      <div className="landing-hero">
        <div className="hero-content">
          <h1>Smart City Traffic Command</h1>
          <p className="hero-subtitle">
            AI-driven adaptive traffic management with emergency green wave system
          </p>
          <div className="hero-stats">
            <div className="hero-stat">
              <span className="stat-number">1,247</span>
              <span className="stat-label">Vehicles Tracked</span>
            </div>
            <div className="hero-stat">
              <span className="stat-number">12</span>
              <span className="stat-label">Active Intersections</span>
            </div>
            <div className="hero-stat">
              <span className="stat-number">94.2%</span>
              <span className="stat-label">Efficiency Rate</span>
            </div>
          </div>
          <button className="get-started-btn" onClick={onGetStarted}>
            Enter Dashboard
          </button>
        </div>
        <div className="hero-visual">
          <div className="traffic-animation">
            <div className="road-vertical"></div>
            <div className="road-horizontal"></div>
            <div className="signal-center">
              <div className="signal-light red"></div>
              <div className="signal-light yellow"></div>
              <div className="signal-light green"></div>
            </div>
            <div className="vehicle vehicle-car-1"></div>
            <div className="vehicle vehicle-car-2"></div>
            <div className="vehicle vehicle-bike-1"></div>
            <div className="vehicle vehicle-bike-2"></div>
          </div>
        </div>
      </div>
      
      <div className="features-section">
        <h2>Key Features</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon"></div>
            <h3>Real-time Monitoring</h3>
            <p>Live traffic tracking across all city intersections with instant updates</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon"></div>
            <h3>Emergency Response</h3>
            <p>Automatic green wave activation for emergency vehicles</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon"></div>
            <h3>Smart Analytics</h3>
            <p>AI-powered traffic flow optimization and predictions</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon"></div>
            <h3>Signal Control</h3>
            <p>Adaptive signal timing based on real-time conditions</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Landing;