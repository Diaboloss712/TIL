from mcp.server.fastmcp import FastMCP
import subprocess
import httpx
import os
import datetime
import json
import sys
import asyncio
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("commit-tools")

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
    return message.split(":", 1)[0] in valid_types

def get_modified_files() -> list[str]:
    changed = subprocess.check_output(["git", "diff", "--name-only"]).decode().splitlines()
    untracked = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"]).decode().splitlines()
    return changed + untracked

@mcp.tool()
async def validate_commit_convention(message: str) -> dict:
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

@mcp.tool()
async def check_commit_activity() -> dict:
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

        suggestion = await suggest_commit_message_based_on_changes()
        log_message("⚠️ 오늘 커밋 없음 → 커밋 제안 요청됨")
        log_message(suggestion)

        extracted = extract_first_commit_line(suggestion)
        if extracted:
            result = await validate_commit_convention(extracted)
            return {
                "status": "committed",
                "suggested_message": extracted,
                "result": result
            }
        else:
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
        "tools": tool_schemas(),
        "stream": False
    }

    try:
        res = httpx.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=30)
        tool_call = res.json()
        log_message(f"🧠 모델 응답: {tool_call}")
        if isinstance(tool_call, dict) and "name" in tool_call:
            log_message(f"⚙️ LLM이 선택한 툴: {tool_call['name']} {tool_call.get('arguments', {})}")
            return await dispatch_tool(tool_call)
        return tool_call.get("response", "").strip()
    except Exception as e:
        return f"Ollama 호출 실패: {e}"

def extract_first_commit_line(suggestion: str) -> str:
    for line in suggestion.splitlines():
        line = line.strip("- •*` ")
        if any(line.startswith(t) for t in ["feat:", "fix:", "chore:", "docs:", "refactor:", "test:", "perf:"]):
            return line
    return ""

def tool_schemas() -> List[Dict[str, Any]]:
    return [
        {
            "name": "check_commit_activity",
            "description": "오늘 GitHub에 커밋했는지 확인",
            "parameters": {"type": "object", "properties": {}}
        },
        {
            "name": "validate_commit_convention",
            "description": "커밋 메시지를 검사하고 통과하면 커밋 및 푸시",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "검사할 커밋 메시지"}
                },
                "required": ["message"]
            }
        }
    ]

async def dispatch_tool(tool_call: Dict[str, Any]) -> dict:
    name = tool_call.get("name")
    args = tool_call.get("arguments", {})
    log_message(f"📩 툴 호출: {name} with args: {args}")
    if name == "check_commit_activity":
        return await check_commit_activity()
    elif name == "validate_commit_convention" and "message" in args:
        return await validate_commit_convention(args["message"])
    return {"error": f"도구 '{name}'를 처리할 수 없습니다."}

# ✅ MCP 서버 직접 stdio 처리 루프
# if __name__ == "__main__":
#     log_message("🔌 MCP 서버 시작 준비")
#     while True:
#         try:
#             line = sys.stdin.readline()
#             if not line:
#                 break
#             request = json.loads(line)
#             if "tool_call" in request:
#                 result = asyncio.run(mcp.handle(request["tool_call"]))
#         except Exception as e:
#             log_message(f"❌ 서버 처리 중 예외 발생: {e}")
if __name__ == "__main__":
    import asyncio
    result = asyncio.run(validate_commit_convention("feat: manual commit"))
    print("테스트 출력:", result)


# # server.py (MCP 기반 with 상세 로그)
# from mcp.server.fastmcp import FastMCP
# import subprocess
# import httpx
# import os
# import datetime
# from typing import List, Dict, Any
# from dotenv import load_dotenv

# HOST = "127.0.0.1"
# PORT = 3333
# mcp = FastMCP("commit-tools", host=HOST, port=PORT)

# load_dotenv()
# GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
# GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

# LOG_FILE = "mcp_commit_log.txt"

# def log_message(msg: str):
#     with open(LOG_FILE, "a", encoding="utf-8") as f:
#         f.write(f"[{datetime.datetime.now()}] {msg}\n")

# def is_valid_convention(message: str) -> bool:
#     valid_types = ["feat", "fix", "chore", "docs", "refactor", "test", "perf"]
#     if ": " not in message:
#         return False
#     type_part = message.split(":", 1)[0]
#     return type_part in valid_types

# def get_modified_files() -> list[str]:
#     changed = subprocess.check_output(["git", "diff", "--name-only"]).decode().splitlines()
#     untracked = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"]).decode().splitlines()
#     return changed + untracked

# @mcp.tool()
# async def validate_commit_convention(message: str) -> dict:
#     log_message("🚀 validate_commit_convention 호출됨")
#     log_message(f"메시지: {message}")
#     if not is_valid_convention(message):
#         log_message(f"[검사 실패] '{message}'")
#         return {"status": "invalid", "reason": "Conventional Commit 형식이 아님"}
#     try:
#         subprocess.run(["git", "add", "."], check=True)
#         subprocess.run(["git", "commit", "-m", message], check=True)
#         subprocess.run(["git", "push"], check=True)
#         log_message(f"✅ 커밋 & 푸시 완료됨: '{message}'")
#         return {"status": "success", "message": "커밋 및 푸시 완료됨"}
#     except subprocess.CalledProcessError as e:
#         log_message(f"❌ Git 명령 실패: {e}")
#         return {"status": "error", "error": str(e)}

# @mcp.tool()
# async def check_commit_activity() -> dict:
#     log_message("🔍 check_commit_activity 호출됨")
#     url = f"https://api.github.com/users/{GITHUB_USERNAME}/events"
#     headers = {
#         "Authorization": f"token {GITHUB_TOKEN}",
#         "Accept": "application/vnd.github.v3+json"
#     }
#     today = datetime.datetime.utcnow().date()
#     try:
#         response = httpx.get(url, headers=headers)
#         log_message("📡 GitHub API 호출 완료")
#         if response.status_code != 200:
#             return {"status": "error", "message": f"GitHub API 오류: {response.status_code}"}
#         events = response.json()
#         for event in events:
#             if event["type"] == "PushEvent":
#                 event_date = datetime.datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ").date()
#                 if event_date == today:
#                     return {"status": "done", "message": "오늘 커밋했습니다."}
#         suggestion = await suggest_commit_message_based_on_changes()
#         log_message("🧠 LLM 커밋 제안 요청 완료")
#         log_message(suggestion)
#         extracted = extract_first_commit_line(suggestion)
#         if extracted:
#             result = await validate_commit_convention(extracted)
#             return {
#                 "status": "committed",
#                 "suggested_message": extracted,
#                 "result": result
#             }
#         else:
#             log_message("❌ 커밋 메시지를 추출하지 못했습니다")
#             return {
#                 "status": "suggested_only",
#                 "message": "커밋 메시지를 추출하지 못했습니다.",
#                 "suggestion": suggestion
#             }
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# async def suggest_commit_message_based_on_changes() -> str:
#     log_message("🧠 LLM 커밋 제안 요청 시작")
#     changed_files = get_modified_files()
#     if not changed_files:
#         return "변경된 파일이 없습니다."
#     file_list_str = "\n".join(f"- {f}" for f in changed_files)
#     prompt = (
#         f"다음 파일들이 변경되었습니다:\n{file_list_str}\n"
#         "이 변경 사항을 기반으로 한 줄짜리 커밋 메시지를 하나만 제안해주세요. "
#         "형식은 반드시 다음을 따르세요: `feat: ...`, `fix: ...`, `refactor: ...` 등. "
#         "영어로, 소문자로 시작하며 콜론 뒤에 한 칸 띄고 메시지를 작성해주세요. "
#         "예시: `feat: add login validation`"
#     )
#     payload = {
#         "model": "mistral",
#         "prompt": prompt,
#         "tools": tool_schemas(),
#         "stream": False
#     }
#     try:
#         res = httpx.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=30)
#         tool_call = res.json()
#         log_message(f"🧠 모델 응답: {tool_call}")
#         if isinstance(tool_call, dict) and "name" in tool_call:
#             log_message(f"⚙️ LLM이 선택한 툴: {tool_call['name']} {tool_call.get('arguments', {})}")
#             return await dispatch_tool(tool_call)
#         return tool_call.get("response", "").strip()
#     except Exception as e:
#         return f"Ollama 호출 실패: {e}"

# def extract_first_commit_line(suggestion: str) -> str:
#     lines = suggestion.split("\n")
#     for line in lines:
#         line = line.strip("- •*` ")
#         if any(line.startswith(t) for t in ["feat:", "fix:", "chore:", "docs:", "refactor:", "test:", "perf:"]):
#             return line
#     return ""

# def tool_schemas() -> List[Dict[str, Any]]:
#     return [
#         {
#             "name": "check_commit_activity",
#             "description": "오늘 GitHub에 커밋했는지 확인",
#             "parameters": {"type": "object", "properties": {}}
#         },
#         {
#             "name": "validate_commit_convention",
#             "description": "커밋 메시지를 검사하고 통과하면 커밋 및 푸시",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "message": {"type": "string", "description": "검사할 커밋 메시지"}
#                 },
#                 "required": ["message"]
#             }
#         }
#     ]

# async def dispatch_tool(tool_call: Dict[str, Any]) -> str:
#     name = tool_call.get("name")
#     args = tool_call.get("arguments", {})
#     log_message(f"📩 툴 호출: {name} with args: {args}")
#     if name == "check_commit_activity":
#         return await check_commit_activity()
#     elif name == "validate_commit_convention" and "message" in args:
#         return await validate_commit_convention(args["message"])
#     return f"도구 '{name}'를 처리할 수 없습니다."

# if __name__ == "__main__":
#     try:
#         log_message("🔌 MCP 서버 시작 준비")
#         log_message(f"🌐 MCP 서버 주소: http://{HOST}:{PORT}")
#         mcp.run(transport='stdio')
#     except Exception as e:
#         log_message(f"❌ MCP 서버 실행 중 예외 발생: {e}")