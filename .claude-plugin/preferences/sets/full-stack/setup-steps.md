# Project Setup Steps

These steps are run once when starting a new project with this stack.
Phase 0 of dev-flow will walk through these if no project preferences exist yet.

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

## 1.6 Install Nuxt UI and Google Fonts

```bash
cd {project-name}
bun add @nuxt/ui @nuxtjs/google-fonts nuxt-icon
```

## 1.7 Configure Nuxt UI Theme

Add to `nuxt.config.ts` inside `defineNuxtConfig`:

```typescript
export default defineNuxtConfig({
  modules: ['@nuxt/ui', '@nuxtjs/google-fonts', 'nuxt-icon'],
  googleFonts: {
    families: {
      'DM+Sans': [400, 500, 600, 700],
      'Fraunces': [400, 700],
    },
  },
  ui: {
    theme: {
      colors: {
        primary: { 50: '#fffbeb', 100: '#fef3c7', 500: '#f59e0b', 900: '#78350f' },
      },
      font: { sans: "'DM Sans', sans-serif", heading: "'Fraunces', serif" },
    }
  }
})
```

## 1.8 Create Custom CSS Variables

Create `assets/css/main.css`:

```css
/* Custom spacing scale (4pt base) */
:root {
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-6: 1.5rem;   /* 24px */
  --space-8: 2rem;     /* 32px */
  --space-12: 3rem;    /* 48px */
  --space-16: 4rem;    /* 64px */
}

/* Motion easing tokens */
:root {
  --ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);
  --ease-out-quint: cubic-bezier(0.22, 1, 0.36, 1);
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in: cubic-bezier(0.7, 0, 0.84, 0);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
}
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
```
