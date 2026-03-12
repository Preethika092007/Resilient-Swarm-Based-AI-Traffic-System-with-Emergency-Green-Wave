import React from 'react';
import './KPICard.css';

const KPICard = ({ icon, label, value, trend, trendType, colorClass }) => {
  return (
    <div className={`kpi-card ${colorClass}`}>
      <div className={`kpi-icon ${icon}`}></div>
      <div className="kpi-content">
        <div className="kpi-label">{label}</div>
        <div className="kpi-value">{value}</div>
        <div className={`kpi-trend ${trendType}`}>{trend}</div>
      </div>
    </div>
  );
};

export default KPICard;
