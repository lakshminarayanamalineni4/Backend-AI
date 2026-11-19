from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db.models.role import Role


class RoleRepository:
    """
    Repository responsible for database operations
    related to Role entities.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        name: str,
        description: str | None = None,
    ) -> Role:
        """
        Create and persist a new role.
        """

        role = Role(
            name=name,
            description=description,
        )

        self.db.add(role)
        self.db.flush()
        # self.db.refresh(role)

        return role

    def get_by_id(
        self,
        role_id: int,
    ) -> Role | None:
        """
        Retrieve a role by its primary key.
        """

        statement = select(Role).where(
            Role.id == role_id
        )

        return self.db.scalar(statement)

    def get_by_name(
        self,
        name: str,
    ) -> Role | None:
        """
        Retrieve a role by its unique name.
        """

        statement = select(Role).where(
            Role.name == name
        )

        return self.db.scalar(statement)

    def list(
        self,
        *,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Role]:
        """
        Retrieve a paginated list of roles.
        """

        statement = (
            select(Role)
            .order_by(Role.id)
            .offset(offset)
            .limit(limit)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def update(
        self,
        role: Role,
        *,
        name: str | None = None,
        description: str | None = None,
    ) -> Role:
        """
        Update an existing role.
        """

        if name is not None:
            role.name = name

        if description is not None:
            role.description = description

        self.db.flush()
        # self.db.refresh(role)

        return role

    def delete(
        self,
        role: Role,
    ) -> None:
        """
        Delete a role.
        """

        self.db.delete(role)
        self.db.flush()
        
    def count(self) -> int:
        """
        Return the total number of roles.
        """

        statement = select(
            func.count(Role.id)
        )

        return self.db.scalar(statement) or 0