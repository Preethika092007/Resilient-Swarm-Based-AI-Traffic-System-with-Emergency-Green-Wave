import React, { useState, useEffect } from 'react';
import './Dashboard.css';
import KPICard from './KPICard';
import AlertBanner from './AlertBanner';
import IntersectionCanvas from './IntersectionCanvas';
import SignalStatus from './SignalStatus';
import StatsRow from './StatsRow';

const Dashboard = () => {
  const [vehicleCount, setVehicleCount] = useState(1247);
  const [density, setDensity] = useState('Medium');
  const mode = 'Adaptive';
  const emergency = 'Active';

  useEffect(() => {
    const interval = setInterval(() => {
      setVehicleCount(Math.floor(Math.random() * 200) + 1100);
      const densities = ['Low', 'Medium', 'High'];
      setDensity(densities[Math.floor(Math.random() * densities.length)]);
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard-section">
      <div className="section-header">
        <h1>Traffic Command Dashboard</h1>
        <p>AI-driven adaptive traffic management with emergency green wave system</p>
      </div>

      <div className="kpi-grid">
        <KPICard
          icon="vehicles"
          label="Vehicles Detected"
          value={vehicleCount.toLocaleString()}
          trend="↑ 12% from last hour"
          trendType="positive"
          colorClass="kpi-primary"
        />
        <KPICard
          icon="density"
          label="Traffic Density"
          value={density}
          trend="→ Stable"
          trendType="neutral"
          colorClass="kpi-warning"
        />
        <KPICard
          icon="mode"
          label="Signal Mode"
          value={mode}
          trend="✓ Optimized"
          trendType="positive"
          colorClass="kpi-success"
        />
        <KPICard
          icon="emergency"
          label="Emergency Status"
          value={emergency}
          trend="⚠ Green Wave ON"
          trendType="alert"
          colorClass="kpi-danger"
        />
      </div>

      <AlertBanner />

      <div className="dashboard-grid">
        <IntersectionCanvas />
        <SignalStatus />
      </div>

      <StatsRow />
    </div>
  );
};

export default Dashboard;
