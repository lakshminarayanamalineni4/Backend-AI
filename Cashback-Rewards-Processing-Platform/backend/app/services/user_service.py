from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import logging

from app.core.exceptions.role import RoleNotFoundException
from app.core.exceptions.user import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.core.security import (
    decrypt_mobile,
    encrypt_mobile,
    hash_mobile,
    hash_password,
)
from app.db.models.user import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)

logger = logging.getLogger(__name__)


class UserService:
    """
    Business logic for User management.
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)
        self.role_repository = RoleRepository(db)

    def _commit(self) -> None:
        """
        Commit the current transaction.
        """

        try:
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def _to_response(self, user: User) -> UserResponse:
        """
        Build API response with decrypted mobile_number.
        """

        return UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            mobile_number=decrypt_mobile(user.mobile_encrypted),
            role_id=user.role_id,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def _ensure_role_exists(
        self,
        role_id: int,
    ) -> None:
        role = self.role_repository.get_by_id(role_id)

        if role is None:
            logger.warning(
                "User operation rejected: role not found role_id=%s",
                role_id,
            )
            raise RoleNotFoundException(
                f"Role with id={role_id} was not found."
            )

    def _ensure_mobile_available(
        self,
        mobile_number: str,
        *,
        exclude_user_id: int | None = None,
    ) -> str:
        """
        Hash mobile and ensure no other user owns it.
        Returns the mobile_hash.
        """

        mobile_digest = hash_mobile(mobile_number)
        existing = self.repository.get_by_mobile_hash(
            mobile_digest
        )

        if existing and existing.id != exclude_user_id:
            logger.warning(
                "User operation rejected: mobile already exists "
                "user_id=%s",
                existing.id,
            )
            raise UserAlreadyExistsException(
                "User with this mobile number already exists."
            )

        return mobile_digest

    def create_user(
        self,
        user_create: UserCreate,
    ) -> UserResponse:

        existing = self.repository.get_by_email(
            user_create.email
        )

        if existing:
            logger.warning(
                "User create rejected: email already exists email=%s",
                user_create.email,
            )
            raise UserAlreadyExistsException(
                f"User with email '{user_create.email}' already exists."
            )

        self._ensure_role_exists(user_create.role_id)
        mobile_digest = self._ensure_mobile_available(
            user_create.mobile_number
        )

        user = self.repository.create(
            email=user_create.email,
            hashed_password=hash_password(
                user_create.password
            ),
            mobile_encrypted=encrypt_mobile(
                user_create.mobile_number
            ),
            mobile_hash=mobile_digest,
            full_name=user_create.full_name,
            role_id=user_create.role_id,
            is_active=user_create.is_active,
        )

        self._commit()
        logger.info(
            "User created id=%s email=%s role_id=%s",
            user.id,
            user.email,
            user.role_id,
        )

        return self._to_response(user)

    def get_user(
        self,
        user_id: int,
    ) -> UserResponse:

        user = self.repository.get_by_id(user_id)

        if user is None:
            logger.warning(
                "User get rejected: not found id=%s",
                user_id,
            )
            raise UserNotFoundException(
                f"User with id={user_id} was not found."
            )

        logger.info(
            "User retrieved id=%s email=%s",
            user.id,
            user.email,
        )
        return self._to_response(user)

    def list_users(
        self,
        offset: int = 0,
        limit: int = 20,
        mobile_number: str | None = None,
    ) -> list[UserResponse]:

        mobile_digest = None
        if mobile_number is not None:
            mobile_digest = hash_mobile(mobile_number)

        users = self.repository.list(
            offset=offset,
            limit=limit,
            mobile_hash=mobile_digest,
        )
        logger.info(
            "Users listed offset=%s limit=%s mobile_filter=%s returned=%s",
            offset,
            limit,
            mobile_number is not None,
            len(users),
        )
        return [self._to_response(user) for user in users]

    def update_user(
        self,
        user_id: int,
        user_update: UserUpdate,
    ) -> UserResponse:

        user = self.repository.get_by_id(user_id)

        if user is None:
            logger.warning(
                "User update rejected: not found id=%s",
                user_id,
            )
            raise UserNotFoundException(
                f"User with id={user_id} was not found."
            )

        if (
            user_update.email
            and user_update.email != user.email
        ):
            existing = self.repository.get_by_email(
                user_update.email
            )

            if existing:
                logger.warning(
                    "User update rejected: email already exists "
                    "id=%s email=%s",
                    user_id,
                    user_update.email,
                )
                raise UserAlreadyExistsException(
                    f"User with email '{user_update.email}' already exists."
                )

        if user_update.role_id is not None:
            self._ensure_role_exists(user_update.role_id)

        hashed = None
        if user_update.password is not None:
            hashed = hash_password(user_update.password)

        mobile_encrypted = None
        mobile_digest = None
        if user_update.mobile_number is not None:
            mobile_digest = self._ensure_mobile_available(
                user_update.mobile_number,
                exclude_user_id=user.id,
            )
            mobile_encrypted = encrypt_mobile(
                user_update.mobile_number
            )

        updated_user = self.repository.update(
            user,
            email=user_update.email,
            hashed_password=hashed,
            mobile_encrypted=mobile_encrypted,
            mobile_hash=mobile_digest,
            full_name=user_update.full_name,
            role_id=user_update.role_id,
            is_active=user_update.is_active,
        )

        self._commit()

        logger.info(
            "User updated id=%s email=%s",
            updated_user.id,
            updated_user.email,
        )
        return self._to_response(updated_user)

    def delete_user(
        self,
        user_id: int,
    ) -> None:

        user = self.repository.get_by_id(user_id)

        if user is None:
            logger.warning(
                "User delete rejected: not found id=%s",
                user_id,
            )
            raise UserNotFoundException(
                f"User with id={user_id} was not found."
            )

        user_email = user.email

        self.repository.delete(user)

        self._commit()

        logger.info(
            "User deleted id=%s email=%s",
            user_id,
            user_email,
        )

    def count_users(
        self,
    ) -> int:

        total = self.repository.count()
        logger.info("Users counted total=%s", total)
        return total
