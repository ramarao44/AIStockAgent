# AIStockAgent — Token-Optimized Copilot Instructions

## Goal
Use this repository with a low-token, high-signal workflow. Prefer small, targeted changes that directly satisfy the requirements in docs/req.md and docs/architecture.md.

## Working rules
- Treat docs/req.md and docs/architecture.md as the source of truth.
- Do not restate the full requirements unless the user asks.
- Implement the smallest change that completes the task.
- Reuse existing modules in Python/ instead of creating duplicate logic.
- Keep responses short, practical, and focused on the next step.
- Favor free/local-first tools and simple Python implementations.

## Project context
- Build a zero-cost stock intelligence system.
- Core stack: Python, local file/watchlist support, free market data sources, and optional n8n/WhatsApp integration.
- Primary output should remain structured and JSON-friendly where applicable.

## Default behavior
- If a request is ambiguous, ask one short clarification question instead of generating a large plan.
- When editing code, make the minimum viable change and avoid unnecessary refactors.
- Prefer clear names, simple functions, and robust error handling over verbose abstractions.
