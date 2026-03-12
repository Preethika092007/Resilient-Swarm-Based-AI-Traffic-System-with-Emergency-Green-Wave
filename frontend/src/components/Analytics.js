import React, { useEffect, useRef } from 'react';
import './Analytics.css';

const Analytics = () => {
  const trafficChartRef = useRef(null);
  const densityChartRef = useRef(null);

  useEffect(() => {
    drawTrafficChart();
    drawDensityChart();
  }, []);

  const drawTrafficChart = () => {
    const canvas = trafficChartRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth;
    canvas.height = 300;

    const data = {
      labels: ['10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30'],
      values: [180, 220, 195, 240, 280, 260, 290, 270, 250, 247]
    };

    const padding = 50;
    const chartWidth = canvas.width - padding * 2;
    const chartHeight = canvas.height - padding * 2;
    const maxValue = Math.max(...data.values);

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Grid
    ctx.strokeStyle = '#e2e8f0';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 5; i++) {
      const y = padding + (chartHeight / 5) * i;
      ctx.beginPath();
      ctx.moveTo(padding, y);
      ctx.lineTo(canvas.width - padding, y);
      ctx.stroke();
    }

    // Axes
    ctx.strokeStyle = '#718096';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, canvas.height - padding);
    ctx.lineTo(canvas.width - padding, canvas.height - padding);
    ctx.stroke();

    // Y-axis labels
    ctx.fillStyle = '#4a5568';
    ctx.font = '12px Arial';
    ctx.textAlign = 'right';
    for (let i = 0; i <= 5; i++) {
      const value = Math.round((maxValue / 5) * (5 - i));
      const y = padding + (chartHeight / 5) * i;
      ctx.fillText(value, padding - 10, y + 4);
    }

    // X-axis labels
    ctx.textAlign = 'center';
    const step = chartWidth / (data.labels.length - 1);
    data.labels.forEach((label, i) => {
      const x = padding + step * i;
      ctx.fillText(label, x, canvas.height - padding + 20);
    });

    // Gradient area
    const gradient = ctx.createLinearGradient(0, padding, 0, canvas.height - padding);
    gradient.addColorStop(0, 'rgba(102, 126, 234, 0.3)');
    gradient.addColorStop(1, 'rgba(102, 126, 234, 0.05)');
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.moveTo(padding, canvas.height - padding);
    data.values.forEach((value, i) => {
      const x = padding + (chartWidth / (data.values.length - 1)) * i;
      const y = canvas.height - padding - (value / maxValue) * chartHeight;
      ctx.lineTo(x, y);
    });
    ctx.lineTo(canvas.width - padding, canvas.height - padding);
    ctx.closePath();
    ctx.fill();

    // Line
    ctx.strokeStyle = '#667eea';
    ctx.lineWidth = 3;
    ctx.beginPath();
    data.values.forEach((value, i) => {
      const x = padding + (chartWidth / (data.values.length - 1)) * i;
      const y = canvas.height - padding - (value / maxValue) * chartHeight;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();

    // Points
    ctx.fillStyle = '#667eea';
    data.values.forEach((value, i) => {
      const x = padding + (chartWidth / (data.values.length - 1)) * i;
      const y = canvas.height - padding - (value / maxValue) * chartHeight;
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, Math.PI * 2);
      ctx.fill();
    });
  };

  const drawDensityChart = () => {
    const canvas = densityChartRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width = canvas.offsetWidth;
    canvas.height = 300;

    const data = [
      { label: 'Low', value: 35, color: '#48bb78' },
      { label: 'Medium', value: 45, color: '#ed8936' },
      { label: 'High', value: 20, color: '#f56565' }
    ];

    const padding = 50;
    const chartWidth = canvas.width - padding * 2;
    const chartHeight = canvas.height - padding * 2;
    const barWidth = chartWidth / data.length - 40;
    const maxValue = 100;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Axes
    ctx.strokeStyle = '#718096';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, canvas.height - padding);
    ctx.lineTo(canvas.width - padding, canvas.height - padding);
    ctx.stroke();

    // Bars
    data.forEach((item, i) => {
      const x = padding + (chartWidth / data.length) * i + 20;
      const barHeight = (item.value / maxValue) * chartHeight;
      const y = canvas.height - padding - barHeight;

      ctx.fillStyle = item.color;
      ctx.fillRect(x, y, barWidth, barHeight);

      ctx.fillStyle = '#4a5568';
      ctx.font = '14px Arial';
      ctx.textAlign = 'center';
      ctx.fillText(item.label, x + barWidth / 2, canvas.height - padding + 20);

      ctx.fillStyle = '#2d3748';
      ctx.font = 'bold 16px Arial';
      ctx.fillText(item.value + '%', x + barWidth / 2, y - 10);
    });
  };

  return (
    <div className="analytics-section">
      <div className="section-header">
        <h1>Traffic Analytics</h1>
        <p>Historical data and trends</p>
      </div>
      <div className="analytics-grid">
        <div className="card chart-card">
          <div className="card-header">
            <h2>Vehicle Count Over Time</h2>
            <select className="chart-filter">
              <option>Last Hour</option>
              <option>Last 6 Hours</option>
              <option>Last 24 Hours</option>
              <option>Last Week</option>
            </select>
          </div>
          <canvas ref={trafficChartRef}></canvas>
        </div>
        <div className="card chart-card">
          <div className="card-header">
            <h2>Traffic Density Distribution</h2>
          </div>
          <canvas ref={densityChartRef}></canvas>
        </div>
      </div>
    </div>
  );
};

export default Analytics;