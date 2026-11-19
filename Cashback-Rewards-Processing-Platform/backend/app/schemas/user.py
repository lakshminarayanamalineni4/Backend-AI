from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    """
    Request schema for creating a new user.
    """

    email: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Unique email used for login.",
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Plaintext password; stored hashed only.",
    )

    mobile_number: str = Field(
        ...,
        min_length=8,
        max_length=20,
        description="Mobile number; stored encrypted, hashed for lookup.",
    )

    full_name: str | None = Field(
        default=None,
        max_length=255,
        description="Optional display name.",
    )

    role_id: int = Field(
        ...,
        gt=0,
        description="Foreign key to an existing role.",
    )

    is_active: bool = Field(
        default=True,
        description="Whether the user can authenticate.",
    )


class UserUpdate(BaseModel):
    """
    Request schema for partially updating an existing user.
    """

    email: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
        description="Updated unique email.",
    )

    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=128,
        description="Updated plaintext password; stored hashed only.",
    )

    mobile_number: str | None = Field(
        default=None,
        min_length=8,
        max_length=20,
        description="Updated mobile number; re-encrypted and re-hashed.",
    )

    full_name: str | None = Field(
        default=None,
        max_length=255,
        description="Updated display name.",
    )

    role_id: int | None = Field(
        default=None,
        gt=0,
        description="Updated role foreign key.",
    )

    is_active: bool | None = Field(
        default=None,
        description="Updated active flag.",
    )


class UserResponse(BaseModel):
    """
    Response schema for a user.
    Never includes password, hashed_password, mobile_encrypted, or mobile_hash.
    mobile_number is decrypted for the client.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    email: str

    full_name: str | None

    mobile_number: str

    role_id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime


class UserListResponse(BaseModel):
    """
    Paginated response schema for listing users.
    """

    items: list[UserResponse]

    total: int

    page: int

    page_size: int
