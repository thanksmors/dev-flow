# Domain Anti-Patterns

Anti-patterns related to domain modeling, entity design, and aggregate boundaries.

---

## Anemic Domain Model

**What it is:** Entities that are pure data containers — TypeScript interfaces or classes with only properties, no methods or behavior.

**Why it looks right:** Separating "data" from "logic" feels clean. Interfaces are easy to type. Business rules can live in "services" that operate on the data. This mirrors how ORMs and API boundaries work, so it feels proven.

**The actual problem:** Domain logic scatters across services, becoming harder to find and test. Invariants — rules that must always hold — are not encapsulated. Objects become "dumb data" that any code can mutate into invalid states. The model doesn't protect itself; every consumer must know the rules.

**Likelihood in autonomous context:** High

**How to detect it:**
- Entity files contain only `interface` declarations or classes with only `readonly` properties
- No invariant tests exist (`* invariants.test.ts`)
- Business rules exist as standalone functions in `src/services/` or `src/utils/`
- TypeScript strictness is partially disabled (`// @ts-ignore` near entity definitions)

**The fix:** Encapsulate invariants and business logic within the entity itself; make the entity the first line of defense for domain rules.

---

## God Aggregate

**What it is:** A single aggregate that encompasses the entire system — one root entity that references every other type, with no boundaries between subdomains.

**Why it looks right:** Everything relates to everything else in the domain, so "why not put it all in one aggregate?" It avoids the complexity of defining boundaries. Operations are convenient because all data is accessible from one place.

**The actual problem:** The aggregate grows without limit. Every change risks violating its invariants because the scope of invariants is unbounded. The repository becomes a bottleneck — you must load the entire system state to use any part of it. Concurrency becomes impossible because one lock covers everything. Eventually, no developer can reason about this aggregate fully.

**Likelihood in autonomous context:** Medium

**How to detect it:**
- One entity file exceeds 200 lines
- The entity declares properties referencing 10+ other domain types
- No repository interface can be written without depending on this one entity
- `git blame` shows every developer on the team modifying this file

**The fix:** Identify natural bounded contexts and split into separate aggregates with explicit boundaries and owned data.

---

## Deep Hierarchy

**What it is:** Domain types nested 5 or more levels — a type has a property that's a list of another type that has a property that's a list of another type, and so on.

**Why it looks right:** Nesting types to reflect real-world hierarchies feels natural. "A Company has Departments has Teams has Employees has Skills" mirrors how organizations work in the problem domain. The type system enforces completeness at each level.

**The actual problem:** Traversing 5+ levels to access a leaf value is cumbersome and fragile. Serialization/deserialization breaks at any level. Testing requires constructing the entire tree. The type hierarchy becomes a implicit coupling mechanism — changing a leaf type requires propagating changes up the entire chain. Aggregates with deep hierarchies often indicate a God Aggregate in disguise.

**Likelihood in autonomous context:** Medium

**How to detect it:**
- A type definition contains `Array<Array<Array<...>>>` nesting
- Domain types import from each other in a chain (A imports B, B imports C, C imports D, D imports E)
- A query or operation must unwrap 5+ levels to access a simple value
- TypeScript error messages show deeply indented generic instantiation

**The fix:** Flatten the hierarchy by identifying which associations are truly compositional (must be together) versus relationships (can be queried separately).

---

## Shared Identity

**What it is:** Multiple distinct domain concepts sharing the same identifier type (e.g., `id: string` for both `User` and `Organization`).

**Why it looks right:** Identifier generation is a concern that shouldn't clutter domain types. Using a shared type like `string` or `UUID` keeps things simple and consistent. The same pattern works in databases and APIs.

**The actual problem:** Nothing in the type system prevents confusing a User ID with an Organization ID. Passing the wrong identifier type compiles without warning. The domain layer loses semantic precision — you cannot look at a value and know what it identifies. This ambiguity compounds as the system grows, leading to runtime errors where a User ID is used where an Organization ID is expected.

**Likelihood in autonomous context:** High

**How to detect it:**
- Domain types use primitive types (`string`, `number`) for identifiers
- No dedicated ID types exist in the domain layer
- Functions accept identifier parameters but don't constrain which kind
- Test helpers generate IDs without naming which entity they belong to

**The fix:** Create distinct branded types for each identifier concept (e.g., `UserId`, `OrganizationId`) that are incompatible despite sharing the same underlying primitive.

---

## Domain Anemia Through Anxious Abstraction

**What it is:** Domain entities are abstracted behind interfaces "for flexibility," but the interfaces expose setters and mutable state, defeating the purpose of abstraction.

**Why it looks right:** Programming to interfaces is good practice. If we define an interface for `UserRepository`, we can swap implementations. This feels like SOLID design. Defensive coding suggests making everything mutable to handle "all cases."

**The actual problem:** The interface doesn't encapsulate anything — it just renames the mutators. Changing the entity still requires finding all implementations. The "flexibility" is illusory because the interface leaks the same complexity as the concrete type. The abstraction adds a layer of indirection without adding a layer of safety.

**Likelihood in autonomous context:** Medium

**How to detect it:**
- Repository interfaces expose `save()`, `update()`, `delete()` methods accepting entity parameters
- Entity interfaces include `setName()`, `updateEmail()` style mutators
- Interface files are nearly identical to implementing class files
- `implements` clauses appear without corresponding `extends` or composition

**The fix:** Push behavior into the entity; keep interfaces narrow and focused on capabilities rather than data mutation.
