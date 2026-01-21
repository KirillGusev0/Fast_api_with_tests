#tests/debug/test_db_integrity.py

import pytest
from sqlalchemy import text

@pytest.mark.debug
@pytest.mark.asyncio
async def test_database_connection_alive(db_session):
    result = await db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1