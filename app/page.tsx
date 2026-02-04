'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function Page() {
  const [activeTab, setActiveTab] = useState('trial');

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Main Container */}
      <div className="max-w-4xl mx-auto my-10 bg-white rounded-2xl shadow-lg overflow-hidden">
        {/* Navigation Bar */}
        <div className="bg-slate-800 text-white px-8 py-6 flex items-center justify-between">
          <h1 className="text-2xl font-bold">Clinical Trial Intelligence</h1>
          <div className="flex gap-6">
            <button
              onClick={() => setActiveTab('trial')}
              className={`font-semibold transition ${activeTab === 'trial' ? 'text-white' : 'text-gray-300 hover:text-white'}`}
            >
              Trial
            </button>
            <button
              onClick={() => setActiveTab('changes')}
              className={`font-semibold transition ${activeTab === 'changes' ? 'text-white' : 'text-gray-300 hover:text-white'}`}
            >
              Changes
            </button>
            <button
              onClick={() => setActiveTab('evidence')}
              className={`font-semibold transition ${activeTab === 'evidence' ? 'text-white' : 'text-gray-300 hover:text-white'}`}
            >
              Evidence
            </button>
            <button
              onClick={() => setActiveTab('audit')}
              className={`font-semibold transition ${activeTab === 'audit' ? 'text-white' : 'text-gray-300 hover:text-white'}`}
            >
              Audit
            </button>
          </div>
        </div>

        {/* Content Area */}
        <div className="p-8">
          {activeTab === 'trial' && (
            <div>
              <h2 className="text-xl font-bold text-slate-800 mb-4">Trial Documents</h2>
              <div className="bg-gray-50 border border-gray-300 rounded-lg p-6">
                <input
                  type="file"
                  accept=".pdf"
                  className="w-full border border-gray-400 rounded-md px-3 py-2 mb-4"
                />
                <button className="bg-slate-800 text-white px-6 py-2 rounded-md font-semibold hover:bg-slate-700 transition">
                  Upload Protocol
                </button>
              </div>
            </div>
          )}

          {activeTab === 'changes' && (
            <div>
              <h2 className="text-xl font-bold text-slate-800 mb-4">Protocol Changes</h2>
              <p className="text-gray-600">Version comparison coming soon.</p>
            </div>
          )}

          {activeTab === 'evidence' && (
            <div>
              <h2 className="text-xl font-bold text-slate-800 mb-4">Evidence Review</h2>
              <p className="text-gray-600">Evidence review system coming soon.</p>
            </div>
          )}

          {activeTab === 'audit' && (
            <div>
              <h2 className="text-xl font-bold text-slate-800 mb-4">Audit Trail</h2>
              <p className="text-gray-600">Audit trail coming soon.</p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="bg-gray-100 text-center py-4 text-sm text-gray-600">
          Regulatory AI System · Internal Demo · 2026
        </div>
      </div>
    </div>
  );
}
