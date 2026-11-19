"""
Shared pytest fixtures for backend unit tests.
"""

import os

# Must run before app.core.config / security imports.
# Force a valid Fernet key so a bad local .env cannot break tests.
os.environ["FIELD_ENCRYPTION_KEY"] = (
    "cGgN5A6uEr_ZJQLRQroIzwvjP1DB3HsfXeBtw0VQY6I="
)
os.environ.setdefault(
    "DATABASE_URL",
    "sqlite://",
)
os.environ.setdefault(
    "GEMINI_API_KEY",
    "test-gemini-key",
)

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.models import Role, User  # noqa: F401 — register metadata
from app.schemas.role import RoleCreate
from app.services.role_service import RoleService
from app.services.user_service import UserService


@pytest.fixture()
def db_session() -> Session:
    """
    Provide an isolated in-memory SQLite session per test.
    """

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def role_service(db_session: Session) -> RoleService:
    """
    RoleService bound to the isolated test session.
    """

    return RoleService(db_session)


@pytest.fixture()
def user_service(db_session: Session) -> UserService:
    """
    UserService bound to the isolated test session.
    """

    return UserService(db_session)


@pytest.fixture()
def seeded_role(role_service: RoleService) -> Role:
    """
    Create a role required by User.role_id FK.
    """

    return role_service.create_role(
        RoleCreate(
            name="ADMIN",
            description="Administrator",
        )
    )
