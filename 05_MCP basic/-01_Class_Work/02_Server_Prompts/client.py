import requests

url = "http://localhost:8000/mcp"

payload = {
    "jsonrpc":"2.0",
    "method":"prompts/get",
    "params":{
        "cursor":None,
        "name" : "create_lesson_plan",
        "arguments": {
            "subject": "Maths",
            "grade_level":"11 grade",
            "duration": "35 mins"
        }

    },
    "id":3  
}

# Reqauest headers
headers= {
    "Content-Type":"application/json",
    "Accept":"application/json,text/event-stream"
    
}

response = requests.post(url,headers=headers,json=payload,stream=True)
print(response)
for line in response.iter_lines():
    if line:
       print(line.decode("utf-8"))