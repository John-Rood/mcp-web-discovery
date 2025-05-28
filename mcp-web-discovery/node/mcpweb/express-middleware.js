/*
 * Express middleware for MCP Web Discovery (package: mcpwd)
 * ---------------------------------------------------------
 * • Always serves /.well-known/mcp-metadata.json
 * • Injects <Link rel="mcp-server"> header when access==="public"
 */

const fs = require("fs");
const path = require("path");

function loadMeta(metadataPath = "mcp-metadata.json") {
  const full = path.resolve(metadataPath);
  if (!fs.existsSync(full)) {
    throw new Error(`MCP metadata file not found at ${full}`);
  }
  return JSON.parse(fs.readFileSync(full, "utf8"));
}

function mcpDiscovery({ metadataPath = "mcp-metadata.json" } = {}) {
  const meta = loadMeta(metadataPath);
  const isPublic = (meta.access || "public") !== "restricted";

  return function (req, res, next) {
    // Well‑known JSON
    if (req.path === "/.well-known/mcp-metadata.json") {
      res.type("application/json").send(meta);
      return;
    }

    // Header injection (public only)
    if (isPublic) {
      res.set("Link", `<${meta.mcp_server_url}>; rel="mcp-server"`);
    }
    next();
  };
}

module.exports = { mcpDiscovery };
