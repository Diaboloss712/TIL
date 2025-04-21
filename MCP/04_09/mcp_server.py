from fastapi import FastAPI, Request
from fastapi_mcp import FastApiMCP
import subprocess
import httpx
import os
import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv
import uvicorn
from pathlib import Path
import traceback
import requests
from datetime import timezone

# 설정 값
PORT = "8000"
HOST = "0.0.0.0"
app = FastAPI()
mcp = FastApiMCP(
    app,
    name="commit-tools",
    description="commit-tools with Local LLM",
    describe_full_response_schema=True,
    describe_all_responses=True,
)

load_dotenv()
REPO_PATH = Path(os.getenv("TIL_ROOT") or Path(__file__).resolve().parents[2])
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
LOG_FILE = os.getenv("LOG_FILE", "mcp_commit_log.txt")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

@app.post("/tools/define")
def define_tools():
    return {
        "tools": [
            {
                "name": "check_commit_activity",
                "description": "오늘 GitHub에 커밋이 있었는지 확인합니다.",
                "parameters": {}
            },
            {
                "name": "commit_if_needed",
                "description": "오늘 커밋이 없으면 자동 커밋을 수행합니다.",
                "parameters": {}
            },
            {
                "name": "batch_commit",
                "description": "변경된 파일을 커밋하고 push 합니다.",
                "parameters": {}
            }
        ]
    }

@app.post("/tools/call")
async def call_tool(request: Request):
    body = await request.json()
    name = body.get("name")
    args = body.get("arguments", {})

    if name == "check_commit_activity":
        return check_commit_activity()
    elif name == "commit_if_needed":
        return await commit_if_needed()
    elif name == "batch_commit":
        return await batch_commit()
    else:
        return {"error": f"Unknown tool: {name}"}


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

@app.get("/github/check_commit", operation_id="check_commit_activity", description="오늘 GitHub에 커밋이 있었는지 확인합니다.")
def check_commit_activity():
    today = datetime.datetime.now(timezone.utc).date()
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/events"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        events = response.json()
        for event in events:
            if event["type"] == "PushEvent":
                pushed_date = datetime.datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ").date()
                if pushed_date == today:
                    return {"status": "committed", "message": "오늘 GitHub에 커밋이 존재합니다."}
        return {"status": "no_commit", "message": "오늘 GitHub에 커밋 기록이 없습니다."}
    except Exception as e:
        return {"status": "error", "message": f"GitHub API 오류: {e}"}

@app.post("/commit/batch", operation_id="batch_commit", description="변경된 파일을 커밋하고 push 합니다.")
async def batch_commit():
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

@app.post("/commit/daily", operation_id="commit_if_needed", description="오늘 커밋이 없으면 자동 커밋 및 push 수행")
async def commit_if_needed():
    status = check_commit_activity()
    if status["status"] == "committed":
        return {"status": "skipped", "message": "이미 커밋이 존재합니다."}
    return await batch_commit()

# MCP 마운트
mcp.mount()
mcp.setup_server()

for tool in mcp.tools:
    print(f" - {tool.name}: {tool.description}")

if __name__ == "__main__":
    try:
        log_message("🔌 MCP 서버 시작 준비")
        log_message(f"🌐 MCP 서버 주소: http://{HOST}:{PORT}")
        uvicorn.run(app, host=HOST, port=int(PORT))
    except Exception as e:
        log_message(f"❌ MCP 서버 실행 중 예외 발생: {e}")
