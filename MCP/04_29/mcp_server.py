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
import pytest
from unittest.mock import AsyncMock, patch


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
MODEL = "mistral"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
LOG_FILE = os.getenv("LOG_FILE")
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}