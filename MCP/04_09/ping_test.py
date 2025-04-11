from mcp.server.fastmcp import FastMCP

mcp = FastMCP("test-server", port=5055)

@mcp.tool()
def ping() -> str:
    return "pong"

if __name__ == "__main__":
    print("🟢 MCP 서버 시작됨 (ping 테스트)")
    mcp.run()