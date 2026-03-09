"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Mail, Lock, User, UserPlus, Chrome, ArrowLeft, Loader2 } from 'lucide-react';
import { signInWithPopup, createUserWithEmailAndPassword, googleProvider, auth } from '@/lib/firebase';

export default function RegisterPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      // In a real app, you would also update the user's profile with their name
      await createUserWithEmailAndPassword(auth, email, password);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Failed to create account');
      setLoading(false);
    }
  };

  const handleGoogleLogin = async () => {
    setLoading(true);
    setError('');
    try {
      await signInWithPopup(auth, googleProvider);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Failed to sign up with Google');
      setLoading(false);
    }
  };

  return (
    <div>
      <div style={{ textAlign: 'center', marginBottom: '32px' }}>
        <h1 className="gradient-text" style={{ fontSize: '2rem', fontWeight: 800, marginBottom: '8px' }}>
          Create Account
        </h1>
        <p style={{ color: '#a1a1aa', fontSize: '0.95rem' }}>
          Start turning meetings into intelligence today
        </p>
      </div>

      <form onSubmit={handleRegister}>
        <div className="input-group">
          <label className="input-label">Full Name</label>
          <div style={{ position: 'relative' }}>
            <User size={18} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: '#71717a' }} />
            <input
              type="text"
              placeholder="John Doe"
              className="input-premium"
              style={{ paddingLeft: '40px' }}
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
        </div>

        <div className="input-group">
          <label className="input-label">Email Address</label>
          <div style={{ position: 'relative' }}>
            <Mail size={18} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: '#71717a' }} />
            <input
              type="email"
              placeholder="name@company.com"
              className="input-premium"
              style={{ paddingLeft: '40px' }}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
        </div>

        <div className="input-group">
          <label className="input-label">Password</label>
          <div style={{ position: 'relative' }}>
            <Lock size={18} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: '#71717a' }} />
            <input
              type="password"
              placeholder="••••••••"
              className="input-premium"
              style={{ paddingLeft: '40px' }}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <p style={{ color: '#71717a', fontSize: '0.75rem', marginTop: '4px' }}>
            Must be at least 6 characters long
          </p>
        </div>

        {error && <p className="error-text">{error}</p>}

        <button 
          type="submit" 
          className="btn-primary" 
          style={{ width: '100%', marginTop: '8px' }}
          disabled={loading}
        >
          {loading ? <Loader2 className="animate-spin" size={20} /> : <UserPlus size={20} />}
          <span>Create Account</span>
        </button>
      </form>

      <div style={{ position: 'relative', margin: '24px 0', textAlign: 'center' }}>
        <div style={{ position: 'absolute', top: '50%', left: 0, right: 0, height: '1px', background: 'var(--border)', zIndex: 0 }} />
        <span style={{ position: 'relative', background: '#111', padding: '0 12px', color: '#71717a', fontSize: '0.8rem', zIndex: 1, borderRadius: '4px' }}>
          OR REGISTER WITH
        </span>
      </div>

      <button 
        onClick={handleGoogleLogin} 
        className="btn-outline" 
        style={{ width: '100%' }}
        disabled={loading}
      >
        <Chrome size={20} />
        <span>Google Account</span>
      </button>

      <p style={{ marginTop: '24px', textAlign: 'center', color: '#a1a1aa', fontSize: '0.9rem' }}>
        Already have an account?{' '}
        <Link href="/login" style={{ color: 'var(--primary)', fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
          <ArrowLeft size={14} /> Back to login
        </Link>
      </p>
    </div>
  );
}
