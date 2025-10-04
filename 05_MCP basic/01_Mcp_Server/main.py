"""
MCP server:
Testing Your Resources
You can test resources using the MCP Inspector. Start your server with:

        `uv run mcp dev mcp_server.py`
"""

from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


# ✅ Tool: Read a document
@mcp.tool(
        name="read_doc",
        description="Read the contents of a document by ID"
        )
def read_doc(doc_id: str) -> str:
    return docs.get(doc_id, "Document not found.")

# ✅ Tool: Edit a document
@mcp.tool(
        name="edit_doc",
        description="Edit the contents of a document"
        )
def edit_doc(doc_id: str, new_content: str) -> str:
    if doc_id in docs:
        docs[doc_id] = new_content
        return f"Document '{doc_id}' updated successfully."
    return "Document not found."

# ✅ Resource: Return all doc IDs
@mcp.resource(
        "docs://documents",
        mime_type="application/json"
    )
def list_doc_ids() -> list[str]:
    return list(docs.keys())

# ✅ Resource: Return contents of a particular doc
@mcp.resource(
        "docs://documents",
        mime_type="application/json"
        )
def get_doc_content(doc_id: str) -> str:
    return docs.get(doc_id, "Document not found.")

# ✅ Prompt: Rewrite a doc in markdown format
@mcp.prompt(
        name="rewrite_markdown",
        description="Rewrite given text into markdown format"
        )
def rewrite_markdown(doc_text: str) -> str:
    return f"# Markdown Version\n\n{doc_text}"

# ✅ Prompt: Summarize a doc
@mcp.prompt(
        name="summarize_doc",
        description="Summarize the document"
        )
def summarize_doc(doc_text: str) -> str:
    return f"Summary: {doc_text[:50]}..." if len(doc_text) > 50 else f"Summary: {doc_text}"

# if __name__ == "__main__":
#     mcp.run(transport="stdio")


# "I ran it this way because it was giving me a 'missing session ID' error."
app = FastAPI()
app.mount("/mcp", mcp.streamable_http_app())