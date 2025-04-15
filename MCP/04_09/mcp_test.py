from fastapi_mcp import FastApiMCP
from fastapi import FastAPI
import subprocess
import httpx
import os
import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv
import uvicorn
from pathlib import Path

PORT = 8000
HOST = "127.0.0.1"
app = FastAPI()

mcp = FastApiMCP(
    app,
    name="commit-tools",
    description="commit-tools with Local LLM",
    base_url=f"http://{HOST}:{PORT}",
    describe_full_response_schema=True,
    describe_all_responses=True,
)

load_dotenv()
TIL_ROOT = Path(os.getenv("TIL_ROOT") or Path(__file__).resolve().parents[2])
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

LOG_FILE = "mcp_commit_log.txt"


def log_message(msg: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")


def is_valid_convention(message: str) -> bool:
    valid_types = ["feat", "fix", "chore", "docs", "refactor", "test", "perf"]
    return ": " in message and message.split(":", 1)[0] in valid_types


def get_modified_files_recursive() -> list[str]:
    from pathlib import Path

    log_message(f"📁 TIL_ROOT 경로 확인: {TIL_ROOT}")
    til_path = Path(TIL_ROOT)

    if not til_path.exists():
        raise FileNotFoundError(f"TIL_ROOT 경로가 존재하지 않음: {TIL_ROOT}")

    try:
        changed = subprocess.check_output(
            ["git", "diff", "--name-only"],
            cwd=str(til_path)
        ).decode().splitlines()

        untracked = subprocess.check_output(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=str(til_path)
        ).decode().splitlines()

        return changed + untracked

    except subprocess.CalledProcessError as e:
        log_message(f"❌ Git 명령어 오류: {e}")
        raise e


async def generate_commit_message(file_path: str) -> str:
    prompt = (
        f"다음 파일이 변경되었습니다: {file_path}\n"
        "해당 파일의 변경 내용에 기반하여 Conventional Commit 형식의 메시지를 작성해주세요.\n"
        "형식: `feat: ...`, `fix: ...`, `refactor: ...` 등, 한 줄로 작성해주세요."
    )
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }
    try:
        res = httpx.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=30)
        response = res.json().get("response", "").strip()
        return response
    except Exception as e:
        log_message(f"❌ Ollama 호출 실패 ({file_path}): {e}")
        return ""


@app.post("/commit/batch/", operation_id="batch_commit")
async def batch_commit():
    try:
        files = get_modified_files_recursive()
        log_message(f"🔍 변경 파일 목록: {files}")

        if not files:
            return {"status": "no_changes", "message": "변경된 파일이 없습니다."}

        results = []
        for file in files:
            diff = subprocess.check_output(["git", "diff", file]).decode()
            if not diff.strip():
                continue

            log_message(f"📄 {file} diff 추출 완료")
            prompt = (
                f"파일 `{file}`의 변경 내용은 다음과 같습니다:\n{diff}\n"
                "이 변경 내용을 기반으로 커밋 메시지를 한 줄로 제안해주세요..."
            )
            payload = {
                "model": "mistral",
                "prompt": prompt,
                "tools": [],
                "stream": False
            }

            res = httpx.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=30)
            suggestion = res.json().get("response", "").strip()
            log_message(f"🧠 제안된 메시지 for {file}: {suggestion}")

            if is_valid_convention(suggestion):
                subprocess.run(["git", "add", file], check=True)
                subprocess.run(["git", "commit", "-m", suggestion], check=True)
                results.append({"file": file, "message": suggestion, "status": "committed"})
            else:
                results.append({"file": file, "message": suggestion, "status": "skipped"})

        subprocess.run(["git", "push"], check=True)
        return {"status": "done", "details": results}

    except Exception as e:
        log_message(f"❌ batch_commit 예외: {e}")
        return {"status": "error", "message": str(e)}

mcp.mount()
mcp.setup_server()

if __name__ == "__main__":
    try:
        log_message("🔌 MCP 서버 시작 준비")
        log_message(f"🌐 MCP 서버 주소: http://{HOST}:{PORT}")
        uvicorn.run(app, host=HOST, port=PORT)
    except Exception as e:
        log_message(f"❌ MCP 서버 실행 중 예외 발생: {e}")