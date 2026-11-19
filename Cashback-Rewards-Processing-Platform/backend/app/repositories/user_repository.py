from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db.models.user import User


class UserRepository:
    """
    Repository responsible for database operations
    related to User entities.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        email: str,
        hashed_password: str,
        mobile_encrypted: str,
        mobile_hash: str,
        full_name: str | None = None,
        role_id: int,
        is_active: bool = True,
    ) -> User:
        """
        Create and persist a new user.
        """

        user = User(
            email=email,
            hashed_password=hashed_password,
            mobile_encrypted=mobile_encrypted,
            mobile_hash=mobile_hash,
            full_name=full_name,
            role_id=role_id,
            is_active=is_active,
        )

        self.db.add(user)
        self.db.flush()

        return user

    def get_by_id(
        self,
        user_id: int,
    ) -> User | None:
        """
        Retrieve a user by its primary key.
        """

        statement = select(User).where(
            User.id == user_id
        )

        return self.db.scalar(statement)

    def get_by_email(
        self,
        email: str,
    ) -> User | None:
        """
        Retrieve a user by its unique email.
        """

        statement = select(User).where(
            User.email == email
        )

        return self.db.scalar(statement)

    def get_by_mobile_hash(
        self,
        mobile_hash: str,
    ) -> User | None:
        """
        Retrieve a user by mobile HMAC hash (exact-match lookup).
        """

        statement = select(User).where(
            User.mobile_hash == mobile_hash
        )

        return self.db.scalar(statement)

    def list(
        self,
        *,
        offset: int = 0,
        limit: int = 20,
        mobile_hash: str | None = None,
    ) -> list[User]:
        """
        Retrieve a paginated list of users.
        Optionally filter by mobile_hash.
        """

        statement = select(User)

        if mobile_hash is not None:
            statement = statement.where(
                User.mobile_hash == mobile_hash
            )

        statement = (
            statement
            .order_by(User.id)
            .offset(offset)
            .limit(limit)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def update(
        self,
        user: User,
        *,
        email: str | None = None,
        hashed_password: str | None = None,
        mobile_encrypted: str | None = None,
        mobile_hash: str | None = None,
        full_name: str | None = None,
        role_id: int | None = None,
        is_active: bool | None = None,
    ) -> User:
        """
        Update an existing user.
        """

        if email is not None:
            user.email = email

        if hashed_password is not None:
            user.hashed_password = hashed_password

        if mobile_encrypted is not None:
            user.mobile_encrypted = mobile_encrypted

        if mobile_hash is not None:
            user.mobile_hash = mobile_hash

        if full_name is not None:
            user.full_name = full_name

        if role_id is not None:
            user.role_id = role_id

        if is_active is not None:
            user.is_active = is_active

        self.db.flush()

        return user

    def delete(
        self,
        user: User,
    ) -> None:
        """
        Delete a user.
        """

        self.db.delete(user)
        self.db.flush()

    def count(self) -> int:
        """
        Return the total number of users.
        """

        statement = select(
            func.count(User.id)
        )

        return self.db.scalar(statement) or 0
