from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from typing import Optional
from uuid import UUID
from ... import services, security, database
from ...schemas import user as user_schema
from ...models import Customer
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/users",
    response_model=user_schema.UserPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create user with specific role (Admin only)",
    description="Admin can create users with any role: customer, delivery_guy, or admin"
)
def create_user_by_admin(
    user: user_schema.AdminUserCreate,
    db: Session = Depends(database.get_db),
    current_user: Customer = Depends(security.get_admin_user)
):
    """Admin creates a user with specified role"""
    try:
        # Check if email already exists
        db_user = services.user_service.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        return services.user_service.create_user_with_role(db=db, user=user)
        
    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection unavailable"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.get(
    "/users",
    response_model=user_schema.UserListResponse,
    summary="Get all users (Admin only)",
    description="List all users with optional filtering by role"
)
def list_users(
    role: Optional[str] = Query(None, description="Filter by role: customer, delivery_guy, admin"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(database.get_db),
    current_user: Customer = Depends(security.get_admin_user)
):
    """Get list of all users"""
    try:
        if role:
            users = services.user_service.get_users_by_role(db, role=role, skip=skip, limit=limit)
        else:
            users = services.user_service.get_all_users(db, skip=skip, limit=limit)
        
        total = len(users)
        return {"users": users, "total": total}
        
    except OperationalError as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection unavailable"
        )
    except Exception as e:
        logger.error(f"Unexpected error listing users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.get(
    "/users/{user_id}",
    response_model=user_schema.UserPublic,
    summary="Get user by ID (Admin only)",
    description="Get detailed information about a specific user"
)
def get_user(
    user_id: UUID,
    db: Session = Depends(database.get_db),
    current_user: Customer = Depends(security.get_admin_user)
):
    """Get user by ID"""
    try:
        user = services.user_service.get_user_by_id(db, customer_id=str(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.patch(
    "/users/{user_id}",
    response_model=user_schema.UserPublic,
    summary="Update user (Admin only)",
    description="Update user information or deactivate user account"
)
def update_user(
    user_id: UUID,
    user_update: user_schema.UserUpdate,
    db: Session = Depends(database.get_db),
    current_user: Customer = Depends(security.get_admin_user)
):
    """Update user information"""
    try:
        user = services.user_service.update_user(db, customer_id=user_id, user_update=user_update)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error updating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Deactivate user (Admin only)",
    description="Soft delete user by setting is_active=False"
)
def delete_user(
    user_id: UUID,
    db: Session = Depends(database.get_db),
    current_user: Customer = Depends(security.get_admin_user)
):
    """Deactivate a user (soft delete)"""
    try:
        # Prevent self-deletion
        if str(user_id) == str(current_user.customer_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot deactivate your own account"
            )
        
        success = services.user_service.delete_user(db, customer_id=user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {"message": "User deactivated successfully", "user_id": str(user_id)}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error deleting user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.get(
    "/delivery-personnel",
    response_model=user_schema.UserListResponse,
    summary="Get all delivery personnel (Admin only)",
    description="List all users with delivery_guy role"
)
def list_delivery_personnel(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(database.get_db),
    current_user: Customer = Depends(security.get_admin_user)
):
    """Get list of delivery personnel"""
    try:
        users = services.user_service.get_users_by_role(db, role="delivery_guy", skip=skip, limit=limit)
        return {"users": users, "total": len(users)}
        
    except Exception as e:
        logger.error(f"Unexpected error listing delivery personnel: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )
