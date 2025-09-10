import requests


url = "http://localhost:8000/mcp"

headers= {
    "Content-Type": "application/json",
    "Accept": "application/json,text/event-stream"
}


body = {
    "jsonrpc":"2.0",
    "method" :"tools/call",
    "params" :{
        "cursor": "null" ,
        "name": "calculator",
        "arguments":{
            "expression" :"3 * 2"
        }
    },
    "id" :  3
}
response = requests.post(url,headers=headers ,json=body)
# Final response
print(response.text)