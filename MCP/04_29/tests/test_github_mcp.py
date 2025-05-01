import pytest
from mcp_server import fetch_mcp_tools

@pytest.mark.asyncio
async def test_fetch_mcp_tools():
    result = await fetch_mcp_tools("https://thisisnotreal-test.com")
    assert isinstance(result, list)
    assert result == []

