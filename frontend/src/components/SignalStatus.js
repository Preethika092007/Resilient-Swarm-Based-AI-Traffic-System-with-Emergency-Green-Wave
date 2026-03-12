import React, { useState, useEffect } from 'react';
import './SignalStatus.css';

const SignalStatus = () => {
  const [timers, setTimers] = useState({ A: 45, B: 30, C: 15, D: 60 });

  useEffect(() => {
    const interval = setInterval(() => {
      setTimers(prev => {
        const updated = { ...prev };
        Object.keys(updated).forEach(lane => {
          updated[lane]--;
          if (updated[lane] <= 0) {
            updated[lane] = Math.floor(Math.random() * 30) + 30;
          }
        });
        return updated;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const getProgress = (seconds) => Math.min((seconds / 60) * 100, 100);

  const signals = [
    { lane: 'A', name: 'Lane A (North)', color: 'green', status: 'Green - Active' },
    { lane: 'B', name: 'Lane B (East)', color: 'red', status: 'Red - Stopped' },
    { lane: 'C', name: 'Lane C (South)', color: 'yellow', status: 'Yellow - Waiting' },
    { lane: 'D', name: 'Lane D (West)', color: 'blue', status: 'Blue - Preparing' }
  ];

  return (
    <div className="card signal-card">
      <div className="card-header">
        <h2>Signal Status</h2>
        <span className="status-badge live">● LIVE</span>
      </div>
      <div className="signal-grid">
        {signals.map(signal => (
          <div key={signal.lane} className="signal-item" data-lane={signal.lane}>
            <div className="signal-header">
              <span className="signal-name">{signal.name}</span>
              <span className="signal-timer">{timers[signal.lane]}s</span>
            </div>
            <div className="signal-bar">
              <div 
                className={`signal-progress ${signal.color}`}
                style={{ width: `${getProgress(timers[signal.lane])}%` }}
              ></div>
            </div>
            <div className="signal-status">
              <span className={`status-light ${signal.color}`}></span>
              <span className="status-text">{signal.status}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SignalStatus;