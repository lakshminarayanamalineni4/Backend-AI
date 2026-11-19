"""
Unit tests for UserService business logic.
"""

import pytest

from app.core.exceptions.role import RoleNotFoundException
from app.core.exceptions.user import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.core.security import hash_mobile
from app.db.models.role import Role
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.user_service import UserService


def _user_create(
    role_id: int,
    *,
    email: str = "admin@bigcity.test",
    mobile_number: str = "+919876543210",
    full_name: str | None = "Admin User",
) -> UserCreate:
    return UserCreate(
        email=email,
        password="Secret123!",
        mobile_number=mobile_number,
        full_name=full_name,
        role_id=role_id,
    )


class TestCreateUser:
    def test_create_user_success(
        self,
        user_service: UserService,
        seeded_role: Role,
        db_session,
    ) -> None:
        user = user_service.create_user(
            _user_create(seeded_role.id)
        )

        assert user.id is not None
        assert user.email == "admin@bigcity.test"
        assert user.mobile_number == "+919876543210"
        assert user.full_name == "Admin User"
        assert user.role_id == seeded_role.id
        assert user.is_active is True

        stored = UserRepository(db_session).get_by_id(user.id)
        assert stored is not None
        assert stored.hashed_password != "Secret123!"
        assert stored.mobile_encrypted != "+919876543210"
        assert stored.mobile_hash == hash_mobile("+919876543210")

    def test_create_user_duplicate_email_raises(
        self,
        user_service: UserService,
        seeded_role: Role,
    ) -> None:
        user_service.create_user(
            _user_create(seeded_role.id)
        )

        with pytest.raises(UserAlreadyExistsException):
            user_service.create_user(
                _user_create(
                    seeded_role.id,
                    mobile_number="+919111111111",
                )
            )

    def test_create_user_duplicate_mobile_raises(
        self,
        user_service: UserService,
        seeded_role: Role,
    ) -> None:
        user_service.create_user(
            _user_create(seeded_role.id)
        )

        with pytest.raises(UserAlreadyExistsException):
            user_service.create_user(
                _user_create(
                    seeded_role.id,
                    email="other@bigcity.test",
                    mobile_number="+91 98765 43210",
                )
            )

    def test_create_user_missing_role_raises(
        self,
        user_service: UserService,
    ) -> None:
        with pytest.raises(RoleNotFoundException):
            user_service.create_user(_user_create(role_id=999))


class TestGetUser:
    def test_get_user_success(
        self,
        user_service: UserService,
        seeded_role: Role,
    ) -> None:
        created = user_service.create_user(
            _user_create(seeded_role.id)
        )

        found = user_service.get_user(created.id)

        assert found.id == created.id
        assert found.email == created.email
        assert found.mobile_number == "+919876543210"

    def test_get_user_missing_raises(
        self,
        user_service: UserService,
    ) -> None:
        with pytest.raises(UserNotFoundException):
            user_service.get_user(999)


class TestListAndCountUsers:
    def test_list_users_returns_created_users(
        self,
        user_service: UserService,
        seeded_role: Role,
    ) -> None:
        user_service.create_user(
            _user_create(
                seeded_role.id,
                email="a@bigcity.test",
                mobile_number="+919111111111",
            )
        )
        user_service.create_user(
            _user_create(
                seeded_role.id,
                email="b@bigcity.test",
                mobile_number="+919222222222",
            )
        )

        users = user_service.list_users()

        assert len(users) == 2
        assert {user.email for user in users} == {
            "a@bigcity.test",
            "b@bigcity.test",
        }

    def test_list_users_filters_by_mobile(
        self,
        user_service: UserService,
        seeded_role: Role,
    ) -> None:
        user_service.create_user(
            _user_create(
                seeded_role.id,
                email="a@bigcity.test",
                mobile_number="+919111111111",
            )
        )
        user_service.create_user(
            _user_create(
                seeded_role.id,
                email="b@bigcity.test",
                mobile_number="+919222222222",
            )
        )

        users = user_service.list_users(
            mobile_number="+91 91111 11111"
        )

        assert len(users) == 1
        assert users[0].email == "a@bigcity.test"
        assert users[0].mobile_number == "+919111111111"

    def test_list_users_respects_pagination(
        self,
        user_service: UserService,
        seeded_role: Role,
    ) -> None:
        user_service.create_user(
            _user_create(
                seeded_role.id,
                email="a@bigcity.test",
                mobile_number="+919111111111",
            )
        )
        user_service.create_user(
            _user_create(
                seeded_role.id,
                email="b@bigcity.test",
                mobile_number="+919222222222",
            )
        )
        user_service.create_user(
            _user_create(
                seeded_role.id,
                email="c@bigcity.test",
                mobile_number="+919333333333",
            )
        )

        page = user_service.list_users(offset=1, limit=1)

        assert len(page) == 1
        assert page[0].email == "b@bigcity.test"

    def test_count_users(
        self,
        user_service: UserService,
        seeded_role: Role,
    ) -> None:
        assert user_service.count_users() == 0

        user_service.create_user(
            _user_create(
                seeded_role.id,
                email="a@bigcity.test",
                mobile_number="+919111111111",
            )
        )
        user_service.create_user(
            _user_create(
                seeded_role.id,
                email="b@bigcity.test",
                mobile_number="+919222222222",
            )
        )

        assert user_service.count_users() == 2


class TestUpdateUser:
    def test_update_user_success(
        self,
        user_service: UserService,
        seeded_role: Role,
    ) -> None:
        created = user_service.create_user(
            _user_create(seeded_role.id)
        )

        updated = user_service.update_user(
            created.id,
            UserUpdate(
                full_name="Updated Name",
                mobile_number="+919000000000",
            ),
        )

        assert updated.id == created.id
        assert updated.full_name == "Updated Name"
        assert updated.mobile_number == "+919000000000"

    def test_update_user_email_conflict_raises(
        self,
        user_service: UserService,
        seeded_role: Role,
    ) -> None:
        user_service.create_user(
            _user_create(
                seeded_role.id,
                email="a@bigcity.test",
                mobile_number="+919111111111",
            )
        )
        other = user_service.create_user(
            _user_create(
                seeded_role.id,
                email="b@bigcity.test",
                mobile_number="+919222222222",
            )
        )

        with pytest.raises(UserAlreadyExistsException):
            user_service.update_user(
                other.id,
                UserUpdate(email="a@bigcity.test"),
            )

    def test_update_user_mobile_conflict_raises(
        self,
        user_service: UserService,
        seeded_role: Role,
    ) -> None:
        user_service.create_user(
            _user_create(
                seeded_role.id,
                email="a@bigcity.test",
                mobile_number="+919111111111",
            )
        )
        other = user_service.create_user(
            _user_create(
                seeded_role.id,
                email="b@bigcity.test",
                mobile_number="+919222222222",
            )
        )

        with pytest.raises(UserAlreadyExistsException):
            user_service.update_user(
                other.id,
                UserUpdate(mobile_number="+919111111111"),
            )

    def test_update_user_missing_raises(
        self,
        user_service: UserService,
    ) -> None:
        with pytest.raises(UserNotFoundException):
            user_service.update_user(
                999,
                UserUpdate(full_name="Nope"),
            )


class TestDeleteUser:
    def test_delete_user_success(
        self,
        user_service: UserService,
        seeded_role: Role,
    ) -> None:
        created = user_service.create_user(
            _user_create(seeded_role.id)
        )

        user_service.delete_user(created.id)

        assert user_service.count_users() == 0

        with pytest.raises(UserNotFoundException):
            user_service.get_user(created.id)

    def test_delete_user_missing_raises(
        self,
        user_service: UserService,
    ) -> None:
        with pytest.raises(UserNotFoundException):
            user_service.delete_user(999)
