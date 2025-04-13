# mcp_server_test.py
import sys
import json
import subprocess
import datetime

def is_valid_convention(message: str) -> bool:
    return message.startswith(("feat:", "fix:", "chore:", "docs:", "refactor:", "test:", "perf:"))

def validate_commit_convention(message: str):
    if not is_valid_convention(message):
        return {"status": "invalid", "reason": "형식 오류"}

    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        return {"status": "success", "message": "커밋 완료"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    raw = sys.stdin.readline()
    try:
        data = json.loads(raw)
        tool = data.get("tool_call", {})
        name = tool.get("name")
        args = tool.get("arguments", {})

        if name == "validate_commit_convention":
            result = validate_commit_convention(args.get("message", ""))
            print(json.dumps(result), flush=True)
        else:
            print(json.dumps({"status": "error", "message": "Unknown tool"}), flush=True)
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), flush=True)
