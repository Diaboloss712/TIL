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

async def call_LLM_api(prompt:str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(f'{OLLAMA_URL}/api/generate', json=payload)
        data = response.json()
        return data.get("response", "")
