from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any
from supabase import create_client, Client
from ...config import settings  # Import from src/config.py

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

# Dependency to get Supabase client (using service key for full access)
def get_supabase_client() -> Client:
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
        raise HTTPException(status_code=500, detail="Supabase configuration missing")
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)

class AnalyticsResponse(BaseModel):
    total_revenue: float
    delivery_success_rate: float
    avg_delivery_time: str
    customer_satisfaction: float
    revenue_trend: Dict[str, float]
    delivery_status_distribution: Dict[str, int]
    top_delivery_personnel: List[Dict[str, Any]]
    popular_routes: List[Dict[str, Any]]

@router.get("", response_model=AnalyticsResponse)
def get_analytics(supabase: Client = Depends(get_supabase_client)):
    """
    Retrieve the latest analytics summary data from Supabase.
    """
    try:
        response = supabase.table('analytics_summary').select('*').order('last_updated', desc=True).limit(1).execute()
        # If no analytics row exists, return a safe default object instead of 404 so the frontend doesn't fail
        if not response.data:
            return AnalyticsResponse(
                total_revenue=0.0,
                delivery_success_rate=0.0,
                avg_delivery_time="0 minutes",
                customer_satisfaction=0.0,
                revenue_trend={},
                delivery_status_distribution={},
                top_delivery_personnel=[],
                popular_routes=[],
            )

        summary = response.data[0]
        
        # Safely parse JSONB fields (handle if they are dict or str)
        def safe_parse_jsonb(field: Any) -> Dict:
            if isinstance(field, dict):
                return field
            try:
                import json
                return json.loads(field) if field else {}
            except:
                return {}
        
        revenue_trend = safe_parse_jsonb(summary.get('revenue_trend_json', {}))
        status_dist = safe_parse_jsonb(summary.get('delivery_status_distribution', {}))
        
        # Parse top personnel (assuming structure like {"personnel": [...]})
        top_personnel_raw = safe_parse_jsonb(summary.get('top_delivery_personnel', {}))
        top_personnel = top_personnel_raw.get('personnel', []) if 'personnel' in top_personnel_raw else []
        
        # Parse popular routes (assuming structure like {"routes": [...]})
        popular_routes_raw = safe_parse_jsonb(summary.get('popular_routes', {}))
        popular_routes = popular_routes_raw.get('routes', []) if 'routes' in popular_routes_raw else []
        
        return AnalyticsResponse(
            total_revenue=float(summary.get('total_revenue', 0)),
            delivery_success_rate=float(summary.get('delivery_success_rate', 0)),
            avg_delivery_time=str(summary.get('avg_delivery_time', '0 minutes')),
            customer_satisfaction=float(summary.get('customer_satisfaction', 0)),
            revenue_trend=revenue_trend,
            delivery_status_distribution=status_dist,
            top_delivery_personnel=top_personnel,
            popular_routes=popular_routes
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching analytics: {str(e)}")


@router.get("/summary", response_model=AnalyticsResponse)
def get_analytics_summary(supabase: Client = Depends(get_supabase_client)):
    """Alias endpoint to match legacy path /api/v1/analytics/summary"""
    return get_analytics(supabase)