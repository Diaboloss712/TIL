import httpx

MCP_URL = "http://localhost:3333"  # FastAPI 서버 포트 확인

def check_commit_today():
    try:
        response = httpx.get(f"{MCP_URL}/check-activity", timeout=15)
        print("🟢 응답:", response.json())
    except Exception as e:
        print("❌ 호출 실패:", e)

if __name__ == "__main__":
    check_commit_today()
