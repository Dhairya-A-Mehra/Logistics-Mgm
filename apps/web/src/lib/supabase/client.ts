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
