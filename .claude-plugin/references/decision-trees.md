# Decision Trees

**Usage:** Reference these flowcharts when making routine decisions during development. Each tree includes an explicit fallback to human judgment for edge cases not covered by the branches.

---

## Tree 1: Which test type should I write?

```mermaid
flowchart TD
    A[Start: Which test type should I write?] --> B{Is it pure business logic, no I/O?}
    B -- Yes --> UT[Unit Test<br/>bun test]
    B -- No --> C{Is it port - adapter wiring, component interaction?}
    C -- Yes --> IT[Integration Test<br/>bun test + fake adapter]
    C -- No --> E{Is it a critical cross-layer user journey?}
    E -- Yes --> E2E[E2E Test<br/>playwright]
    E -- No --> F{Is it a property always true regardless of input?}
    F -- Yes --> INV[Invariant Test<br/>bun test]
    F -- No --> G{Is it a rule across many random inputs?}
    G -- Yes --> PBT[Property-Based Test<br/>fast-check + bun test]
    G -- No --> H{Is it verifying layer dependency rules?}
    H -- Yes --> AT[Architecture Test<br/>ts-arch]
    H -- No --> I{Is this a regression test — one test per bug, kept forever?}
    I -- Yes --> RT[Regression Test<br/>bun test — regression/ directory]
    I -- No --> Z[None of the above — route to HUMAN DECISION]
    UT --> Z
    IT --> Z
    E2E --> Z
    INV --> Z
    PBT --> Z
    AT --> Z
    RT --> Z
```

**Summary:** Business logic -> Unit. Wiring -> Integration. Critical journeys -> E2E. Invariants -> Invariant test. Random-input rules -> Property-based. Layer rules -> Architecture test. Bug fix regression -> Regression test. Anything else -> human.

---

## Tree 2: Fake adapter, MSW, or real?

```mermaid
flowchart TD
    A[Start: Fake adapter, MSW, or real?] --> B{Port interface exists?}
    B -- No port exists --> C{HTTP API with no domain logic?}
    C -- Yes --> D{Fake adapter exists?}
    D -- Yes --> FA_E[Use existing fake adapter]
    D -- No --> MSW[MSW handler<br/>LAST RESORT only]
    C -- No domain logic --> E[Create port composable FIRST<br/>Then fake -> then real]
    B -- Yes --> F{Fake adapter exists?}
    F -- Yes --> FA[Use existing fake adapter]
    F -- No --> G[Create fake adapter FIRST<br/>HARD-GATE: must complete before proceeding]
    G --> H[Wire and verify fake works]
    H --> I[Then use REAL adapter only after fake walks]
    E --> Z[None of the above — route to HUMAN DECISION]
    FA_E --> Z
    MSW --> Z
    FA --> Z
    G --> Z
    H --> Z
    I --> Z
    J[Unusual case detected:<br/>file system, WebSocket, CLI,<br/>non-HTTP protocol] --> Z
```

**Note:** Fallback for unusual cases: If the dependency doesn't fit any branch above — e.g., a file system, CLI tool, WebSocket, or non-HTTP protocol — do NOT force it into the tree. Route directly to a human decision.

**Summary:** Port exists + fake exists -> fake. Port exists + no fake -> create fake first (hard gate), wire, verify, then real only after fake passes. No port + HTTP + no domain logic -> fake if exists, otherwise MSW (last resort). No port + no domain -> create port first. Any unusual case -> human immediately.

---

## Tree 3: ADR or decision journal entry?

```mermaid
flowchart TD
    A[Start: ADR or decision journal?] --> B{Is it a significant architecture choice?<br/>tech stack, layer layout, architecture pattern}
    B -- Yes, with real trade-offs --> ADR[Write ADR]
    B -- Yes, but no trade-offs identified --> ADR_S[Write ADR<br/>still document for visibility]
    B -- No, not architectural --> C{Is it a process or workflow decision?}
    C -- Yes --> DJ[Decision journal entry]
    C -- No --> TRIV[Trivial — no documentation needed]
    ADR --> Z[None of the above — route to HUMAN DECISION]
    ADR_S --> Z
    DJ --> Z
    TRIV --> Z
```

**Summary:** Architectural with trade-offs -> ADR. Architectural without trade-offs -> still ADR. Process/workflow -> decision journal. Trivial -> skip. Anything else -> human.

---

## Tree 4: Task scope — atomic or split?

```mermaid
flowchart TD
    A[Start: Task scope — atomic or split?] --> B{How many files are involved?}
    B -- 1 file --> ATOMIC[One atomic task]
    B -- 2 to 5 files, same layer --> ATOMIC2[One task]
    B -- 2 to 5 files, different layers --> SPLIT[Split into 2 tasks<br/>one per layer boundary]
    B -- Many files across layers --> ELPHANT[Split by layer boundary<br/>elephant carpaccio]
    B -- Still unclear --> Z[None of the above — route to HUMAN DECISION]
    ATOMIC --> Z
    ATOMIC2 --> Z
    SPLIT --> Z
    ELPHANT --> Z
```

**Summary:** 1 file -> atomic. 2-5 files same layer -> one task. 2-5 files different layers -> split by layer. Many files across layers -> split by layer (carpaccio). Unclear -> human.

---

## Tree 5: Phase skip or run?

```mermaid
flowchart TD
    A[Start: Phase skip or run?] --> B{What is complexityTier from state.json?}

    B -- simple / Tier 1 --> C{Which phase?}
    C -- Phase 4 or 7 --> SKIP_T1[SKIP<br/>substitute lightweight alternative]
    C -- Phase 5 --> REPLACE_T1[REPLACE with lightweight task list<br/>Phase 5 still runs, reduced scope]
    C -- Phase 5b --> RUN_T1_5b[RUN — Phase 5b is a HARD-GATE<br/>and cannot be skipped]
    C -- Phase 1, 2, 3, 6, or 8 --> RUN_T1[RUN full process]

    B -- moderate / Tier 2 --> RUN_T2[RUN full process<br/>all phases — no skips]

    B -- complex / Tier 3 --> D{Which phase?}
    D -- Phase 4 --> RUN_ARCH[RUN + expanded risk analysis<br/>with failure mode annotations]
    D -- Phase 7 --> RUN_CQRS[RUN + full regression suite<br/>+ CQRS + arch compliance checks]
    D -- Phase 1, 2, 3, 5, 5b, 6, or 8 --> RUN_T3[RUN full process<br/>with Tier 3 enhancements]

    SKIP_T1 --> Z[None of the above — route to HUMAN DECISION]
    RUN_T1 --> Z
    RUN_T1_5b --> Z
    REPLACE_T1 --> Z
    RUN_T2 --> Z
    RUN_ARCH --> Z
    RUN_CQRS --> Z
    RUN_T3 --> Z
```

**Summary:**
- **Tier 1 (simple)**: Phase 4 or 7 → skip (lightweight alternative). Phase 5 → replace with lightweight task list (still runs). Phase 5b → always run (HARD-GATE). Tier 1 phases 1, 2, 3, 6, 8 → run.
- **Tier 2 (moderate)**: all phases run — no skips.
- **Tier 3 (complex)**: Phase 4 → run + expanded risk analysis. Phase 7 → run + full regression suite + CQRS + architecture compliance. All other phases → run with enhancements. Any mismatch → human decision.

---

*Last updated: 2026-03-28*
