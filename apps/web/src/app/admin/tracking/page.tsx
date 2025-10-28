"use client";

import { useState } from "react";
import DashboardLayout from "@/components/DashboardLayout";
import TrackingMap from "@/components/TrackingMap";
import { fetchShipmentById } from "@/lib/supabase/client";

const adminMenuItems = [
  {
    name: "Dashboard",
    href: "/admin/dashboard",
    icon: (
      <svg
        className="w-5 h-5"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
        />
      </svg>
    ),
  },
  { name: 'Dispatch Orders', href: '/admin/dispatch', icon: <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg> },
  {
    name: "Chat",
    href: "/admin/chat",
    icon: (
      <svg
        className="w-5 h-5"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
        />
      </svg>
    ),
  },
  {
    name: "Tracking",
    href: "/admin/tracking",
    icon: (
      <svg
        className="w-5 h-5"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"
        />
      </svg>
    ),
  },
  {
    name: "Knowledge Base",
    href: "/admin/knowledge-base",
    icon: (
      <svg
        className="w-5 h-5"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
        />
      </svg>
    ),
  },
  {
    name: "Analysis",
    href: "/admin/analysis",
    icon: (
      <svg
        className="w-5 h-5"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
        />
      </svg>
    ),
  },
  {
    name: "Users",
    href: "/admin/users",
    icon: (
      <svg
        className="w-5 h-5"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
        />
      </svg>
    ),
  },
  {
    name: "Warehouses",
    href: "/admin/warehouses",
    icon: (
      <svg
        className="w-5 h-5"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
        />
      </svg>
    ),
  },
  {
    name: "Vehicles",
    href: "/admin/vehicles",
    icon: (
      <svg
        className="w-5 h-5"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M13 10V3L4 14h7v7l9-11h-7z"
        />
      </svg>
    ),
  },
];

// Note: keeping the sample listing for the admin table but the per-id tracking will query Supabase.

const shipmentsData: Record<string, any> = {
  "SHP-001": {
    id: "SHP-001",
    order: "ORD-1234",
    customer: "John Doe",
    status: "in-transit",
    location: "Delhi Hub",
    eta: "2 hours",
    progress: 75,
    origin: { lat: 28.6139, lng: 77.209, label: "Delhi Warehouse" },
    destination: {
      lat: 19.076,
      lng: 72.8777,
      label: "Mumbai - Customer Address",
    },
    currentLocation: { lat: 23.0225, lng: 72.5714, label: "Ahmedabad Hub" },
  },
  "SHP-002": {
    id: "SHP-002",
    order: "ORD-1235",
    customer: "Jane Smith",
    status: "delivered",
    location: "Mumbai",
    eta: "Delivered",
    progress: 100,
    origin: { lat: 28.6139, lng: 77.209, label: "Delhi Warehouse" },
    destination: {
      lat: 19.076,
      lng: 72.8777,
      label: "Mumbai - Customer Address",
    },
    currentLocation: { lat: 19.076, lng: 72.8777, label: "Delivered" },
  },
  "SHP-003": {
    id: "SHP-003",
    order: "ORD-1236",
    customer: "Bob Johnson",
    status: "pending",
    location: "Warehouse A",
    eta: "5 hours",
    progress: 25,
    origin: { lat: 12.9716, lng: 77.5946, label: "Bangalore Warehouse" },
    destination: {
      lat: 13.0827,
      lng: 80.2707,
      label: "Chennai - Customer Address",
    },
    currentLocation: {
      lat: 12.9716,
      lng: 77.5946,
      label: "Bangalore Warehouse",
    },
  },
};

export default function AdminTracking() {
  const [shipmentId, setShipmentId] = useState("");
  const [selectedShipment, setSelectedShipment] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleTrack = () => {
    // fetch live shipment by id
    (async () => {
      if (!shipmentId) return;
      setLoading(true);
      try {
        const data = await fetchShipmentById(shipmentId);
        if (!data) {
          alert("Shipment not found");
          setSelectedShipment(null);
        } else {
          setSelectedShipment({
            id: data.id,
            order: data.order,
            customer: data.customer,
            status: data.status,
            eta: data.eta,
            progress: data.progress || 0,
            origin: data.origin,
            destination: data.destination,
            currentLocation: data.currentLocation,
          });
        }
      } catch (e) {
        console.error(e);
        alert("Error fetching shipment");
        setSelectedShipment(null);
      } finally {
        setLoading(false);
      }
    })();
  };
  return (
    <DashboardLayout role="admin" menuItems={adminMenuItems}>
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">
          Shipment Tracking
        </h1>

        {/* Shipment ID Search */}
        <div className="mb-6">
          <div className="flex gap-3">
            <div className="relative flex-1">
              <input
                type="text"
                value={shipmentId}
                onChange={(e) => setShipmentId(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleTrack()}
                placeholder="Enter Shipment ID (e.g., SHP-001)"
                className="w-full px-4 py-3 pl-12 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent dark:bg-gray-800 dark:text-white"
              />
              <svg
                className="absolute left-4 top-3.5 w-5 h-5 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
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
          <div className="mb-8 space-y-6">
            {/* Shipment Info */}
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                Shipment Details
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Shipment ID
                  </p>
                  <p className="font-semibold text-gray-900 dark:text-white">
                    {selectedShipment.id}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Customer
                  </p>
                  <p className="font-semibold text-gray-900 dark:text-white">
                    {selectedShipment.customer}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Status
                  </p>
                  <span
                    className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      selectedShipment.status === "delivered"
                        ? "bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400"
                        : selectedShipment.status === "in-transit"
                        ? "bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400"
                        : "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400"
                    }`}
                  >
                    {selectedShipment.status}
                  </span>
                </div>
                <div>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    ETA
                  </p>
                  <p className="font-semibold text-gray-900 dark:text-white">
                    {selectedShipment.eta}
                  </p>
                </div>
              </div>
              <div className="mt-4">
                <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">
                  Progress
                </p>
                <div className="flex items-center gap-3">
                  <div className="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                    <div
                      className="bg-indigo-600 h-3 rounded-full transition-all"
                      style={{ width: `${selectedShipment.progress}%` }}
                    ></div>
                  </div>
                  <span className="text-sm font-medium text-gray-900 dark:text-white">
                    {selectedShipment.progress}%
                  </span>
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

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-md">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Total Shipments
            </p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
              156
            </p>
          </div>
          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-md">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              In Transit
            </p>
            <p className="text-2xl font-bold text-blue-600 dark:text-blue-400 mt-1">
              87
            </p>
          </div>
          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-md">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Delivered Today
            </p>
            <p className="text-2xl font-bold text-green-600 dark:text-green-400 mt-1">
              42
            </p>
          </div>
          <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-md">
            <p className="text-sm text-gray-600 dark:text-gray-400">Pending</p>
            <p className="text-2xl font-bold text-yellow-600 dark:text-yellow-400 mt-1">
              27
            </p>
          </div>
        </div>

        {/* Shipments List */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              Active Shipments
            </h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Shipment ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Order ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Customer
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Location
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    ETA
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Progress
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                {Object.values(shipmentsData).map((shipment: any) => (
                  <tr
                    key={shipment.id}
                    className="hover:bg-gray-50 dark:hover:bg-gray-700"
                  >
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="font-medium text-gray-900 dark:text-white">
                        {shipment.id}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-600 dark:text-gray-400">
                      {shipment.order}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-600 dark:text-gray-400">
                      {shipment.customer}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          shipment.status === "delivered"
                            ? "bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400"
                            : shipment.status === "in-transit"
                            ? "bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400"
                            : "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400"
                        }`}
                      >
                        {shipment.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-600 dark:text-gray-400">
                      {shipment.location}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-600 dark:text-gray-400">
                      {shipment.eta}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <div className="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                          <div
                            className="bg-indigo-600 h-2 rounded-full"
                            style={{ width: `${shipment.progress}%` }}
                          ></div>
                        </div>
                        <span className="text-sm text-gray-600 dark:text-gray-400">
                          {shipment.progress}%
                        </span>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
