from fastapi import FastAPI, Body
from pydantic import BaseModel
import subprocess
import httpx
import os
import datetime
import asyncio
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="MCP Commit Tool API")

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

LOG_FILE = "mcp_commit_log.txt"

def log_message(msg: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")

def is_valid_convention(message: str) -> bool:
    valid_types = ["feat", "fix", "chore", "docs", "refactor", "test", "perf"]
    if ": " not in message:
        return False
    type_part = message.split(":", 1)[0]
    return type_part in valid_types

def get_modified_files() -> list[str]:
    changed = subprocess.check_output(["git", "diff", "--name-only"]).decode().splitlines()
    untracked = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"]).decode().splitlines()
    return changed + untracked

class CommitRequest(BaseModel):
    message: str

@app.post("/validate-commit")
def validate_commit_convention(req: CommitRequest):
    message = req.message
    if not is_valid_convention(message):
        log_message(f"[검사 실패] '{message}'")
        return {"status": "invalid", "reason": "Conventional Commit 형식이 아님"}

    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push"], check=True)
        log_message(f"✅ 커밋 & 푸시 완료됨: '{message}'")
        return {"status": "success", "message": "커밋 및 푸시 완료됨"}
    except subprocess.CalledProcessError as e:
        log_message(f"❌ Git 명령 실패: {e}")
        return {"status": "error", "error": str(e)}

@app.get("/check-activity")
def check_commit_activity():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/events"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    today = datetime.datetime.utcnow().date()

    try:
        response = httpx.get(url, headers=headers)
        if response.status_code != 200:
            return {"status": "error", "message": f"GitHub API 오류: {response.status_code}"}

        events = response.json()
        for event in events:
            if event["type"] == "PushEvent":
                event_date = datetime.datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ").date()
                if event_date == today:
                    return {"status": "done", "message": "오늘 커밋했습니다."}

        suggestion = asyncio.run(suggest_commit_message_based_on_changes())
        log_message("⚠️ 오늘 커밋 없음 → 커밋 제안 요청됨")
        log_message(suggestion)

        extracted = extract_first_commit_line(suggestion)
        if extracted:
            result = validate_commit_convention(CommitRequest(message=extracted))
            return {
                "status": "committed",
                "suggested_message": extracted,
                "result": result
            }
        else:
            log_message("❌ 커밋 메시지를 추출하지 못했습니다")
            return {
                "status": "suggested_only",
                "message": "커밋 메시지를 추출하지 못했습니다.",
                "suggestion": suggestion
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}

async def suggest_commit_message_based_on_changes() -> str:
    changed_files = get_modified_files()
    if not changed_files:
        return "변경된 파일이 없습니다."

    file_list_str = "\n".join(f"- {f}" for f in changed_files)
    prompt = (
    f"다음 파일들이 변경되었습니다:\n{file_list_str}\n"
    "이 변경 사항을 기반으로 한 줄짜리 커밋 메시지를 하나만 제안해주세요. "
    "형식은 반드시 다음을 따르세요: `feat: ...`, `fix: ...`, `refactor: ...` 등. "
    "영어로, 소문자로 시작하며 콜론 뒤에 한 칸 띄고 메시지를 작성해주세요. "
    "예시: `feat: add login validation`"
    )


    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }

    try:
        res = httpx.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=30)
        answer = res.json().get("response", "")
        return answer.strip()
    except Exception as e:
        return f"Ollama 호출 실패: {e}"

def extract_first_commit_line(suggestion: str) -> str:
    lines = suggestion.split("\n")
    for line in lines:
        line = line.strip("- •*").strip()
        if any(line.startswith(t) for t in ["feat:", "fix:", "chore:", "docs:", "refactor:", "test:", "perf:"]):
            return line
    return ""

@app.get("/")
def root():
    return {"message": "MCP Commit Tool API 작동 중"}