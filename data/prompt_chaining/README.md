# Prompt Chaining Outputs

Results from a sequential prompt approach without agentic orchestration.

## Approach

Uses the same prompts as the LLM-MAS experiment, but:
- No tool invocation
- No agentic frameworks or workflow definitions
- Prompts executed in sequence manually
- Minimal scripting only to ensure output format consistency

## Purpose

Baseline to isolate the contribution of multi-agent orchestration vs. prompt design alone.

## Files

| File | Description |
|------|-------------|
| `terms.csv` | Extracted terminology |
| `scored_terms.csv` | Scored terminology |
| `plantuml_agentic.puml` | Generated class diagram |