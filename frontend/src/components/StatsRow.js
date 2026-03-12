import React from 'react';
import './StatsRow.css';

const StatsRow = () => {
  const stats = [
    { icon: 'time', value: '2.3 min', label: 'Avg Wait Time' },
    { icon: 'efficiency', value: '94.2%', label: 'Efficiency' },
    { icon: 'signals', value: '12', label: 'Active Signals' },
    { icon: 'alerts', value: '3', label: 'Alerts Today' }
  ];

  return (
    <div className="stats-row">
      {stats.map((stat, index) => (
        <div key={index} className="stat-card">
          <div className={`stat-icon ${stat.icon}`}></div>
          <div className="stat-info">
            <div className="stat-value">{stat.value}</div>
            <div className="stat-label">{stat.label}</div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default StatsRow;