import React, { useState } from 'react';
import './Profile.css';

const Profile = () => {
  const [user, setUser] = useState({
    name: 'John Smith',
    email: 'john.smith@trafficcontrol.gov',
    role: 'Traffic Operations Manager',
    department: 'City Traffic Department',
    phone: '+1 (555) 123-4567',
    location: 'Central Command Center'
  });

  const [isEditing, setIsEditing] = useState(false);
  const [editedUser, setEditedUser] = useState(user);

  const handleSave = () => {
    setUser(editedUser);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditedUser(user);
    setIsEditing(false);
  };

  return (
    <div className="profile-section">
      <div className="section-header">
        <h1>Profile</h1>
        <p>Manage your account settings</p>
      </div>

      <div className="profile-grid">
        <div className="card profile-card">
          <div className="profile-header">
            <div className="avatar">
              {user.name.split(' ').map(n => n[0]).join('')}
            </div>
            <div className="profile-info">
              <h2>{user.name}</h2>
              <p>{user.role}</p>
            </div>
            <button 
              className="edit-btn"
              onClick={() => setIsEditing(!isEditing)}
            >
              {isEditing ? 'Cancel' : 'Edit Profile'}
            </button>
          </div>

          <div className="profile-details">
            <div className="detail-row">
              <label>Full Name</label>
              {isEditing ? (
                <input
                  type="text"
                  value={editedUser.name}
                  onChange={(e) => setEditedUser({...editedUser, name: e.target.value})}
                  className="edit-input"
                />
              ) : (
                <span>{user.name}</span>
              )}
            </div>
            <div className="detail-row">
              <label>Email</label>
              {isEditing ? (
                <input
                  type="email"
                  value={editedUser.email}
                  onChange={(e) => setEditedUser({...editedUser, email: e.target.value})}
                  className="edit-input"
                />
              ) : (
                <span>{user.email}</span>
              )}
            </div>
            <div className="detail-row">
              <label>Role</label>
              <span>{user.role}</span>
            </div>
            <div className="detail-row">
              <label>Department</label>
              <span>{user.department}</span>
            </div>
            <div className="detail-row">
              <label>Phone</label>
              {isEditing ? (
                <input
                  type="tel"
                  value={editedUser.phone}
                  onChange={(e) => setEditedUser({...editedUser, phone: e.target.value})}
                  className="edit-input"
                />
              ) : (
                <span>{user.phone}</span>
              )}
            </div>
            <div className="detail-row">
              <label>Location</label>
              <span>{user.location}</span>
            </div>
          </div>

          {isEditing && (
            <div className="profile-actions">
              <button className="save-btn" onClick={handleSave}>Save Changes</button>
              <button className="cancel-btn" onClick={handleCancel}>Cancel</button>
            </div>
          )}
        </div>

        <div className="profile-stats">
          <div className="card stat-card">
            <h3>Activity Summary</h3>
            <div className="activity-stats">
              <div className="activity-item">
                <span className="activity-number">156</span>
                <span className="activity-label">Logins This Month</span>
              </div>
              <div className="activity-item">
                <span className="activity-number">42</span>
                <span className="activity-label">Alerts Handled</span>
              </div>
              <div className="activity-item">
                <span className="activity-number">98%</span>
                <span className="activity-label">Response Rate</span>
              </div>
            </div>
          </div>

          <div className="card stat-card">
            <h3>Recent Activity</h3>
            <div className="activity-list">
              <div className="activity-entry">
                <span className="activity-time">2 hours ago</span>
                <span className="activity-desc">Updated signal timing at Intersection A</span>
              </div>
              <div className="activity-entry">
                <span className="activity-time">5 hours ago</span>
                <span className="activity-desc">Handled emergency green wave activation</span>
              </div>
              <div className="activity-entry">
                <span className="activity-time">Yesterday</span>
                <span className="activity-desc">Generated weekly traffic report</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;