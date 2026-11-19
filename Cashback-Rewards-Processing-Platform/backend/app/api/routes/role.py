from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.role import (
    RoleCreate,
    RoleResponse,
    RoleUpdate,
)
from app.services.role_service import RoleService


router = APIRouter()


@router.post(
    "/",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Role",
)
def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new role.
    """
    service = RoleService(db)

    return service.create_role(role)


@router.get(
    "/",
    response_model=list[RoleResponse],
    summary="List Roles",
)
def list_roles(
    offset: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """
    Retrieve all roles.
    """
    service = RoleService(db)

    return service.list_roles(
        offset=offset,
        limit=limit,
    )


@router.get(
    "/count",
    summary="Count Roles",
)
def count_roles(
    db: Session = Depends(get_db),
):
    """
    Return total number of roles.
    """
    service = RoleService(db)

    return {
        "count": service.count_roles()
    }


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
    summary="Get Role",
)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve a role by ID.
    """
    service = RoleService(db)

    return service.get_role(role_id)


@router.put(
    "/{role_id}",
    response_model=RoleResponse,
    summary="Update Role",
)
def update_role(
    role_id: int,
    role: RoleUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing role.
    """
    service = RoleService(db)

    return service.update_role(
        role_id,
        role,
    )


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Role",
)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a role.
    """
    service = RoleService(db)

    service.delete_role(role_id)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )