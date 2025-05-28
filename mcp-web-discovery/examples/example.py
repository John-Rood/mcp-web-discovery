from mcpweb.fastapi_middleware import create_mcp_app

app = create_mcp_app("./maximal_site/public/.well-known/mcp-metadata.json")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)

# visit http://localhost:8000/.well-known/mcp-metadata.json in your browser to verify