# Worked Example: API Endpoint

Adding a REST API endpoint — GET /api/users/{id} — to workspace.dsl.

## Scenario

Implementing: **GET /api/users/{id}** — retrieves a user by ID. Uses an API processor to handle the request and a repository to fetch the entity.

## Components to Add

| Layer | Component | Type | Why |
|---|---|---|---|
| Application | UserItemProcessor | StateProcessor | API Platform state processor for user item |
| Domain | User | Entity | The aggregate being retrieved |
| Domain | UserRepositoryInterface | Interface | Hexagonal port for data access |
| Infrastructure | UserRepository | Repository | Implements the port with MariaDB |
| External | Database | MariaDB | User data storage |

## Step 1: Add Application Components

```structurizr
userItemProcessor = component "UserItemProcessor" "Processes user item state for GET /api/users/{id}" "StateProcessor" {
    tags "Item"
}
```

## Step 2: Add Domain Components

```structurizr
user = component "User" "User entity" "Entity" {
    tags "Item"
}

userRepositoryInterface = component "UserRepositoryInterface" "Contract for user data access" "Interface" {
    tags "Item"
}
```

## Step 3: Add Infrastructure Components

```structurizr
userRepository = component "UserRepository" "Retrieves users from MariaDB" "Repository" {
    tags "Item"
}
```

## Step 4: Add External Dependencies

```structurizr
database = component "Database" "MariaDB instance" "MariaDB" {
    tags "Database"
}
```

## Step 5: Add Relationships

```structurizr
// Request flow
userItemProcessor -> userRepository "retrieves user via"
userItemProcessor -> user "returns"

// Data access
userRepository -> userRepositoryInterface "implements"
userRepository -> user "retrieves"
userRepository -> database "accesses data"
```

## Verification Checklist

- [ ] All components defined with correct layer grouping
- [ ] External dependency (database) outside groups
- [ ] Relationships use standardized labels from `references/dsl-relationship-patterns.md`
- [ ] Component types specified

## What to Exclude

- `UserResponseDTO` — DTO, not a component
- `UuidTransformer` — implementation detail of ID transformation
- Framework configuration classes
