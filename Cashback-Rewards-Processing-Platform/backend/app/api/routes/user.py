from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import UserService


router = APIRouter()


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create User",
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new user.
    """
    service = UserService(db)

    return service.create_user(user)


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="List Users",
)
def list_users(
    offset: int = 0,
    limit: int = 20,
    mobile_number: str | None = None,
    db: Session = Depends(get_db),
):
    """
    Retrieve users. Optional exact mobile_number filter uses mobile_hash.
    """
    service = UserService(db)

    return service.list_users(
        offset=offset,
        limit=limit,
        mobile_number=mobile_number,
    )


@router.get(
    "/count",
    summary="Count Users",
)
def count_users(
    db: Session = Depends(get_db),
):
    """
    Return total number of users.
    """
    service = UserService(db)

    return {
        "count": service.count_users()
    }


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get User",
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve a user by ID.
    """
    service = UserService(db)

    return service.get_user(user_id)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update User",
)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing user.
    """
    service = UserService(db)

    return service.update_user(
        user_id,
        user,
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete User",
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a user.
    """
    service = UserService(db)

    service.delete_user(user_id)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
