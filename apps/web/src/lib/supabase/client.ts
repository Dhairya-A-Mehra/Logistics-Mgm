import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Helper functions for common operations
export const fetchDashboardStats = async () => {
  const [
    { count: totalShipments },
    { count: pendingShipments },
    { count: inTransitShipments },
    { count: completedShipments },
  ] = await Promise.all([
    supabase.from('shipments').select('*', { count: 'exact', head: true }),
    supabase.from('shipments').select('*', { count: 'exact', head: true }).eq('status', 'pending'),
    supabase.from('shipments').select('*', { count: 'exact', head: true }).eq('status', 'in_transit'),
    supabase.from('shipments').select('*', { count: 'exact', head: true }).eq('status', 'delivered'),
  ]);

  return {
    totalShipments,
    pendingShipments,
    inTransitShipments,
    completedShipments,
  };
};

export const fetchRecentShipments = async (limit = 5) => {
  const { data, error } = await supabase
    .from('shipments')
    .select('*, customers(*)')
    .order('created_at', { ascending: false })
    .limit(limit);

  if (error) throw error;
  return data;
};

export const fetchVehicleLocations = async () => {
  const { data, error } = await supabase
    .from('vehicles')
    .select('vehicle_id, current_location, status, vehicle_number');

  if (error) throw error;
  return data;
};

// Fetch a single shipment and compose origin/destination/currentLocation for the map
export const fetchShipmentById = async (shipmentId: string) => {
  // fetch shipment
  const { data: shipment, error: shipErr } = await supabase
    .from('shipments')
    .select('*')
    .eq('shipment_id', shipmentId)
    .single();

  if (shipErr) {
    throw shipErr;
  }
  if (!shipment) return null;

  // fetch origin warehouse
  const { data: warehouse, error: whErr } = await supabase
    .from('warehouses')
    .select('warehouse_id, name, lat, lon')
    .eq('warehouse_id', shipment.origin_warehouse_id)
    .single();

  if (whErr) {
    // non-fatal: continue with null warehouse
    console.warn('warehouse fetch error', whErr);
  }

  // fetch order (for destination & customer)
  const { data: order, error: orderErr } = await supabase
    .from('orders')
    .select('order_id, customer_id, destination')
    .eq('order_id', shipment.order_id)
    .single();

  if (orderErr) {
    console.warn('order fetch error', orderErr);
  }

  // fetch customer name if available
  let customer = null;
  if (order?.customer_id) {
    const { data: cust, error: custErr } = await supabase
      .from('customers')
      .select('customer_id, name')
      .eq('customer_id', order.customer_id)
      .single();
    if (custErr) console.warn('customer fetch error', custErr);
    customer = cust || null;
  }

  // fetch latest telemetry for vehicle (current location)
  let telemetry = null;
  if (shipment.vehicle_id) {
    const { data: tdata, error: tErr } = await supabase
      .from('vehicle_telemetry')
      .select('lat, lon, ts')
      .eq('vehicle_id', shipment.vehicle_id)
      .order('ts', { ascending: false })
      .limit(1);
    if (tErr) console.warn('telemetry fetch error', tErr);
    telemetry = Array.isArray(tdata) && tdata.length ? tdata[0] : null;
  }

  // compute progress percent when dates are available
  let progress = 0;
  try {
    if (shipment.shipped_at && shipment.expected_arrival) {
      const shipped = new Date(shipment.shipped_at).getTime();
      const expected = new Date(shipment.expected_arrival).getTime();
      const now = Date.now();
      if (expected > shipped) {
        progress = Math.max(0, Math.min(100, Math.round(((now - shipped) / (expected - shipped)) * 100)));
      }
    }
  } catch (e) {
    // ignore
  }

  // compose map-friendly objects
  const origin = warehouse ? { lat: warehouse.lat, lng: warehouse.lon, label: warehouse.name || 'Origin' } : null;
  const destination = order?.destination ? { lat: order.destination.lat, lng: order.destination.lon, label: `${order.destination.address || ''} ${order.destination.city || ''}`.trim() } : null;
  const currentLocation = telemetry ? { lat: telemetry.lat, lng: telemetry.lon, label: `Vehicle ${shipment.vehicle_id}` } : null;

  return {
    id: shipment.shipment_id,
    order: shipment.order_id,
    customer: customer?.name || null,
    status: shipment.status,
    eta: shipment.current_eta || shipment.expected_arrival || null,
    progress,
    origin,
    destination,
    currentLocation,
    raw: { shipment, order, warehouse, telemetry, customer },
  };
};
