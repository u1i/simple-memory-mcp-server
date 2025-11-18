import asyncio
import sys

# 1. SETUP IMPORTS
try:
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client
except ImportError:
    print("❌ Error: 'mcp' library not found.")
    sys.exit(1)

# CONFIGURATION
SERVER_URL = "http://localhost:8088/mcp"

async def run_full_discovery():
    print(f"--- Connecting to {SERVER_URL} ---")

    try:
        # Connect using the official client
        async with streamablehttp_client(SERVER_URL) as transport:
            
            # Tuple Unpacking Fix (Handles the 3-value return issue)
            if isinstance(transport, tuple):
                if len(transport) >= 2:
                    read, write = transport[0], transport[1]
                else:
                    print(f"❌ Unexpected tuple length: {len(transport)}")
                    return
            else:
                print(f"❌ Unexpected transport type: {type(transport)}")
                return

            print("✅ Connection Valid. Fetching full details...")
            
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.list_tools()
                
                print(f"\n🎉 SUCCESS! Found {len(result.tools)} tools. Full details below:\n")
                print("="*60)
                
                for tool in result.tools:
                    print(f"🔹 TOOL NAME: {tool.name}")
                    print("-" * 20)
                    
                    # PRINT THE FULL DESCRIPTION
                    desc = tool.description if tool.description else "[No description]"
                    print(desc)
                    
                    print("\n" + "="*60)

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        if hasattr(e, 'exceptions'):
            print(f"   Sub-errors: {e.exceptions}")

if __name__ == "__main__":
    asyncio.run(run_full_discovery())
