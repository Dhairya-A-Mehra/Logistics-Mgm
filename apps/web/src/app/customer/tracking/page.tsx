'use client';

import { useState } from 'react';
import DashboardLayout from '@/components/DashboardLayout';
import TrackingMap from '@/components/TrackingMap';

const customerMenuItems = [
  { name: 'Dashboard', href: '/customer/dashboard', icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg> },
  { name: 'Chat', href: '/customer/chat', icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg> },
  { name: 'Tracking', href: '/customer/tracking', icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" /></svg> },
  { name: 'Place Order', href: '/customer/place-order', icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" /></svg> },
  { name: 'My Orders', href: '/customer/orders', icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" /></svg> },
];

const shipmentsData: Record<string, any> = {
  'SHP-001': {
    id: 'SHP-001',
    order: 'ORD-1234',
    customer: 'John Doe',
    status: 'in-transit',
    location: 'Delhi Hub',
    eta: '2 hours',
    progress: 75,
    origin: { lat: 28.6139, lng: 77.2090, label: 'Delhi Warehouse' },
    destination: { lat: 19.0760, lng: 72.8777, label: 'Mumbai - Customer Address' },
    currentLocation: { lat: 23.0225, lng: 72.5714, label: 'Ahmedabad Hub' },
  },
  'SHP-002': {
    id: 'SHP-002',
    order: 'ORD-1235',
    customer: 'Jane Smith',
    status: 'delivered',
    location: 'Mumbai',
    eta: 'Delivered',
    progress: 100,
    origin: { lat: 28.6139, lng: 77.2090, label: 'Delhi Warehouse' },
    destination: { lat: 19.0760, lng: 72.8777, label: 'Mumbai - Customer Address' },
    currentLocation: { lat: 19.0760, lng: 72.8777, label: 'Delivered' },
  },
  'SHP-003': {
    id: 'SHP-003',
    order: 'ORD-1236',
    customer: 'Bob Johnson',
    status: 'pending',
    location: 'Warehouse A',
    eta: '5 hours',
    progress: 25,
    origin: { lat: 12.9716, lng: 77.5946, label: 'Bangalore Warehouse' },
    destination: { lat: 13.0827, lng: 80.2707, label: 'Chennai - Customer Address' },
    currentLocation: { lat: 12.9716, lng: 77.5946, label: 'Bangalore Warehouse' },
  },
};

export default function CustomerTracking() {
  const [shipmentId, setShipmentId] = useState('');
  const [selectedShipment, setSelectedShipment] = useState<any>(null);

  const handleTrack = () => {
    const shipment = shipmentsData[shipmentId.toUpperCase()];
    if (shipment) {
      setSelectedShipment(shipment);
    } else {
      alert('Shipment not found!');
      setSelectedShipment(null);
    }
  };

  return (
    <DashboardLayout role="customer" menuItems={customerMenuItems}>
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">Track Your Shipment</h1>

        {/* Shipment ID Search */}
        <div className="mb-6">
          <div className="flex gap-3">
            <div className="relative flex-1">
              <input
                type="text"
                value={shipmentId}
                onChange={(e) => setShipmentId(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleTrack()}
                placeholder="Enter Shipment ID (e.g., SHP-001)"
                className="w-full px-4 py-3 pl-12 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent dark:bg-gray-800 dark:text-white"
              />
              <svg className="absolute left-4 top-3.5 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <button
              onClick={handleTrack}
              className="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition-colors"
            >
              Track Shipment
            </button>
          </div>
        </div>

        {/* Shipment Details & Map */}
        {selectedShipment && (
          <div className="space-y-6">
            {/* Shipment Info */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Shipment Details</h2>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Shipment ID</p>
                  <p className="font-semibold text-gray-900 dark:text-white">{selectedShipment.id}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Order ID</p>
                  <p className="font-semibold text-gray-900 dark:text-white">{selectedShipment.order}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Status</p>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    selectedShipment.status === 'delivered' ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400' :
                    selectedShipment.status === 'in-transit' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400' :
                    'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400'
                  }`}>
                    {selectedShipment.status}
                  </span>
                </div>
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">ETA</p>
                  <p className="font-semibold text-gray-900 dark:text-white">{selectedShipment.eta}</p>
                </div>
              </div>
              <div className="mt-4">
                <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">Delivery Progress</p>
                <div className="flex items-center gap-3">
                  <div className="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                    <div className="bg-indigo-600 h-3 rounded-full transition-all" style={{ width: `${selectedShipment.progress}%` }}></div>
                  </div>
                  <span className="text-sm font-medium text-gray-900 dark:text-white">{selectedShipment.progress}%</span>
                </div>
              </div>
            </div>

            {/* Map */}
            <TrackingMap
              origin={selectedShipment.origin}
              destination={selectedShipment.destination}
              currentLocation={selectedShipment.currentLocation}
            />
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
