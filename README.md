# MCP Web Discovery  🔍

*Instantly make any website discoverable by Model Context Protocol‑aware agents and LLM crawlers.*

---


## ✨ What is this?

Model Context Protocol (MCP) lets agents query rich, structured resources over
JSON‑RPC. **What’s missing is a way for the open web to *advertise* an MCP
endpoint**—so ChatGPT, Claude, Perplexity, or your own agent can find it
automatically.

This repo provides:

* **Two dead‑simple discovery methods**  
  1. **Well‑known JSON** – `/.well-known/mcp-metadata.json`  
  2. **HTML `<link rel="mcp-server">` tag** in any page header  
* **Reference middleware** for FastAPI, Express, and Cloudflare Workers  
* **Copy‑paste JSON examples** (minimal → fully‑featured)  
* MIT‑licensed code you can drop into any stack

<br>

---

<br>

## 0. Why you want this ⚡️

| Old Web Reality | AI‑Native Reality (with **mcpwd**) |
|-----------------|------------------------------------|
| **Google blue links ruled traffic.** | **Answer engines rule traffic.** Perplexity, ChatGPT, Claude, Cursor, etc. can *instantly* talk to your site via MCP. |
| Crawlers scrape walls of HTML, guess context, often get it wrong. | You expose **one clean vector endpoint**; AI pulls the exact chunks you curated—no guessing, no hallucination. |
| Traditional SEO is **necessary** but **not sufficient**. | Keep your meta tags, **add an MCP doorbell** so AI actually understands and cites you. |
| Users bounce after reading a snippet. | Users ask, AI answers, **your brand is the citation**—traffic that converts. |

> Google search isn’t dead, but the click‑through is.  
> Publish a single link (or JSON) and graduate from “random HTML blob” to
> **AI‑search optimized content hub**.

---
<br>

## 1. Installation

### Python (FastAPI)
`pip install mcpweb`


### JavaScript (Express / Node)
`npm install mcpweb`

<br> 

## 2. Quick Start

### 2.1 Framework integration

#### Next.js / Vercel (static export)
1. Drop your mcp-metadata.json into public/.well-known/.
2. Add the <link> tag to /app/_document.tsx.

#### WordPress
Use an “Insert Headers and Footers” plugin to paste the <link> tag; upload the
JSON via Media Library or your server.

```html
<link rel="mcp-server" href="https://api.yoursite.com/mcp">
```

<br>

### 2.2 FastAPI self‑host (public or private)

```python
from mcpweb.fastapi_middleware import create_mcp_app

app = create_mcp_app("mcp-metadata.json")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
```

### 2.3 Express (Node)

```javascript
const express = require('express');
const { mcpDiscovery } = require('mcpweb/express-middleware');
const app = express();

app.use(
  mcpDiscovery({
    metadataPath: 'mcp-metadata.json'   // same rules as Python
  })
);

app.listen(8080);
```

## 3. Discovery Mechanics for Crawlers

### 3.1 Primary path
```text
GET https://<origin>/.well-known/mcp-metadata.json
```
<i>Works for public and restricted endpoints.</i>

<br>

### 3.2 Fallback (header tag) – used only if JSON returns 404

```html
<link rel="mcp-server" href="https://api.example.com/mcp">
```
<i>Works for public endpoints.</i>

#### Crawlers MUST: load JSON first → inspect `access` → fetch token if "restricted".

<br>

## 4. JSON Schema & Examples

### 4.1 Required fields

| Key                     | Type                         | Required?                          | Description                                                  |
| ----------------------- | ---------------------------- | ---------------------------------- | ------------------------------------------------------------ |
| `name`                  | string                       | **Yes**                            | Human label |
| `version`               | string                       | **Yes**                            | MCP server version                |
| `mcp_server_url`        | string (HTTPS)               | **Yes**                            | Root endpoint for /messages, /sse, etc.         |
| `access`                | `"public"` \| `"restricted"` | No → defaults to `"public"`        | Indicates whether prior authorization is required            |
| `authorization_servers` | string array                 | **Yes if** `access = "restricted"` | One or more OIDC issuer URLs that can mint / validate tokens |


Unknown keys are ignored (prefix custom ones with x_).

<br>

### 4.2 Minimal (public)

```json
{
  "name": "Demo MCP Server",
  "version": "1.0.0",
  "mcp_server_url": "https://api.demo.com/mcp"
}
```

<br>

### 4.3 Maximal (restricted)

```json
{
  "name": "Acme Inc MCP",
  "version": "1.0.0",

  "mcp_server_url": "https://api.acme.com/mcp",
  "access": "restricted",
  "authorization_servers": ["https://login.acme.com"],

  "public_key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...",
  "contact": "ai-team@acme.com",
  "features": ["faq", "customer_profile"],
  "x_rate_limit_policy": "https://api.acme.com/policy"
}
```

<br>

## 5. Repo Layout

| Path                                 | Purpose                     |
| ------------------------------------ | --------------------------- |
| `python/mcpwd/fastapi_middleware.py` | Plug‑n‑play FastAPI helper  |
| `node/mcpwd/express-middleware.js`   | Same for Express            |
| `examples/minimal_site`              | Header‑only (public) demo   |
| `examples/maximal_site`              | JSON‑only (restricted) demo |

<br>

## 6. Contributing

PRs welcome! Follow [Conventional Commits](https://www.conventionalcommits.org/).

1. git clone & pnpm install && pip install -e .

2. Add tests (pytest, vitest) if you touch code.

3. Submit PR.

<br>

## 7. License
MIT — use it, fork it, ship it.

<br>

Questions? Open an issue or ping @John-Rood on GitHub.
<br>

Let’s make the open web AI‑discoverable by default. 🚀
