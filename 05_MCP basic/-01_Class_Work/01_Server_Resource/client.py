import requests
import uuid

url = "http://localhost:8000/mcp/"

# Generate a unique session ID
# session_id = str(uuid.uuid4())

headers = {
    "Accept": "application/json,text/event-stream",
    # "X-Session-ID": session_id  # Add session ID to headers
}

body = {
    "jsonrpc": "2.0",
    "method": "resources/list",
    "id": 1,
    "params": {
        "cursor": None,
        "uri": "user://get_user_info/user_1",
    },
}
# Responce

response = requests.post(url, json=body, headers=headers)
print(response.text)