import pytest
import mcp_server
from unittest.mock import AsyncMock, patch
from mcp_server import(
    call_LLM,
    generate_TDD,
)

@pytest.mark.asyncio
async def test_generate_tdd_success():
    source_code = """
    async def add_numbers(a: int, b: int) -> int:
        return a + b
    """
    result = await generate_TDD(source_code)

    # 1. 반환 타입 체크
    assert isinstance(result, dict)

    # 2. 키 존재 여부 체크
    assert "fail_test_code" in result
    assert "success_test_code" in result

    # 3. 타입 체크
    assert isinstance(result["fail_test_code"], str)
    assert isinstance(result["success_test_code"], str)

    # 4. 테스트 코드 패턴 체크
    assert "def test_" in result["fail_test_code"]
    assert "def test_" in result["success_test_code"]

@pytest.mark.asyncio
async def test_generate_tdd_failure_handling(monkeypatch):
    async def fake_call_LLM(prompt: str) -> str:
        return ""

    # monkeypatching 해서 일부러 LLM 실패 시뮬레이션
    monkeypatch.setattr(mcp_server, "call_LLM", fake_call_LLM)
    source_code = """
    async def add_numbers(a: int, b: int) -> int:
        return a + b
    """
    result = await generate_TDD(source_code)

    # 반환값 체크
    assert isinstance(result, dict)
    assert result["fail_test_code"] == ""
    assert result["success_test_code"] == ""