import React, { useEffect, useRef, useState } from 'react';
import './IntersectionCanvas.css';

const IntersectionCanvas = () => {
  const canvasRef = useRef(null);
  const [isRunning, setIsRunning] = useState(true);
  const [signalState, setSignalState] = useState('green');
  const vehiclesRef = useRef([
    { x: 250, y: 80, lane: 'A', type: 'car', color: '#3498db', speed: 1.5, direction: 'down', stopped: false },
    { x: 250, y: 140, lane: 'A', type: 'bike', color: '#e74c3c', speed: 1.5, direction: 'down', stopped: false },
    { x: 420, y: 250, lane: 'B', type: 'car', color: '#9b59b6', speed: 1.5, direction: 'left', stopped: false },
    { x: 360, y: 250, lane: 'B', type: 'bike', color: '#1abc9c', speed: 1.5, direction: 'left', stopped: false },
    { x: 250, y: 420, lane: 'C', type: 'car', color: '#f39c12', speed: 1.5, direction: 'up', stopped: false },
    { x: 250, y: 360, lane: 'C', type: 'bike', color: '#e67e22', speed: 1.5, direction: 'up', stopped: false },
    { x: 80, y: 250, lane: 'D', type: 'car', color: '#2ecc71', speed: 1.5, direction: 'right', stopped: false },
    { x: 140, y: 250, lane: 'D', type: 'bike', color: '#16a085', speed: 1.5, direction: 'right', stopped: false }
  ]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    let animationId;
    let signalTimer = 0;

    const drawSignal = (x, y, state) => {
      // Signal box
      ctx.fillStyle = '#1a1a1a';
      ctx.fillRect(x - 25, y - 50, 50, 100);
      ctx.strokeStyle = '#333';
      ctx.lineWidth = 2;
      ctx.strokeRect(x - 25, y - 50, 50, 100);

      // Red light
      ctx.beginPath();
      ctx.arc(x, y - 30, 18, 0, Math.PI * 2);
      ctx.fillStyle = state === 'red' ? '#e74c3c' : '#333';
      ctx.fill();
      if (state === 'red') {
        ctx.shadowColor = '#e74c3c';
        ctx.shadowBlur = 15;
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      // Yellow light
      ctx.beginPath();
      ctx.arc(x, y, 18, 0, Math.PI * 2);
      ctx.fillStyle = state === 'yellow' ? '#f39c12' : '#333';
      ctx.fill();
      if (state === 'yellow') {
        ctx.shadowColor = '#f39c12';
        ctx.shadowBlur = 15;
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      // Green light
      ctx.beginPath();
      ctx.arc(x, y + 30, 18, 0, Math.PI * 2);
      ctx.fillStyle = state === 'green' ? '#27ae60' : '#333';
      ctx.fill();
      if (state === 'green') {
        ctx.shadowColor = '#27ae60';
        ctx.shadowBlur = 15;
        ctx.fill();
        ctx.shadowBlur = 0;
      }
    };

    const drawVehicle = (vehicle) => {
      ctx.save();
      ctx.translate(vehicle.x, vehicle.y);
      
      if (vehicle.direction === 'left' || vehicle.direction === 'right') {
        ctx.rotate(Math.PI / 2);
      }
      
      if (vehicle.type === 'car') {
        // Car body
        ctx.fillStyle = vehicle.color;
        ctx.fillRect(-20, -12, 40, 24);
        // Car roof
        ctx.fillStyle = vehicle.color;
        ctx.filter = 'brightness(1.2)';
        ctx.fillRect(-8, -8, 16, 16);
        ctx.filter = 'none';
        // Headlights
        ctx.fillStyle = '#f1c40f';
        ctx.fillRect(16, -10, 4, 6);
        ctx.fillRect(16, 4, 4, 6);
      } else {
        // Bike body
        ctx.fillStyle = vehicle.color;
        ctx.fillRect(-15, -8, 30, 16);
        // Rider
        ctx.fillStyle = vehicle.color;
        ctx.filter = 'brightness(1.3)';
        ctx.beginPath();
        ctx.arc(0, 0, 8, 0, Math.PI * 2);
        ctx.fill();
        ctx.filter = 'none';
      }
      
      ctx.restore();
    };

    const animate = () => {
      if (!isRunning) {
        animationId = requestAnimationFrame(animate);
        return;
      }

      signalTimer++;
      if (signalTimer > 200) {
        signalTimer = 0;
        setSignalState(prev => {
          if (prev === 'green') return 'yellow';
          if (prev === 'yellow') return 'red';
          return 'green';
        });
      }

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Draw roads with better styling
      ctx.fillStyle = '#3d3d3d';
      ctx.fillRect(200, 0, 100, 500);
      ctx.fillRect(0, 200, 500, 100);

      // Road markings
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.setLineDash([20, 20]);
      ctx.beginPath();
      ctx.moveTo(250, 0);
      ctx.lineTo(250, 200);
      ctx.moveTo(250, 300);
      ctx.lineTo(250, 500);
      ctx.moveTo(0, 250);
      ctx.lineTo(200, 250);
      ctx.moveTo(300, 250);
      ctx.lineTo(500, 250);
      ctx.stroke();
      ctx.setLineDash([]);

      // Stop lines
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(200, 200);
      ctx.lineTo(300, 200);
      ctx.moveTo(200, 300);
      ctx.lineTo(300, 300);
      ctx.moveTo(200, 200);
      ctx.lineTo(200, 300);
      ctx.moveTo(300, 200);
      ctx.lineTo(300, 300);
      ctx.stroke();

      // Draw traffic signal in center
      drawSignal(250, 250, signalState);

      // Update and draw vehicles
      vehiclesRef.current.forEach(vehicle => {
        const stopLine = 200;
        const startLine = 300;
        let shouldStop = false;

        if (vehicle.direction === 'down' && vehicle.y < stopLine && signalState !== 'green') {
          shouldStop = true;
        }
        if (vehicle.direction === 'up' && vehicle.y > startLine && signalState !== 'green') {
          shouldStop = true;
        }
        if (vehicle.direction === 'left' && vehicle.x > startLine && signalState !== 'green') {
          shouldStop = true;
        }
        if (vehicle.direction === 'right' && vehicle.x < stopLine && signalState !== 'green') {
          shouldStop = true;
        }

        if (!shouldStop) {
          switch(vehicle.direction) {
            case 'down':
              vehicle.y += vehicle.speed;
              if (vehicle.y > 500) vehicle.y = -30;
              break;
            case 'up':
              vehicle.y -= vehicle.speed;
              if (vehicle.y < 0) vehicle.y = 530;
              break;
            case 'left':
              vehicle.x -= vehicle.speed;
              if (vehicle.x < 0) vehicle.x = 530;
              break;
            case 'right':
              vehicle.x += vehicle.speed;
              if (vehicle.x > 500) vehicle.x = -30;
              break;
            default:
              break;
          }
        }

        drawVehicle(vehicle);
      });

      // Draw lane labels
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 14px Arial';
      ctx.textAlign = 'center';
      ctx.fillText('Lane A', 250, 30);
      ctx.fillText('Lane B', 470, 255);
      ctx.fillText('Lane C', 250, 490);
      ctx.fillText('Lane D', 30, 255);

      animationId = requestAnimationFrame(animate);
    };

    animate();

    return () => cancelAnimationFrame(animationId);
  }, [isRunning, signalState]);

  const handleToggle = () => {
    setIsRunning(!isRunning);
  };

  const handleReset = () => {
    vehiclesRef.current = [
      { x: 250, y: 80, lane: 'A', type: 'car', color: '#3498db', speed: 1.5, direction: 'down', stopped: false },
      { x: 250, y: 140, lane: 'A', type: 'bike', color: '#e74c3c', speed: 1.5, direction: 'down', stopped: false },
      { x: 420, y: 250, lane: 'B', type: 'car', color: '#9b59b6', speed: 1.5, direction: 'left', stopped: false },
      { x: 360, y: 250, lane: 'B', type: 'bike', color: '#1abc9c', speed: 1.5, direction: 'left', stopped: false },
      { x: 250, y: 420, lane: 'C', type: 'car', color: '#f39c12', speed: 1.5, direction: 'up', stopped: false },
      { x: 250, y: 360, lane: 'C', type: 'bike', color: '#e67e22', speed: 1.5, direction: 'up', stopped: false },
      { x: 80, y: 250, lane: 'D', type: 'car', color: '#2ecc71', speed: 1.5, direction: 'right', stopped: false },
      { x: 140, y: 250, lane: 'D', type: 'bike', color: '#16a085', speed: 1.5, direction: 'right', stopped: false }
    ];
    setSignalState('green');
  };

  return (
    <div className="card intersection-card">
      <div className="card-header">
        <h2>Live Intersection View</h2>
        <div className="card-actions">
          <button className="btn-icon" onClick={handleReset}>↻</button>
        </div>
      </div>
      <div className="intersection-wrapper">
        <canvas ref={canvasRef} width="500" height="500"></canvas>
        <div className="intersection-controls">
          <button className="control-btn" onClick={handleToggle}>
            {isRunning ? 'Pause' : 'Play'}
          </button>
          <button className="control-btn" onClick={handleReset}>Reset</button>
        </div>
      </div>
    </div>
  );
};

export default IntersectionCanvas;
