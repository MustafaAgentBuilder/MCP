import requests
import json

# MCP Client for Stateful Servers (stateless=False)
# When the server maintains session state, we need to:
# 1. Extract session ID from initialization response
# 2. Include session ID in all subsequent requests

def run_mcp_with_session():
    """
    This code is used when MCP server is configured with Stateful=True (stateless=False)
    It handles session management by:
    1. Getting session ID from server during initialization
    2. Using that session ID in all subsequent requests
    """
    
    base_url = "http://127.0.0.1:8000/mcp"
    
    # Initial headers for stateful connection (no session ID yet)
    # Session ID will be provided by server after initialization
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json,text/event-stream"
    }
    
    # Step 1: Initialize and get session ID
    lifecycle_start = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "roots": {
                    "listChanged": True
                },
                "sampling": {},
                "elicitation": {}
            },
            "clientInfo": {
                "name": "ExampleClient",
                "title": "Example Client Display Name",
                "version": "1.0.0"
            }
        }
    }
    
    print("--- STEP 1: INITIALIZE ---")
    # print(f"Sending: {json.dumps(lifecycle_start, indent=2)}")
    
    try:
        response = requests.post(
            url=base_url,
            headers=headers,
            json=lifecycle_start,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        # IMPORTANT: Extract session ID from response headers for stateful connection
        # Server returns 'mcp-session-id' header that must be used in all future requests
        session_id = response.headers.get('mcp-session-id')
        print(f"Session ID received: {session_id}")
        
        if not session_id:
            print("ERROR: No session ID received from server!")
            return
        
        # Update headers with session ID for all subsequent requests
        # This is required for stateful MCP servers (stateless=False)
        headers["mcp-session-id"] = session_id
        
        print(f"Response: {response.text}")
        
    except requests.exceptions.RequestException as e:
        print(f"Initialize request failed: {e}")
        return
    
    # Step 2: Send initialized notification with session ID
    initialized = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }
    
    print("\n--- STEP 2: INITIALIZED NOTIFICATION ---")
    print(f"Using Session ID: {session_id}")
    print(f"Sending: {json.dumps(initialized, indent=2)}")
    
    try:
        response = requests.post(
            url=base_url,
            headers=headers,
            json=initialized,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code not in [200, 202]:
            print("ERROR: Initialized notification failed!")
            return
        else:
            print("SUCCESS: Initialized notification accepted!")
            
    except requests.exceptions.RequestException as e:
        print(f"Initialized request failed: {e}")
        return
    
    # Step 3: List prompts with session ID
    body = {
        "jsonrpc": "2.0",
        "method": "prompts/list",
        "id": 9,
        "params": {}
    }
    
    print("\n--- STEP 3: LIST PROMPTS ---")
    print(f"Using Session ID: {session_id}")
    print(f"Sending: {json.dumps(body, indent=2)}")
    
    try:
        response = requests.post(
            url=base_url,
            headers=headers,
            json=body,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("SUCCESS: All MCP lifecycle steps completed!")
        else:
            print("ERROR: List prompts failed!")
            
    except requests.exceptions.RequestException as e:
        print(f"List prompts request failed: {e}")

if __name__ == "__main__":
    # Run MCP client for stateful server configuration
    run_mcp_with_session()