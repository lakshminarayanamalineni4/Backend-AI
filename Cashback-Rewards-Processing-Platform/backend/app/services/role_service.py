from sqlalchemy.exc import SQLAlchemyError  # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Session  # pyright: ignore[reportMissingImports]
import logging

from app.core.exceptions.role import (
    RoleAlreadyExistsException,
    RoleNotFoundException,
)
from app.db.models.role import Role
from app.repositories.role_repository import RoleRepository
from app.schemas.role import (
    RoleCreate,
    RoleUpdate,
)

logger = logging.getLogger(__name__)


class RoleService:
    """
    Business logic for Role management.
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = RoleRepository(db)

    def _commit(self) -> None:
        """
        Commit the current transaction.
        """

        try:
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def create_role(
        self,
        role_create: RoleCreate,
    ) -> Role:

        existing = self.repository.get_by_name(
            role_create.name
        )

        if existing:
            logger.warning(
                "Role create rejected: name already exists name=%s",
                role_create.name,
            )
            raise RoleAlreadyExistsException(
                f"Role '{role_create.name}' already exists."
            )

        role = self.repository.create(
            name=role_create.name,
            description=role_create.description,
        )

        self._commit()
        logger.info(
            "Role created id=%s name=%s",
            role.id,
            role.name,
        )

        return role

    def get_role(
        self,
        role_id: int,
    ) -> Role:

        role = self.repository.get_by_id(role_id)

        if role is None:
            logger.warning(
                "Role get rejected: not found id=%s",
                role_id,
            )
            raise RoleNotFoundException(
                f"Role with id={role_id} was not found."
            )

        logger.info(
            "Role retrieved id=%s name=%s",
            role.id,
            role.name,
        )
        return role

    def list_roles(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Role]:

        roles = self.repository.list(
            offset=offset,
            limit=limit,
        )
        logger.info(
            "Roles listed offset=%s limit=%s returned=%s",
            offset,
            limit,
            len(roles),
        )
        return roles

    def update_role(
        self,
        role_id: int,
        role_update: RoleUpdate,
    ) -> Role:

        role = self.get_role(role_id)

        if (
            role_update.name
            and role_update.name != role.name
        ):
            existing = self.repository.get_by_name(
                role_update.name
            )

            if existing:
                logger.warning(
                    "Role update rejected: name already exists "
                    "id=%s name=%s",
                    role_id,
                    role_update.name,
                )
                raise RoleAlreadyExistsException(
                    f"Role '{role_update.name}' already exists."
                )

        updated_role = self.repository.update(
            role,
            name=role_update.name,
            description=role_update.description,
        )

        self._commit()

        logger.info(
            "Role updated id=%s name=%s",
            updated_role.id,
            updated_role.name,
        )
        return updated_role

    def delete_role(
        self,
        role_id: int,
    ) -> None:

        role = self.get_role(role_id)
        role_name = role.name

        self.repository.delete(role)

        self._commit()

        logger.info(
            "Role deleted id=%s name=%s",
            role_id,
            role_name,
        )

    def count_roles(
        self,
    ) -> int:

        total = self.repository.count()
        logger.info("Roles counted total=%s", total)
        return total
