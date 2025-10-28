'use client';

import DashboardLayout from '@/components/DashboardLayout';
import { useState } from 'react';

const adminMenuItems = [
  { name: 'Dashboard', href: '/admin/dashboard', icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg> },
  { name: 'Dispatch Orders', href: '/admin/dispatch', icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg> },
  { name: 'Chat', href: '/admin/chat', icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg> },
  { name: 'Tracking', href: '/admin/tracking', icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" /></svg> },
  { name: 'Knowledge Base', href: '/admin/knowledge-base', icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" /></svg> },
  { name: 'Analysis', href: '/admin/analysis', icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg> },
  { name: 'Users', href: '/admin/users', icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" /></svg> },
  { name: 'Warehouses', href: '/admin/warehouses', icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" /></svg> },
  { name: 'Vehicles', href: '/admin/vehicles', icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg> },
];

const tables = [
  { name: 'customers', description: 'User accounts with roles (customer, delivery_guy, admin)', columns: 10 },
  { name: 'orders', description: 'Customer orders with items and delivery details', columns: 9 },
  { name: 'shipments', description: 'Delivery shipments linked to orders and vehicles', columns: 9 },
  { name: 'warehouses', description: 'Warehouse locations and regions', columns: 5 },
  { name: 'vehicles', description: 'Fleet vehicles with capacity and status', columns: 6 },
  { name: 'inventory', description: 'Warehouse inventory and stock levels', columns: 6 },
  { name: 'vehicle_telemetry', description: 'Real-time vehicle tracking data', columns: 7 },
  { name: 'fuel_prices', description: 'Current and historical fuel prices', columns: 3 },
  { name: 'packaging_types', description: 'Packaging options with dimensions', columns: 7 },
  { name: 'documents', description: 'Vector embeddings for AI search', columns: 9 },
  { name: 'agent_audit_logs', description: 'AI agent decision tracking', columns: 6 },
];

export default function KnowledgeBase() {
  const [selectedTable, setSelectedTable] = useState<string | null>(null);

  return (
    <DashboardLayout role="admin" menuItems={adminMenuItems}>
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">Knowledge Base</h1>
        
        <p className="text-gray-600 dark:text-gray-400 mb-8">
          Database schema documentation for LogiMAS system
        </p>

        {/* Database Tables */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tables.map((table) => (
            <div
              key={table.name}
              onClick={() => setSelectedTable(table.name)}
              className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-md hover:shadow-lg transition-shadow cursor-pointer border-2 border-transparent hover:border-indigo-500"
            >
              <div className="flex items-start justify-between mb-3">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{table.name}</h3>
                <span className="text-xs bg-indigo-100 dark:bg-indigo-900/20 text-indigo-600 dark:text-indigo-400 px-2 py-1 rounded">
                  {table.columns} cols
                </span>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400">{table.description}</p>
              <div className="mt-4 flex items-center text-indigo-600 dark:text-indigo-400 text-sm font-medium">
                View details
                <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          ))}
        </div>

        {/* Schema Info */}
        <div className="mt-8 bg-white dark:bg-gray-800 rounded-xl shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Database Schema</h2>
          <div className="space-y-3 text-sm">
            <div className="flex items-center gap-2">
              <span className="font-medium text-gray-700 dark:text-gray-300">Total Tables:</span>
              <span className="text-gray-600 dark:text-gray-400">11</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="font-medium text-gray-700 dark:text-gray-300">Database:</span>
              <span className="text-gray-600 dark:text-gray-400">PostgreSQL (Supabase)</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="font-medium text-gray-700 dark:text-gray-300">Extensions:</span>
              <span className="text-gray-600 dark:text-gray-400">pgvector (for AI embeddings)</span>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
