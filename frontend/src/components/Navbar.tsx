"use client";

import React from 'react';
import { Search, Bell, User as UserIcon, Plus } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';

export default function Navbar() {
  const { user } = useAuth();

  return (
    <header style={{
      height: '72px',
      borderBottom: '1px solid var(--glass-border)',
      background: 'rgba(9, 9, 11, 0.5)',
      backdropFilter: 'blur(12px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 32px',
      position: 'sticky',
      top: 0,
      zIndex: 40,
      marginLeft: '260px' // Offset for sidebar
    }}>
      {/* Search Bar */}
      <div style={{ position: 'relative', width: '320px' }}>
        <Search size={18} style={{ 
          position: 'absolute', 
          left: '12px', 
          top: '50%', 
          transform: 'translateY(-50%)', 
          color: '#71717a' 
        }} />
        <input 
          type="text" 
          placeholder="Search meetings or notes..."
          className="input-premium"
          style={{ 
            paddingLeft: '40px', 
            height: '40px',
            background: 'rgba(255, 255, 255, 0.03)',
            borderRadius: '12px'
          }}
        />
      </div>

      {/* Right Actions */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
        <button className="btn-primary" style={{ height: '40px', padding: '0 16px' }}>
          <Plus size={18} />
          <span>New Meeting</span>
        </button>

        <div style={{ 
          width: '40px', 
          height: '40px', 
          borderRadius: '12px', 
          border: '1px solid var(--glass-border)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#a1a1aa',
          cursor: 'pointer'
        }}>
          <Bell size={20} />
        </div>

        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '12px', 
          padding: '4px 4px 4px 12px',
          borderRadius: '14px',
          border: '1px solid var(--glass-border)',
          background: 'rgba(255,255,255,0.02)'
        }}>
          <div style={{ textAlign: 'right', display: 'none', md: 'block' } as any}>
            <p style={{ fontSize: '0.85rem', fontWeight: 600, color: 'white', margin: 0 }}>
              {user?.displayName || 'User'}
            </p>
            <p style={{ fontSize: '0.7rem', color: '#71717a', margin: 0 }}>
              Free Plan
            </p>
          </div>
          <div style={{ 
            width: '32px', 
            height: '32px', 
            borderRadius: '10px', 
            background: 'var(--primary-gradient)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white'
          }}>
            <UserIcon size={18} />
          </div>
        </div>
      </div>
    </header>
  );
}
