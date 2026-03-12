import React, { useState } from 'react';
import './Navigation.css';

const Navigation = ({ activeSection, setActiveSection }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const menuItems = [
    { id: 'landing', label: 'Home' },
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'vehicle-detection', label: 'Vehicle Detection' },
    { id: 'traffic-density', label: 'Traffic Density' },
    { id: 'green-wave', label: 'Green Wave Route' },
    { id: 'analytics', label: 'Analytics' },
    { id: 'emergency', label: 'Emergency' },
    { id: 'signals', label: 'Signals' },
    { id: 'settings', label: 'Settings' },
    { id: 'profile', label: 'Profile' }
  ];

  const handleNavClick = (sectionId) => {
    setActiveSection(sectionId);
    setMobileMenuOpen(false);
  };

  return (
    <nav className="top-nav">
      <div className="nav-container">
        <div className="nav-brand">
          <span className="brand-text">Smart Traffic Control</span>
        </div>
        
        <ul className={`nav-menu ${mobileMenuOpen ? 'active' : ''}`}>
          {menuItems.map(item => (
            <li
              key={item.id}
              className={`nav-item ${activeSection === item.id ? 'active' : ''}`}
              onClick={() => handleNavClick(item.id)}
            >
              <span>{item.label}</span>
            </li>
          ))}
        </ul>
        
        <button 
          className="mobile-toggle" 
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </nav>
  );
};

export default Navigation;
