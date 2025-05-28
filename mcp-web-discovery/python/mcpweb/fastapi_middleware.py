"""
FastAPI plug‑in for MCP Web Discovery (package: mcpwd)
-----------------------------------------------------

• Always serves /.well-known/mcp-metadata.json
• Injects   <Link rel="mcp-server">  header **only** when access=="public"
• Exports:
    - mount_mcp_discovery(app, metadata_path="mcp-metadata.json")
    - create_mcp_app(metadata_path="mcp-metadata.json")
"""

import json
import pathlib
from typing import Union

from fastapi import FastAPI, Request, Response


def _load_meta(path: Union[str, pathlib.Path]) -> dict:
    meta_file = pathlib.Path(path)
    if not meta_file.exists():
        raise FileNotFoundError(f"MCP metadata file not found: {meta_file}")
    return json.loads(meta_file.read_text())


def mount_mcp_discovery(app: FastAPI, metadata_path: str = "mcp-metadata.json"):
    meta = _load_meta(metadata_path)
    is_public = meta.get("access", "public") != "restricted"

    # --- well‑known JSON -----------------------------------------------------
    @app.get("/.well-known/mcp-metadata.json", include_in_schema=False)
    async def _mcp_metadata():
        return Response(json.dumps(meta), media_type="application/json")

    # --- header injection for public servers --------------------------------
    if is_public:

        @app.middleware("http")
        async def _inject_link_header(request: Request, call_next):
            resp = await call_next(request)
            resp.headers.add("Link", f'<{meta["mcp_server_url"]}>; rel="mcp-server"')
            return resp


def create_mcp_app(metadata_path: str = "mcp-metadata.json") -> FastAPI:
    """
    Convenience wrapper: returns a standalone FastAPI app that is MCP‑discoverable.
    """
    _app = FastAPI()
    mount_mcp_discovery(_app, metadata_path)
    return _app
