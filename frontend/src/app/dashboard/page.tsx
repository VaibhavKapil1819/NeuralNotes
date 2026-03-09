"use client";

import React from 'react';
import { Mic, CheckCircle2, Clock, Zap, ArrowUpRight, Plus, MoreHorizontal } from 'lucide-react';
import StatCard from '@/components/StatCard';

export default function DashboardPage() {
  return (
    <div>
      {/* Header */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        marginBottom: '40px' 
      }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: 800, margin: '0 0 8px 0', color: 'white' }}>
            Executive Dashboard
          </h1>
          <p style={{ color: '#a1a1aa', margin: 0 }}>
            Quick overview of your meeting intelligence and activity.
          </p>
        </div>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button className="btn-outline" style={{ height: '44px' }}>
            <span>Export Report</span>
          </button>
          <button className="btn-primary" style={{ height: '44px' }}>
            <Plus size={20} />
            <span>Record Live</span>
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(4, 1fr)', 
        gap: '24px', 
        marginBottom: '48px' 
      }}>
        <StatCard 
          title="Total Meetings" 
          value="48" 
          trend="12%" 
          trendUp={true} 
          icon={Mic} 
        />
        <StatCard 
          title="Insights Generated" 
          value="1,240" 
          trend="8%" 
          trendUp={true} 
          icon={Zap} 
          color="#8b5cf6" 
        />
        <StatCard 
          title="Tasks Completed" 
          value="84" 
          trend="5%" 
          trendUp={true} 
          icon={CheckCircle2} 
          color="#10b981" 
        />
        <StatCard 
          title="Time Saved" 
          value="12.5h" 
          trend="2.4h" 
          trendUp={true} 
          icon={Clock} 
          color="#f59e0b" 
        />
      </div>

      {/* Recent Activity / Content */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
        <div className="glass-panel" style={{ padding: '32px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
             <h3 style={{ margin: 0, fontSize: '1.25rem', fontWeight: 700, color: 'white' }}>Recent Sessions</h3>
             <button style={{ 
               background: 'transparent', 
               border: 'none', 
               color: 'var(--primary)', 
               fontSize: '0.9rem', 
               fontWeight: 600, 
               display: 'flex', 
               alignItems: 'center', 
               gap: '4px',
               cursor: 'pointer'
             }}>
               View All <ArrowUpRight size={16} />
             </button>
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {[1, 2, 3].map((i) => (
              <div key={i} style={{ 
                padding: '16px', 
                borderRadius: '12px', 
                background: 'rgba(255,255,255,0.02)',
                border: '1px solid var(--glass-border)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                  <div style={{ 
                    width: '40px', 
                    height: '40px', 
                    borderRadius: '8px', 
                    background: 'rgba(59, 130, 246, 0.1)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'var(--primary)'
                  }}>
                    <FileText size={20} />
                  </div>
                  <div>
                    <h4 style={{ margin: '0 0 4px 0', fontSize: '1rem', color: 'white' }}>Project Synchronization #{i+102}</h4>
                    <p style={{ margin: 0, fontSize: '0.8rem', color: '#71717a' }}>Yesterday at 4:32 PM • 45m 12s</p>
                  </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <div style={{ 
                    padding: '4px 10px', 
                    borderRadius: '20px', 
                    background: 'rgba(16, 185, 129, 0.1)', 
                    color: '#10b981', 
                    fontSize: '0.75rem', 
                    fontWeight: 600 
                  }}>
                    Analyzed
                  </div>
                  <button style={{ background: 'transparent', border: 'none', color: '#71717a', cursor: 'pointer' }}>
                    <MoreHorizontal size={18} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '32px' }}>
          <h3 style={{ margin: '0 0 24px 0', fontSize: '1.25rem', fontWeight: 700, color: 'white' }}>Action Items</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            {[
              "Update security protocols",
              "Review Q3 budget allocated",
              "Finalize client presentation"
            ].map((task, i) => (
              <div key={i} style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                <div style={{ 
                  marginTop: '4px',
                  width: '18px', 
                  height: '18px', 
                  borderRadius: '4px', 
                  border: '2px solid var(--primary)',
                  cursor: 'pointer'
                }} />
                <div>
                  <p style={{ margin: '0 0 4px 0', fontSize: '0.95rem', color: 'white', fontWeight: 500 }}>{task}</p>
                  <p style={{ margin: 0, fontSize: '0.75rem', color: '#71717a' }}>Due in 2 days</p>
                </div>
              </div>
            ))}
          </div>
          
          <button className="btn-outline" style={{ width: '100%', marginTop: '32px' }}>
            View Full List
          </button>
        </div>
      </div>
    </div>
  );
}

// Internal icon for the list mapping
const FileText = ({ size, ...props }: any) => {
  const { FileText: Icon } = require('lucide-react');
  return <Icon size={size} {...props} />;
};
