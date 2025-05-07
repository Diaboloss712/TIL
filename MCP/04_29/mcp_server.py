from fastapi import FastAPI
from fastmcp import FastMCP
from dotenv import load_dotenv
from pathlib import Path
import subprocess
import httpx
import os
import asyncio
import json
import traceback
import datetime


# 설정 값
PORT = "8000"
HOST = "0.0.0.0"
app = FastAPI()
mcp = FastMCP(
    app,
)

load_dotenv()
REPO_PATH = Path(os.getenv("TIL_ROOT") or Path(__file__).resolve().parents[2])
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
MODEL = os.getenv("MODEL")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
LOG_FILE = os.getenv("LOG_FILE")
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# 로깅 함수
def log_message(msg: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")

# 로컬 LLM 호출
@mcp.tool(name="LLM", description="Local LLM")
async def call_LLM(prompt:str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(f"{OLLAMA_URL}/api/generate", json=payload)
            if response.status_code != 200:
                log_message(f"call_LLM 실패 - status: {response.status_code}, body: {response.text}")
                return ""
            data = response.json()
            return data.get("response", "").strip()
    except Exception as e:
        log_message(f"call_LLM 예외 발생: {e}")
        return ""

# TDD 코드 작성 요청
@mcp.tool(name="TDD", description="TDD 코드 작성")
async def generate_TDD(source_code:str) -> str:
    fail_prompt = f"""
    당신은 TDD 전문가입니다.
    아래 Python 코드에 대해, 아직 기능이 완성되지 않은 상황을 가정하고, 실패하는 테스트 코드를 작성하세요.
        - pytest 사용
        - 실패하는 테스트를 작성
        - 성공하는 테스트를 작성하지 말 것
    [코드 시작]
    {source_code}
    [코드 끝]
    """

    success_prompt = f"""
    당신은 TDD 전문가입니다.
    아래 Python 코드에 대해, 기능이 완성된 상황을 가정하고, 성공하는 테스트 코드를 작성하세요.
    - pytest 사용
    - 통과하는 테스트 코드를 작성
    - 비동기(async) 코드라면 async 테스트로 작성
    [코드 시작]
    {source_code}
    [코드 끝]
    """

    try:
        fail_test_code = await call_LLM(fail_prompt)
        success_test_code = await call_LLM(success_prompt)

        if not is_valid_test_code(fail_test_code):
            raise Exception("Fail 테스트 코드 검증 실패")
        if not is_valid_test_code(success_test_code):
            raise Exception("Success 테스트 코드 검증 실패")

        return {
            "fail_test_code": fail_test_code,
            "success_test_code": success_test_code
        }

    except Exception as e:
        log_message(f"generate_tdd 예외 발생: {e}")
        return {
            "fail_test_code": "",
            "success_test_code": ""
        }
    
# 테스트 코드 검증(추가 조건 필요)
def is_valid_test_code(text: str) -> bool:
    if not text.strip():
        return False
    if "def test_" not in text:
        return False
    return True

# MCP 툴 목록 가져오기
async def fetch_mcp_tools(server_url: str) -> list:
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            res = await client.post(f"{server_url}/tools/list", json={})
            return res.json().get("tools", [])
    except Exception:
        return []