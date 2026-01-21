#tests/debug/test_healthcheck.py

import pytest
from httpx import AsyncClient, ASGITransport

from main import app


transport = ASGITransport(app=app)

@pytest.mark.debug
@pytest.mark.asyncio
async def test_openapi_available():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/openapi.json")

    assert response.status_code == 200


@pytest.mark.debug
@pytest.mark.asyncio
async def test_docs_available():
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/docs")

    assert response.status_code == 200
