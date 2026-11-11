import asyncio
import json
from pathlib import Path
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def main():
    async with streamable_http_client("http://127.0.0.1:8765/mcp") as (reader,writer):
        async with ClientSession(reader,writer) as session:
            await session.initialize()
            tools=(await session.list_tools()).tools
            print("YOUTUBE_MCP_CANARY_HTTP_TOOLS",len(tools),flush=True)
            print("TOOLS_START",",".join(sorted(x.name for x in tools)[:6]),flush=True)
            expected=json.loads(Path("/contract/contract-tools.json").read_text())
            data={x.name:x.input_schema for x in tools}
            assert len(expected)==97
            assert set(data).issuperset(expected), "Lost YouTube MCP tools"
            def norm(v):
                if isinstance(v,list):return [norm(x) for x in v]
                if isinstance(v,dict):return {k:norm(x) for k,x in v.items() if not(k=="required" and x==[])}
                return v
            changed=[k for k in expected if norm(data[k])!=norm(expected[k])]
            assert not changed, f"Changed input contracts: {changed[:12]}"
            print("YOUTUBE_MCP_HTTP_COMPATIBLE_TOOLS_PASS",len(data))
asyncio.run(main())
