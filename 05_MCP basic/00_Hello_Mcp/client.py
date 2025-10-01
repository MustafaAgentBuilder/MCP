# we can Call with in python Code and Postman
# import requests

# url = "http://127.0.0.1:8000/mcp/"    # trailing slash is important

# headers = {
#     # "Content-Type": "application/json" 
#     "Accept": "application/json,text/event-stream"
# }

# # In thos Body we say show all tools in MCP\server 

# body = {
#     "jsonrpc": "2.0",
#     "method": "tools/list",          # matches @mcp.tool() name
#     "id": 1,
#     "params": {}
# }

# response = requests.post(url, headers=headers, json=body)

# # for line in response.iter_lines():
# #     if line:
# #         print(line)

# print(response.text)



# # Here we see who can we call The Tool in Our and MCP server

# url = "http://127.0.0.1:8000/mcp/"    # trailing slash is important

# headers = {
#     "Accept": "application/json,text/event-stream"
# }

# body ={
#   "id": 34,
#   "jsonrpc": "2.0",
#   "method": "tools/call",
#   "params": {
#     "name": "Get weather",
#     "argument": {
#       "city": "Sialkot"
#     }
#   }
# }


# response = requests.post(url, headers=headers, json=body)
# print(response.text)
















