# Stack Adaptation

> Covers: procedure to detect and respect the target project's technology stack and conventions; compact convention table for common ecosystems; the rule for recommending a replacement (DECISION D-13)
> Retrieved: 2026-09-04
> Sources: This file describes a detection procedure and repository conventions observable in the target project; ecosystem rows are general knowledge of each toolchain's manifest and are to be confirmed by inspecting the actual repository, not asserted from this table.
> Evidence: RECOMMENDATION, DECISION

Load when: starting work in a repository, before proposing tools, commands, layouts or libraries.

## 1. Detection procedure (run before any design or code change)

1. **Manifests**: list root and first-level manifest files (table §2). Record language(s), framework(s), package manager, versions pinned (lockfiles, `.tool-versions`, `.nvmrc`, `pyproject`, `go.mod`, `pubspec.yaml`, `pom.xml`/`build.gradle*`).
2. **Commands**: read scripts/targets (`package.json` scripts, `Makefile`, `justfile`, `Taskfile`, Gradle/Maven tasks, `pyproject` tool sections). These are the source of truth for build/test/lint — use them; do not invent commands.
3. **Quality tooling**: linters/formatters configs, test framework config, type checker, pre-commit hooks, CI workflow files (`.github/workflows`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `Jenkinsfile`, `bitbucket-pipelines.yml`).
4. **Runtime and infra**: `Dockerfile`, `docker-compose*`, Kubernetes manifests/Helm, Terraform/Pulumi/CloudFormation, serverless configs, platform files (`Procfile`, `fly.toml`, `vercel.json`).
5. **Layout conventions**: where source, tests, migrations, docs and configs live; naming style; module boundaries; existing ADRs or docs.
6. **Existing engineering docs**: `docs/engineering/STATE.md`, ADRs, README sections — reuse rather than duplicate.
7. Record the summary in `STATE.md › Stack` (languages, frameworks, versions, commands for build/test/lint/run, CI, deploy target). Mark anything not found as unknown, then ask only if it blocks the current skill.

Secrets during detection: `.env*`, credential files and CI secret configs are sensitive. Read variable *names* to learn the configuration surface; never print, quote or copy their values into STATE, artifacts, logs or chat. If a secret is found committed to the repository, record it as a High security finding (`security › D/G`) without reproducing the value.

## 2. Convention table (indicative; verify against the repository)

| Ecosystem | Manifest signals | Package/build | Tests (common) | Lint/format (common) | Migrations (common) |
|---|---|---|---|---|---|
| Node/TypeScript | `package.json`, lockfile (`package-lock`, `yarn.lock`, `pnpm-lock`), `tsconfig.json` | npm/yarn/pnpm scripts | Jest, Vitest, Mocha, Playwright/Cypress (e2e) | ESLint, Prettier, Biome | Prisma, Knex, TypeORM, Drizzle |
| Python | `pyproject.toml`, `requirements*.txt`, `poetry.lock`, `uv.lock` | pip/poetry/uv; `pytest` | pytest, unittest | ruff, black, mypy | Alembic, Django migrations |
| Java/Kotlin | `pom.xml`, `build.gradle(.kts)` | Maven/Gradle | JUnit 5, Testcontainers | Checkstyle, Spotless, detekt | Flyway, Liquibase |
| .NET | `*.csproj`, `*.sln` | dotnet CLI | xUnit, NUnit | dotnet format, analyzers | EF Core migrations |
| Go | `go.mod` | go build/test | `testing`, testify | gofmt, golangci-lint | golang-migrate, goose |
| Rust | `Cargo.toml` | cargo | built-in tests | rustfmt, clippy | sqlx, diesel |
| Dart/Flutter | `pubspec.yaml` | flutter/dart CLI | `flutter test`, integration_test | dart analyze, dart format | drift, sqflite (local) |
| React Native | `package.json` + `android/`, `ios/` | npm/yarn + Gradle/Xcode | Jest, Detox | ESLint, Prettier | (backend-side) |
| Swift/Kotlin native | `*.xcodeproj`/`Package.swift`; `build.gradle` | Xcode/SwiftPM; Gradle | XCTest; JUnit/Espresso | SwiftLint; ktlint | Core Data/Room |
| PHP | `composer.json` | composer | PHPUnit, Pest | PHP-CS-Fixer, PHPStan | Laravel/Doctrine migrations |
| Ruby | `Gemfile` | bundler | RSpec, Minitest | RuboCop | ActiveRecord migrations |

Databases and infrastructure are detected from connection configs, ORMs, `docker-compose` services and IaC files; record them under Stack as well.

## 3. Respect-the-stack rules (DECISION D-13)

1. Use the detected tools and commands; add new tools only when the stack lacks the capability (e.g., no test runner configured).
2. Follow existing layout, naming and module conventions even when a different one is preferred.
3. Match versions: target the language/framework version pinned by the project; avoid APIs newer than the pinned version.
4. Propose replacing a stack element only when a `REQ`/`CON` cannot be met with it; write an ADR with drivers, options, costs and migration path; this is a **Stop and ask**.
5. When the user names a stack for a new project, treat it as `CON-###` and design within it; ask before deviating.
6. Language of artifacts follows the repository's existing documentation language; default English.

## 4. Platform notes

Engineering concerns that differ by platform (frontend state, mobile offline/permissions, backend resilience, async messaging) are covered generically in `skills/implementation/references/`. They apply to any framework in that category.
