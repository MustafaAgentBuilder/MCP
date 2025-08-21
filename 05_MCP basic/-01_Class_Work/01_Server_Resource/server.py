from mcp.server.fastmcp import FastMCP


mcp = FastMCP(name="Server Resource MCP" , stateless_http=True)

docs = {
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.resource(
    "docs://documents",
    mime_type="application/json",
    name="list_docs",
    description="List all available documents with their names and descriptions",
#     annotations={
#         "audience": ["user", "assistant"],  # Both can access
#         "priority": 0.8
#     }
 )
def list_docs() -> list[str]:
    return list(docs.keys())


user_data = {
    "user_1": {"name": "Mustafa", "age": 18, "city": "Sialkot"},
    "user_2": {"name": "Ali", "age": 22, "city": "Karachi"},
    "user_3": {"name": "Ayesha", "age": 25, "city": "Islamabad"}
}

# Template resource that takes a user_id as input and fetches data
@mcp.resource(
    "user://get_user_info/{user_id}",
    mime_type="text/plain",
    name="get_user_info",
    description="Get user details like name, age, and city by user ID"
)
def get_user_info(user_id: str) -> str:
    # Try to get user data
    user = user_data.get(user_id)

    if user:
        return f"👤 Name: {user['name']}, Age: {user['age']}, City: {user['city']}"
    else:
        return "❌ User not found. Please check the ID."

app = mcp.streamable_http_app()