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
import traceback

# 설정 값
PORT = "8000"
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
REPO_PATH = Path(os.getenv("TIL_ROOT") or Path(__file__).resolve().parents[2])
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
LOG_FILE = os.getenv("LOG_FILE", "mcp_commit_log.txt")

# 로깅 함수
def log_message(msg: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")

# Conventional Commit 형식 검사 함수
def is_valid_convention(message: str) -> bool:
    message = message.strip("`\"' \n")
    valid_types = ["feat", "fix", "chore", "docs", "refactor", "test", "perf"]
    if ": " not in message:
        return False
    type_part = message.split(":", 1)[0]
    return type_part in valid_types

# 변경 파일들을 가져오는 함수
def get_modified_files() -> List[str]:
    try:
        changed = subprocess.check_output(["git", "diff", "--name-only"], cwd=str(REPO_PATH)).decode().splitlines()
        untracked = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"], cwd=str(REPO_PATH)).decode().splitlines()
        files = changed + untracked
        log_message(f"변경 파일 목록: {files}")
        return files
    except subprocess.CalledProcessError as e:
        log_message(f"❌ Git 명령어 오류: {e}")
        return []

# 파일별 diff 가져오기
def get_file_diff(file: str) -> str:
    try:
        diff = subprocess.check_output(["git", "diff", "--", file], cwd=str(REPO_PATH)).decode()
        return diff
    except subprocess.CalledProcessError as e:
        log_message(f"❌ 파일({file}) diff 추출 실패: {e}")
        return ""

# LLM으로 메시지 생성
def generate_commit_message(file: str, diff: str) -> str:
    prompt = (
        f'''파일 `{file}`의 변경 내용은 다음과 같습니다:\n{diff}\n\n
        이 변경 내용을 기반으로 한 줄짜리 Conventional Commit 형식의 커밋 메시지를 영어로 생성해 주세요.
        \n 형식은 반드시 다음을 따르세요: `feat: ...`, `fix: ...`, `refactor: ...` 등.
        내용이 다양할 경우 가장 핵심적인 convention을 하나만 골라 생성해주세요.'''
    )
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }
    try:
        res = httpx.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=30)
        commit_msg = res.json().get("response", "").strip()
        log_message(f"LLM으로부터 받은 메시지 for {file}: {commit_msg}")
        return commit_msg
    except Exception as e:
        log_message(f"❌ LLM 호출 실패({file}): {e}")
        return ""

# 파일 커밋
def commit_file(file: str) -> Dict[str, Any]:
    result = {"file": file, "status": None, "message": None}
    diff = get_file_diff(file)
    if not diff.strip():
        result["status"] = "skipped"
        result["message"] = "변경 내용 없음"
        log_message(f"[스킵] {file}: 변경 내용이 없음")
        return result

    commit_msg = generate_commit_message(file, diff)
    if not commit_msg:
        result["status"] = "failed"
        result["message"] = "LLM으로부터 메시지 생성 실패"
        return result

    if not is_valid_convention(commit_msg):
        result["status"] = "skipped"
        result["message"] = f"생성된 메시지가 Conventional Commit 형식이 아님: {commit_msg}"
        log_message(f"[형식 오류] {file}: {commit_msg}")
        return result

    try:
        subprocess.run(["git", "add", file], cwd=str(REPO_PATH), check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(REPO_PATH), check=True)
        result["status"] = "committed"
        result["message"] = commit_msg
        log_message(f"✅ {file} 커밋됨: {commit_msg}")
    except subprocess.CalledProcessError as e:
        result["status"] = "error"
        result["message"] = str(e)
        log_message(f"❌ Git 명령 실패({file}): {e}")
    return result

# 배치 커밋
@app.post("/commit/batch/", operation_id="batch_commit", description="파일별 커밋 및 자동 push 수행")
async def batch_commit() -> Dict[str, Any]:
    try:
        results = []
        files = get_modified_files()
        if not files:
            return {"status": "no_changes", "message": "변경된 파일이 없습니다."}

        for file in files:
            res = commit_file(file)
            results.append(res)

        try:
            subprocess.run(["git", "push"], cwd=str(REPO_PATH), check=True)
            push_status = "pushed"
            log_message("🌐 모든 커밋 후 push 완료")
        except subprocess.CalledProcessError as e:
            push_status = f"push error: {e}"
            log_message(f"❌ push 실패: {e}")

        return {"status": "done", "push_status": push_status, "details": results}

    except Exception as e:
        log_message(f"❌ batch_commit 예외: {e}\n{traceback.format_exc()}")
        return {"status": "error", "message": str(e)}

# MCP 마운트
mcp.mount()
mcp.setup_server()

if __name__ == "__main__":
    try:
        log_message("🔌 MCP 서버 시작 준비")
        log_message(f"🌐 MCP 서버 주소: http://{HOST}:{PORT}")
        uvicorn.run(app, host=HOST, port=int(PORT))
    except Exception as e:
        log_message(f"❌ MCP 서버 실행 중 예외 발생: {e}")