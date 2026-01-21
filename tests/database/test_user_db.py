# tests/database/test_user_db.py

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from apps.user.models import Users


pytestmark = pytest.mark.database


@pytest.mark.asyncio
async def test_create_user(db_session):
    user = Users(
        name="Test User",
        username="testuser",
        email="test@example.com",
        hashed_password="hashedpassword",
    )

    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    assert user.user_id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_get_user_by_id(db_session):
    user = Users(
        name="Get User",
        username="getuser",
        email="get@example.com",
        hashed_password="hashedpassword",
    )

    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)

    result = await db_session.get(Users, user.user_id)

    assert result is not None
    assert result.user_id == user.user_id
    assert result.username == "getuser"


@pytest.mark.asyncio
async def test_get_users_by_ids(db_session):
    user1 = Users(
        name="User 1",
        username="user1",
        email="user1@example.com",
        hashed_password="pass1",
    )
    user2 = Users(
        name="User 2",
        username="user2",
        email="user2@example.com",
        hashed_password="pass2",
    )

    db_session.add_all([user1, user2])
    await db_session.flush()

    result = await db_session.execute(
        select(Users).where(Users.username.in_(["user1", "user2"]))
    )
    users = result.scalars().all()

    assert len(users) == 2


@pytest.mark.asyncio
async def test_unique_username_constraint(db_session):
    user1 = Users(
        name="User A",
        username="uniqueuser",
        email="a@example.com",
        hashed_password="pass",
    )
    user2 = Users(
        name="User B",
        username="uniqueuser",
        email="b@example.com",
        hashed_password="pass",
    )

    db_session.add(user1)
    await db_session.flush()

    db_session.add(user2)

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_unique_email_constraint(db_session):
    user1 = Users(
        name="User A",
        username="emailuser1",
        email="unique@example.com",
        hashed_password="pass",
    )
    user2 = Users(
        name="User B",
        username="emailuser2",
        email="unique@example.com",
        hashed_password="pass",
    )

    db_session.add(user1)
    await db_session.flush()

    db_session.add(user2)

    with pytest.raises(IntegrityError):
        await db_session.flush()
