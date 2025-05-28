// npm install mcpweb     
// node example.js
// Then visit: http://localhost:8000/.well-known/mcp-metadata.json

const express = require('express');
const path = require('path');

const { mcpDiscovery } = require('mcpweb');

const app = express();

// path to your JSON
const metadataFile = path.join(
  __dirname,
  './maximal_site/public/.well-known/mcp-metadata.json'
);

// Mount the discovery middleware.
//  • Serves /.well-known/mcp-metadata.json
//  • Adds the <link rel="mcp-server"> response header automatically
app.use(
  mcpDiscovery({
    metadataPath: metadataFile
  })
);

// (Optional) other routes
app.get('/', (_, res) => {
  res.send('Hello—MCP discovery is live!');
});

app.listen(8000, () => {
  console.log('Server running on http://localhost:8000');
  console.log('Check: http://localhost:8000/.well-known/mcp-metadata.json');
});
