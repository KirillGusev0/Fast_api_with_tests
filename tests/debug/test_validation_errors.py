#tests/debug/test_validation_errors.py

import pytest
from httpx import AsyncClient, ASGITransport

from main import app


@pytest.mark.debug
@pytest.mark.asyncio
async def test_create_user_invalid_payload(async_client, override_get_async_session):
    payload = {
        "username": "no_name",
        "password": "123",
    }

    response = await async_client.post("/api/v1/users/users/", json=payload)

    assert response.status_code == 422
