import React from 'react';
import { LucideIcon } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string;
  trend?: string;
  trendUp?: boolean;
  icon: LucideIcon;
  color?: string;
}

export default function StatCard({ title, value, trend, trendUp, icon: Icon, color = 'var(--primary)' }: StatCardProps) {
  return (
    <div className="glass-panel" style={{ padding: '24px', flex: 1 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px' }}>
        <p style={{ color: '#a1a1aa', fontSize: '0.9rem', fontWeight: 500, margin: 0 }}>{title}</p>
        <div style={{ 
          width: '36px', 
          height: '36px', 
          borderRadius: '10px', 
          background: `rgba(${color === 'var(--primary)' ? '59, 130, 246' : color}, 0.1)`, 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          color: color
        }}>
          <Icon size={20} />
        </div>
      </div>
      
      <div style={{ display: 'flex', alignItems: 'flex-end', gap: '8px' }}>
        <h3 style={{ fontSize: '1.8rem', fontWeight: 800, margin: 0, color: 'white' }}>{value}</h3>
        {trend && (
          <span style={{ 
            fontSize: '0.8rem', 
            fontWeight: 600, 
            color: trendUp ? '#10b981' : '#f43f5e',
            marginBottom: '6px'
          }}>
            {trendUp ? '+' : ''}{trend}
          </span>
        )}
      </div>
    </div>
  );
}
