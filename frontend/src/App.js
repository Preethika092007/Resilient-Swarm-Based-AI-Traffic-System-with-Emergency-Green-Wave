import React, { useState } from 'react';
import './App.css';
import Navigation from './components/Navigation';
import Landing from './components/Landing';
import Dashboard from './components/Dashboard';
import VehicleDetection from './components/VehicleDetection';
import TrafficDensity from './components/TrafficDensity';
import GreenWave from './components/GreenWave';
import Analytics from './components/Analytics';
import Emergency from './components/Emergency';
import Signals from './components/Signals';
import Settings from './components/Settings';
import Profile from './components/Profile';

function App() {
  const [activeSection, setActiveSection] = useState('landing');

  const handleGetStarted = () => {
    setActiveSection('dashboard');
  };

  const renderSection = () => {
    switch(activeSection) {
      case 'landing':
        return <Landing onGetStarted={handleGetStarted} />;
      case 'dashboard':
        return <Dashboard />;
      case 'vehicle-detection':
        return <VehicleDetection />;
      case 'traffic-density':
        return <TrafficDensity />;
      case 'green-wave':
        return <GreenWave />;
      case 'analytics':
        return <Analytics />;
      case 'emergency':
        return <Emergency />;
      case 'signals':
        return <Signals />;
      case 'settings':
        return <Settings />;
      case 'profile':
        return <Profile />;
      default:
        return <Landing onGetStarted={handleGetStarted} />;
    }
  };

  return (
    <div className="App">
      <Navigation activeSection={activeSection} setActiveSection={setActiveSection} />
      <div className="main-container">
        {renderSection()}
      </div>
    </div>
  );
}

export default App;
