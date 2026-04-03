# Project Setup Steps

These steps are run once when starting a new project with this stack.
Phase 0 of devloop will walk through these if no project preferences exist yet.

## 0. Initialize Git Repository
```bash
git init
```
Dev-flow requires a git repository. Do this before any other setup steps.

## 1. Scaffold Nuxt project
```bash
bunx nuxi@latest init {project-name} --force
cd {project-name}
```

## 1.5 Create .gitignore and .env.example
```bash
# .gitignore
cat > .gitignore << 'EOF'
node_modules/
.output/
.data/
.nuxt/
.env
*.local
EOF

# .env.example (reference vars from setup and MCP config)
cat > .env.example << 'EOF'
INSTFORGE_URL=https://api.insforge.dev
INSTFORGE_API_KEY=your_api_key_here
NUXT_PUBLIC_APP_URL=http://localhost:3000
EOF
```

## 2. Install dependencies
```bash
bun install
```

## 3. Install Pinia
```bash
bun add @pinia/nuxt
```
Add to nuxt.config.ts modules: `['@pinia/nuxt']`

## 4. Configure Nuxt Layers
In nuxt.config.ts:
```typescript
export default defineNuxtConfig({
  extends: [
    './layers/core',
    // add domain layers here as you create them
  ]
})
```

## 5. Scaffold first domain layer
```bash
mkdir -p layers/{domain}/{components,composables,ports,pages,server/api,stores}
mkdir -p layers/{domain}/adapters             ← fake + real adapters
mkdir -p layers/{domain}/types                ← domain types
mkdir -p layers/{domain}/tests/{unit,properties,regression}
touch layers/{domain}/index.ts                ← public API (re-export public items)
touch layers/{domain}/nuxt.config.ts
# Project-root test directories (shared across layers)
mkdir -p tests/e2e
```

## 6. Wire up Insforge MCP
In `.claude/settings.json` (or Claude Code MCP settings):
```json
{
  "mcpServers": {
    "insforge": {
      "command": "bun",
      "args": ["x", "@insforge/mcp"]
    }
  }
}
```
Verify the MCP is active before proceeding.

## 7. Install dev dependencies
```bash
bun add zod
bun add -d playwright msw fast-check
bunx playwright install
```

## 8. Add test scripts to package.json
```json
{
  "scripts": {
    "test": "bun test",
    "test:coverage": "bun test --coverage",
    "test:e2e": "playwright test",
    "test:watch": "bun test --watch"
  }
}
```

## 9. Verify green baseline
```bash
bun test
```
Expected: no failures (no tests yet = green baseline). If this fails, stop and fix before any feature work.

## 10. Create first fake adapter (required before any real adapter)

Before adding any real adapter, create the fake adapter:

```bash
# For your first domain, create:
touch layers/{domain}/ports/{Domain}Port.ts
touch layers/{domain}/adapters/Fake{Domain}Adapter.ts
```

Then register in the composition root:
```typescript
// app/diComposition.ts
import { Fake{Domain}Adapter } from 'layers/{domain}/adapters/Fake{Domain}Adapter'
export const {domain}Adapter = new Fake{Domain}Adapter()
```

Verify the skeleton walks before adding any real adapter.
See PRINCIPLES.md → Fake Adapters First (non-negotiable).
