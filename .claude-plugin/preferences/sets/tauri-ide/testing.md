# Testing Strategy

## Test Types

### Rust Unit Tests (cargo test)
Test core services in isolation. Mock the file system and PTY where needed.
Location: src-tauri/tests/*.rs

### Frontend Unit Tests (Vitest)
Test the plugin registry, file association resolution, and context reducers.
Location: src/**/*.test.ts
Location: src/plugin-api/__tests__/registry.test.ts

### Component Tests (Vitest + React Testing Library)
Test shell components and plugin API hooks.
Mock Tauri invoke with vi.mock('@tauri-apps/api/core').

### E2E Tests (WebdriverIO)
Smoke tests on compiled app: launch, open folder, edit file, terminal, command palette.
Location: e2e/specs/*.spec.ts

## Coverage Thresholds
- Rust core services: 80% line coverage via cargo test
- Plugin registry logic: 90% line coverage
- Shell components: integration test coverage (no specific %)
- E2E: 5 critical paths minimum
