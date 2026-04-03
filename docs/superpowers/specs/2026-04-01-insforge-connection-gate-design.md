# Insforge Connection Gate — Design

## Context

Phase 5b pre-implementation gate verifies the project is ready to begin real adapter implementation. One gap in the current gate: it does not verify that the Insforge connection configuration exists before Phase 6 starts wiring real adapters.

The Insforge integration requires three things: a connection script, a base URL, and an API key. All three should be verified at the gate — not discovered mid-implementation.

## Gate Items (Phase 5b)

Add to the Phase 5b gate checklist:

```
- [ ] Insforge connection script exists and is wired in DI composition
- [ ] Base URL configured in .env (INSFORGE_BASE_URL)
- [ ] API key configured in .env (INSFORGE_API_KEY)
```

All three must pass for the gate to clear.
