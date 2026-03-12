import React, { useState } from 'react';
import './Settings.css';

const Settings = () => {
  const [notifications, setNotifications] = useState(true);
  const [darkMode, setDarkMode] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [refreshInterval, setRefreshInterval] = useState(5);

  return (
    <div className="settings-section">
      <div className="section-header">
        <h1>Settings</h1>
        <p>Configure your dashboard preferences</p>
      </div>

      <div className="settings-grid">
        <div className="card settings-card">
          <h2>Notifications</h2>
          <div className="setting-item">
            <div className="setting-info">
              <h3>Push Notifications</h3>
              <p>Receive alerts for emergency vehicles</p>
            </div>
            <label className="toggle">
              <input
                type="checkbox"
                checked={notifications}
                onChange={() => setNotifications(!notifications)}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>
        </div>

        <div className="card settings-card">
          <h2>Display</h2>
          <div className="setting-item">
            <div className="setting-info">
              <h3>Dark Mode</h3>
              <p>Switch to dark theme</p>
            </div>
            <label className="toggle">
              <input
                type="checkbox"
                checked={darkMode}
                onChange={() => setDarkMode(!darkMode)}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>
        </div>

        <div className="card settings-card">
          <h2>Data Refresh</h2>
          <div className="setting-item">
            <div className="setting-info">
              <h3>Auto Refresh</h3>
              <p>Automatically update dashboard data</p>
            </div>
            <label className="toggle">
              <input
                type="checkbox"
                checked={autoRefresh}
                onChange={() => setAutoRefresh(!autoRefresh)}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>
          {autoRefresh && (
            <div className="setting-detail">
              <label>Refresh Interval (seconds)</label>
              <input
                type="number"
                min="1"
                max="60"
                value={refreshInterval}
                onChange={(e) => setRefreshInterval(e.target.value)}
                className="interval-input"
              />
            </div>
          )}
        </div>

        <div className="card settings-card">
          <h2>System</h2>
          <div className="setting-item">
            <div className="setting-info">
              <h3>Version</h3>
              <p>Smart Traffic Control v1.0.0</p>
            </div>
          </div>
          <div className="setting-item">
            <div className="setting-info">
              <h3>Clear Cache</h3>
              <p>Clear cached data</p>
            </div>
            <button className="action-btn">Clear</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;