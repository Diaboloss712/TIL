import httpx
import json

MCP_URL = "http://localhost:8000"

def send_message_to_mcp(prompt: str):
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "tools": [
            {
                "name": "check_commit_activity",
                "description": "오늘 GitHub에 커밋했는지 확인",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "validate_commit_convention",
                "description": "커밋 메시지를 검사하고 통과하면 커밋 및 푸시",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "검사할 커밋 메시지"
                        }
                    },
                    "required": ["message"]
                }
            }
        ],
        "stream": False
    }

    try:
        res = httpx.post(f"{MCP_URL}/api/generate", json=payload, timeout=30)
        result = res.json()
        print("✅ 응답:\n", json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print("❌ 요청 실패:", e)

if __name__ == "__main__":
    user_prompt = (
        "오늘 커밋을 안 했던 것 같아. 확인해주고, 변경 사항이 있다면 "
        "적절한 커밋 메시지를 작성해서 커밋까지 해줘."
    )
    send_message_to_mcp(user_prompt)
