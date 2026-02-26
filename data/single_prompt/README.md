# Single Prompt Outputs

Baseline results from direct metamodel generation using a single prompt.

## Approach

Asks the LLM to generate a PlantUML class diagram representing an AI agent framework metamodel, relying solely on its internal knowledge with no documentation retrieval or pipeline.

## Purpose

Establishes a baseline to measure the value added by:
- Documentation-driven terminology extraction
- Multi-step pipelines
- Multi-agent orchestration

## Files

| File | Description |
|------|-------------|
| `plantuml_agentic.puml` | Generated class diagram |

**Note:** No intermediate artifacts (`terms.csv`, `scored_terms.csv`) since no terminology extraction step was performed.