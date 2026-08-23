# Argentum Architecture Overview

**Observe → Reason → Plan → Act → Verify → Recover**

Argentum is designed around autonomous execution, not conversation.

## Core Loop

Goal
 ↓
Observe
 ↓
Reason
 ↓
Plan
 ↓
Act
 ↓
Verify
 ↓
Recover
 ↺

## Design Principles

1. Goal-first
2. Stateful
3. Verifiable
4. Recoverable
5. Small & specialized

## Components (v0.1)

- src/runtime/ — Agent loop + tool execution
- src/model/   — Model interface
- src/eval/    — Agentic benchmarks
- src/scripts/ — Training / data / utility scripts
