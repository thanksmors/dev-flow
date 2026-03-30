# Architecture Anti-Patterns

Anti-patterns related to module structure, dependency management, and architectural documentation.

---

## Circular Dependencies

**What it is:** Module A imports module B, and module B imports module A — directly or through a chain. The dependency graph contains a cycle.

**Why it looks right:** A depends on B because it needs B's functionality. B depends on A because it needs A's functionality. This feels symmetric and balanced. When you model the problem domain, A and B genuinely seem to need each other.

**The actual problem:** Neither module can be loaded independently. The initialization order becomes fragile — module A might not be fully initialized when B tries to use it. Refactoring is dangerous because changes in one module can silently break the other. Tree-shaking fails. Testing requires loading the entire cycle or using complex mocking. The codebase becomes impossible to reason about locally.

**Likelihood in autonomous context:** Medium-High

**How to detect it:**
- `tsc --noEmit` reports circular dependency errors
- Importing one module implicitly brings 10 others into scope
- `vitest` warnings about "circular dependency detected" appear in test output
- A small change in one file requires changes in a "sister" file to avoid test failures

**The fix:** Introduce a shared abstraction (interface or third module) that both can depend on, or invert one dependency through dependency injection.

---

## Tight Coupling

**What it is:** Modules share too much knowledge — they know each other's internals, depend on specific implementation details, or are coupled at a level of abstraction that makes independent evolution impossible.

**Why it looks right:** Copying a pattern from an existing module feels efficient. "The existing `UserService` does it this way, so I'll do the same." Reusing proven implementation details accelerates initial development.

**The actual problem:** Refactoring one file requires immediate, coordinated refactoring of another. A "small" change in requirements ripples across the codebase. It becomes impossible to replace a module with a different implementation (e.g., a fake for testing) without understanding the real implementation's internals. The codebase resists change in proportion to its size.

**Likelihood in autonomous context:** High

**How to detect it:**
- Refactoring one file requires immediate refactoring of another file to keep tests passing
- A fake adapter cannot be built without reading and understanding the real adapter's source
- Domain types import from infrastructure concerns
- Utility functions are copied between modules rather than extracted to a shared location

**The fix:** Depend on abstractions (interfaces) rather than concretes; expose only what is necessary through well-defined contracts.

---

## Premature Abstraction

**What it is:** Generic interfaces, abstract base classes, or "extensibility points" created before two concrete implementations exist to justify them.

**Why it looks right:** Good design means programming to interfaces, not implementations. Creating the abstraction early means not having to change existing code later. It feels like building a foundation before the house.

**The actual problem:** Without two concrete implementations, you have no empirical evidence that the abstraction is correct. The interface reflects guesses about future needs, which are often wrong. The abstraction layer adds complexity without providing flexibility. Future implementations may need to bend to fit the interface, resulting in worse design than if the abstraction had never existed.

**Likelihood in autonomous context:** Low

**How to detect it:**
- An interface or base class has exactly one implementing/inheriting class
- The abstraction was created in the same commit as the first (and only) implementation
- The interface method signatures must change every time a new consumer is added
- There is no documentation or example of a second hypothetical implementation

**The fix:** Wait for the second concrete implementation to emerge naturally; extract the abstraction then based on actual commonality, not predicted commonality.

---

## Architecture Tourists

**What it is:** C4 diagrams, ADRs, or architectural documentation created but never maintained or referenced. The documentation describes a system that doesn't match the code.

**Why it looks right:** Documentation was requested, so it was created. Diagrams look professional. ADRs capture the decision. The team has a deliverable to point to. This counts as "doing architecture."

**The actual problem:** The documentation becomes noise — it occupies space in the repository but provides no signal. New team members are misled. Technical debt accumulates silently because the documentation doesn't reflect reality and no one checks. Phase 7 (Documentation) produces artifacts that no one uses, wasting effort while real architectural issues go unaddressed.

**Likelihood in autonomous context:** High (especially in projects where Phase 7 is skipped or rushed)

**How to detect it:**
- `workspace.dsl` has not been updated since Phase 3
- C4 container diagrams show containers that don't exist in the code
- ADRs reference file paths or module names that have since changed
- The `doc/` directory contains files last modified months ago while code has changed significantly

**The fix:** Treat documentation as code — commit to keeping it current, or delete it. If an artifact cannot be automatically validated against the codebase, it should be generated or deleted.

---

## Leaky Abstraction

**What it is:** An abstraction that exposes implementation details through its interface, defeating the purpose of the abstraction layer.

**Why it looks right:** The abstraction started clean, but edge cases required access to implementation details. Adding a parameter to handle the special case feels pragmatic. The interface still exists, so technically we're "using abstraction."

**The actual problem:** Consumers of the abstraction are coupled to its implementation. Changing the implementation requires finding and updating all consumers. The abstraction doesn't reduce complexity — it adds a layer that must be understood alongside the implementation. New developers must learn both.

**Likelihood in autonomous context:** Medium

**How to detect it:**
- Interface methods include implementation-specific parameters (e.g., `executeQuery(sql: string)` when the interface is meant to be database-agnostic)
- Mock implementations must replicate production logic to satisfy tests
- The interface cannot be implemented correctly without reading the documentation of the implementing class
- Exposed internal state or side effects in interface methods

**The fix:** Keep abstractions at a level that doesn't leak implementation details; if implementation details must be exposed, reconsider whether an abstraction is appropriate.

---

## Monolith-in-Hiding

**What it is:** A project that claims to be a modular monolith or microservices but where all modules share a single database, deployment unit, or runtime.

**Why it looks right:** True microservices are expensive to operate. A modular monolith provides "proper boundaries" while keeping operational costs low. The architecture diagram looks clean.

**The actual problem:** Module boundaries are not enforced at runtime. A bug in one module can corrupt shared database state. Deployment requires the entire system. Scalability is all-or-nothing. The architecture promises loose coupling but delivers tight coupling through shared data storage.

**Likelihood in autonomous context:** Medium

**How to detect it:**
- All modules connect to the same database instance
- There is one `package.json` or one `Cargo.toml` for the entire system
- C4 diagram shows separate containers that are actually a single deployed unit
- Scaling one module requires scaling the entire system

**The fix:** Enforce module boundaries through separate deployment artifacts, or acknowledge the architecture is a monolith and design accordingly.
