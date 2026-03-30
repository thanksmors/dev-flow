---
name: prerequisites
description: Phase 0 prerequisites hard gate — must pass before any dev-flow phase begins
---

# Prerequisites Checklist

Run this before starting any dev-flow phase. Every item must PASS.

## Runtime & Tools

| # | Check | Command | Expected |
|---|-------|---------|----------|
| 1 | Bun runtime | `bun --version` | Exits 0, version printed |
| 2 | Git repository | `git status` | Exits 0, not "not a git repository" |
| 3 | GitHub CLI authenticated | `gh auth status` | Exits 0, shows logged-in account |

## MCPs

| # | Check | How to verify |
|---|-------|---------------|
| 4 | Insforge MCP | Ping MCP server — confirm connection |
| 5 | Context7 MCP | Ping MCP server — confirm connection |
| 6 | Playwright MCP | Ping MCP server — confirm connection |
| 7 | GitHub MCP | Ping MCP server — confirm connection |

## Environment Variables

| # | Variable | Check |
|---|----------|-------|
| 8 | `.env` file exists | `test -f .env && echo "PASS" \|\| echo "FAIL"` |
| 9 | `INSFORGE_URL` | Set in `.env` |
| 10 | `INSFORGE_API_KEY` | Set in `.env` |
| 11 | `NUXT_PUBLIC_APP_URL` | Set in `.env` |

## Plugins & Skills

| # | Check | How to verify |
|---|-------|---------------|
| 12 | superpowers plugin | Invoke a superpowers skill — confirm response |
| 13 | dev-flow plugin | Invoke dev-flow command — confirm response |
| 14 | hookify plugin | Invoke hookify skill — confirm response |

## Required Skills

| # | Skill | How to verify |
|---|-------|---------------|
| 15 | verification-before-completion | Invoke skill — confirm response |
| 16 | test-driven-development | Invoke skill — confirm response |
| 17 | brainstorming | Invoke skill — confirm response |
| 18 | writing-plans | Invoke skill — confirm response |
| 19 | executing-plans | Invoke skill — confirm response |

## Required Agents

| # | Agent | Check |
|---|-------|-------|
| 20 | implementer | Agent file exists at configured path |
| 21 | spec-reviewer | Agent file exists at configured path |
| 22 | quality-reviewer | Agent file exists at configured path |

## Project Structure

| # | Check | Command |
|---|-------|---------|
| 23 | `dev-flow/` directory exists | `test -d dev-flow` |
| 24 | `dev-flow/phases/` exists | `test -d dev-flow/phases` |
| 25 | `dev-flow/references/` exists | `test -d dev-flow/references` |
| 26 | `.gitignore` includes `.dev-flow/` | `grep -q ".dev-flow" .gitignore` |
| 27 | `package.json` exists | `test -f package.json` |

## Test Infrastructure

| # | Check | Command | Expected |
|---|-------|---------|----------|
| 28 | bun test runs | `bun test` | Exits 0 (green baseline) |
| 29 | Playwright installed | `bunx playwright --version` | Exits 0 |

## Dependencies

| # | Package | Check |
|---|---------|-------|
| 30 | fast-check | In devDependencies |
| 31 | zod | In dependencies |
| 32 | playwright | In devDependencies |
| 33 | @nuxt/ui | In dependencies |
| 34 | nuxt | In dependencies |

## Nuxt Setup

| # | Check | Command |
|---|-------|---------|
| 35 | `nuxt.config.ts` exists | `test -f nuxt.config.ts` |
| 36 | Layers directory exists | `test -d layers` |

## How to Run

Execute each check in order. Print PASS/FAIL per item. If ANY item FAILS:
- Print the failing item and remediation instructions
- Do NOT proceed to Phase 1
- User fixes the issue and re-runs the gate

This checklist is customizable per project — add or remove items in this file as needed.
