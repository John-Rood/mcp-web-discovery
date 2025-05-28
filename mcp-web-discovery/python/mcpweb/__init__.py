"""
mcpwd  •  MCP Web Discovery middleware (FastAPI version)
"""

from .fastapi_middleware import mount_mcp_discovery, create_mcp_app

__all__ = ["mount_mcp_discovery", "create_mcp_app"]

__version__ = "0.1.0"
