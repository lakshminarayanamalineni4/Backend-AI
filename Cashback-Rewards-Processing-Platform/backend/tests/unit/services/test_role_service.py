"""
Unit tests for RoleService business logic.
"""

import pytest

from app.core.exceptions.role import (
    RoleAlreadyExistsException,
    RoleNotFoundException,
)
from app.schemas.role import RoleCreate, RoleUpdate
from app.services.role_service import RoleService


class TestCreateRole:
    def test_create_role_success(
        self,
        role_service: RoleService,
    ) -> None:
        role = role_service.create_role(
            RoleCreate(
                name="admin",
                description="Administrator",
            )
        )

        assert role.id is not None
        assert role.name == "admin"
        assert role.description == "Administrator"

    def test_create_role_duplicate_name_raises(
        self,
        role_service: RoleService,
    ) -> None:
        role_service.create_role(
            RoleCreate(name="admin", description="First")
        )

        with pytest.raises(RoleAlreadyExistsException):
            role_service.create_role(
                RoleCreate(name="admin", description="Second")
            )


class TestGetRole:
    def test_get_role_success(
        self,
        role_service: RoleService,
    ) -> None:
        created = role_service.create_role(
            RoleCreate(name="viewer")
        )

        found = role_service.get_role(created.id)

        assert found.id == created.id
        assert found.name == "viewer"

    def test_get_role_missing_raises(
        self,
        role_service: RoleService,
    ) -> None:
        with pytest.raises(RoleNotFoundException):
            role_service.get_role(999)


class TestListAndCountRoles:
    def test_list_roles_returns_created_roles(
        self,
        role_service: RoleService,
    ) -> None:
        role_service.create_role(RoleCreate(name="admin"))
        role_service.create_role(RoleCreate(name="editor"))

        roles = role_service.list_roles()

        assert len(roles) == 2
        assert {role.name for role in roles} == {
            "admin",
            "editor",
        }

    def test_list_roles_respects_pagination(
        self,
        role_service: RoleService,
    ) -> None:
        role_service.create_role(RoleCreate(name="aa"))
        role_service.create_role(RoleCreate(name="bb"))
        role_service.create_role(RoleCreate(name="cc"))

        page = role_service.list_roles(offset=1, limit=1)

        assert len(page) == 1
        assert page[0].name == "bb"

    def test_count_roles(
        self,
        role_service: RoleService,
    ) -> None:
        assert role_service.count_roles() == 0

        role_service.create_role(RoleCreate(name="admin"))
        role_service.create_role(RoleCreate(name="editor"))

        assert role_service.count_roles() == 2


class TestUpdateRole:
    def test_update_role_success(
        self,
        role_service: RoleService,
    ) -> None:
        created = role_service.create_role(
            RoleCreate(
                name="editor",
                description="Can edit",
            )
        )

        updated = role_service.update_role(
            created.id,
            RoleUpdate(
                name="senior-editor",
                description="Senior editor",
            ),
        )

        assert updated.id == created.id
        assert updated.name == "senior-editor"
        assert updated.description == "Senior editor"

    def test_update_role_rename_conflict_raises(
        self,
        role_service: RoleService,
    ) -> None:
        role_service.create_role(RoleCreate(name="admin"))
        editor = role_service.create_role(
            RoleCreate(name="editor")
        )

        with pytest.raises(RoleAlreadyExistsException):
            role_service.update_role(
                editor.id,
                RoleUpdate(name="admin"),
            )

    def test_update_role_missing_raises(
        self,
        role_service: RoleService,
    ) -> None:
        with pytest.raises(RoleNotFoundException):
            role_service.update_role(
                999,
                RoleUpdate(description="Nope"),
            )


class TestDeleteRole:
    def test_delete_role_success(
        self,
        role_service: RoleService,
    ) -> None:
        created = role_service.create_role(
            RoleCreate(name="temp")
        )

        role_service.delete_role(created.id)

        assert role_service.count_roles() == 0

        with pytest.raises(RoleNotFoundException):
            role_service.get_role(created.id)

    def test_delete_role_missing_raises(
        self,
        role_service: RoleService,
    ) -> None:
        with pytest.raises(RoleNotFoundException):
            role_service.delete_role(999)
