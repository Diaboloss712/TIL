import pytest
import sys
import os
from unittest.mock import AsyncMock, patch
from mcp_server import(
    call_LLM_api,
)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.mark.asyncio
async def test_call_LLM():
    response = await call_LLM_api("다른 대답은 하지 말고 따옴표 안의 글자만 반환해줘. 'New World!'")
    assert response.strip() == "New World!"