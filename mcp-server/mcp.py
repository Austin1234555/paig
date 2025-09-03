from typing import Any
import httpx
import yaml
from mcp.server.fastmcp import FastMCP

# ---------- Initialize FastMCP server ----------
mcp = FastMCP("paig-governance-service")

# ---------- Load Config ----------
with open("default_config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Fetch base URL dynamically from config
PAIG_BASE_URL = config.get("server", {}).get("url", "http://127.0.0.1:4545")


# ---------- Login Helper ----------
async def get_session_cookie() -> str | None:
    """Login to PAIG and return a valid session cookie automatically."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{PAIG_BASE_URL}/account-service/api/login",
                json={"username": "admin", "password": "welcome1"},
            )
            response.raise_for_status()
            return response.cookies.get("PRIVACERAPAIGSESSION")
        except Exception as e:
            print("❌ Login failed:", e)
            return None


# ---------- Helper Function ----------
async def make_paig_request(
    method: str,
    endpoint: str,
    cookies: dict[str, str] = None,
    data: dict = None,
    params: dict = None,
) -> dict[str, Any] | None:
    """Make a request to the PAIG Governance API with a session cookie automatically included."""
    cookie = await get_session_cookie()
    if not cookie:
        return {"error": "Login failed, no session cookie"}

    cookies = {"PRIVACERAPAIGSESSION": cookie}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method,
                f"{PAIG_BASE_URL}{endpoint}",
                cookies=cookies,
                json=data,
                params=params,
                timeout=30.0,
            )
            response.raise_for_status()
            return {"json": response.json() if response.text.strip() else {}}
        except Exception as e:
            return {"error": str(e)}


# ---------- MCP Tools for Applications ----------
@mcp.tool()
async def list_applications(page: int = 0, size: int = 10, status: str = None, name: str = None) -> str:
    """
    List AI applications with optional filters.
    Example queries:
    - "List applications"
    - "Show all AI applications"
    - "Get applications with status=1"
    """
    params = {"page": page, "size": size}
    if status:
        params["status"] = status
    if name:
        params["name"] = name

    result = await make_paig_request("GET", "/governance-service/api/ai/application", params=params)
    if "error" in result:
        return f"❌ Unable to fetch applications: {result['error']}"

    data = result["json"]
    if not data.get("content"):
        return "ℹ️ No applications found."

    apps = [f'App ID {idx}: {app}' for idx, app in enumerate(data["content"], start=1)]
    return "📂 Applications: " + "; ".join(apps)


@mcp.tool()
async def create_application(app_data: dict) -> str:
    """
    Create a new AI application.
    Example queries:
    - "Create application named FraudDetector"
    - "Add new app Austin"
    """
    result = await make_paig_request("POST", "/governance-service/api/ai/application", data=app_data)
    if "error" in result:
        return f"❌ Failed to create application: {result['error']}"
    return f'✅ Application "{app_data.get("name")}" created successfully.'


@mcp.tool()
async def update_application_guardrails(guardrail_data: dict) -> str:
    """
    Update application guardrails.
    Example queries:
    - "Update guardrails for application 42"
    - "Change guardrail settings"
    """
    result = await make_paig_request("PUT", "/governance-service/api/ai/application/guardrails", data=guardrail_data)
    if "error" in result:
        return f"❌ Unable to update guardrails: {result['error']}"
    return "✅ Application guardrails updated successfully."


@mcp.tool()
async def get_application_by_id(app_id: str) -> str:
    """
    Fetch an application by its ID.
    Example queries:
    - "Get application 42"
    - "Show me details of app 101"
    """
    result = await make_paig_request("GET", f"/governance-service/api/ai/application/{app_id}")
    if "error" in result:
        return f"❌ Unable to fetch application {app_id}: {result['error']}"

    data = result["json"]
    return f'📂 Application {data.get("id")}: {data.get("name")} - {data.get("description", "No description")}'


@mcp.tool()
async def update_application(app_id: str, app_data: dict) -> str:
    """
    Update an application by ID.
    Example queries:
    - "Update application 42"
    - "Modify app 101 with new description"
    """
    result = await make_paig_request("PUT", f"/governance-service/api/ai/application/{app_id}", data=app_data)
    if "error" in result:
        return f"❌ Unable to update application {app_id}: {result['error']}"
    return f"✅ Application {app_id} updated successfully."


@mcp.tool()
async def delete_application(app_id: str) -> str:
    """
    Delete an application by ID.
    Example queries:
    - "Delete application 42"
    - "Remove app 101"
    """
    result = await make_paig_request("DELETE", f"/governance-service/api/ai/application/{app_id}")
    if "error" in result:
        return f"❌ Unable to delete application {app_id}: {result['error']}"
    return f"🗑️ Application {app_id} deleted successfully."


# ---------- Run MCP ----------
if __name__ == "__main__":
    mcp.run(transport="stdio")
