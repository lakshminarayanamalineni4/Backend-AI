from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RoleCreate(BaseModel):
    """
    Request schema for creating a new role.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Unique name of the role.",
    )

    description: str | None = Field(
        default=None,
        max_length=500,
        description="Optional description of the role.",
    )


class RoleUpdate(BaseModel):
    """
    Request schema for partially updating an existing role.
    """

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
        description="Updated unique name of the role.",
    )

    description: str | None = Field(
        default=None,
        max_length=500,
        description="Updated description of the role.",
    )


class RoleResponse(BaseModel):
    """
    Response schema for a role.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    name: str

    description: str | None

    created_at: datetime

    updated_at: datetime


class RoleListResponse(BaseModel):
    """
    Paginated response schema for listing roles.
    """

    items: list[RoleResponse]

    total: int

    page: int

    page_size: int