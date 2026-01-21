#tests/debug/test_app_lifecycle.py

import pytest
from asgi_lifespan import LifespanManager

from main import app


@pytest.mark.debug
@pytest.mark.asyncio
async def test_app_startup_and_shutdown():
    async with LifespanManager(app):
        assert True