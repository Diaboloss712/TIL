# mcp_client_stdio.py
import json
import subprocess
import datetime

LOG_FILE = "mcp_client_log.txt"
PYTHON_PATH = r"C:\Users\Dia\TIL\MCP\04_09\venv_client\Scripts\python.exe"

def log_message(msg: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")

def call_mcp_tool(tool_name: str, arguments: dict):
    request = {
        "tool_call": {
            "name": tool_name,
            "arguments": arguments
        }
    }

    try:
        proc = subprocess.Popen(
            # [PYTHON_PATH, "mcp_server.py"],
            [PYTHON_PATH, "mcp_test.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        log_message(f"📤 MCP 요청 전송: {tool_name} {arguments}")
        stdout, stderr = proc.communicate(json.dumps(request) + "\n", timeout=60)

        if stderr:
            log_message(f"🐛 서버 에러 출력:\n" + stderr.strip())

        lines = stdout.strip().splitlines()
        if not lines:
            log_message(f"❌ MCP 서버 응답이 비어 있음")
            return
        try:
            response = json.loads(lines[-1])
            log_message(f"\n✅ 최종 MCP 응답:\n", json.dumps(response, indent=2, ensure_ascii=False))
            log_message(f"✅ MCP 응답 성공: {response}")
        except json.JSONDecodeError as e:
            log_message(f"❌ 응답 파싱 실패: {e}")

    except subprocess.TimeoutExpired as e:
        log_message(f"❌ MCP 호출 Timeout: {e}")
    except Exception as e:
        log_message(f"❌ MCP 호출 실패: {e}")

if __name__ == "__main__":
    # ✅ 테스트: 커밋 메시지 검사
    call_mcp_tool("validate_commit_convention", {
        "message": "feat: implement commit automation"
    })

    # ✅ 또는 오늘 커밋 여부 확인
    # call_mcp_tool("check_commit_activity", {})


# import json
# import subprocess
# import datetime

# LOG_FILE = "mcp_client_log.txt"
# PYTHON_PATH = r"C:\Users\Dia\TIL\MCP\04_09\venv_client\Scripts\python.exe"

# def log_message(msg: str):
#     with open(LOG_FILE, "a", encoding="utf-8") as f:
#         f.write(f"[{datetime.datetime.now()}] {msg}\n")

# def call_mcp_tool(tool_name: str, arguments: dict):
#     request = {
#         "tool_call": {
#             "name": tool_name,
#             "arguments": arguments
#         }
#     }

#     try:
#         proc = subprocess.Popen(
#             [PYTHON_PATH, "mcp_server.py"],
#             stdin=subprocess.PIPE,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )

#         stdout, stderr = proc.communicate(json.dumps(request) + "\n", timeout=60)

#         try:
#             lines = stdout.strip().split("\n")
#             for line in lines:
#                 print("📤", line)
#             response = json.loads(lines[-1])
#             print("\n✅ MCP 응답:\n", json.dumps(response, indent=2, ensure_ascii=False))
#         except Exception as e:
#             log_message(f"❌ 응답 파싱 오류: {e}")
#             log_message(f"⛔ 원본 출력: {stdout}")
#             if stderr:
#                 log_message(f"🐛 에러 출력: {stderr}")

#     except subprocess.TimeoutExpired as e:
#         log_message(f"❌ MCP 클라이언트 실행 중 Timeout: {e}")
#     except Exception as e:
#         log_message(f"❌ MCP 클라이언트 실행 중 기타 예외: {e}")

# if __name__ == "__main__":
#     # ✅ 테스트: 커밋 메시지 검사
#     call_mcp_tool("validate_commit_convention", {
#         "message": "feat: implement commit automation"
#     })
