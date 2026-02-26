# Prompts

All prompts used in the experiments. These are the exact versions used to generate the results in the paper.

## Structure

### `llm-mas/`

Agent-specific prompts for the multi-agent system (also used in the prompt chaining):

| File | Agent | Purpose |
|------|-------|----------|
| `analyst.md` | Analyst | Classifies web pages as API documentation |
| `doc_expert.md` | Doc Expert | Extracts domain terminology from docs |
| `terminology_expert.md` | Terminology Expert | Consolidates and scores terminology |
| `modeler.md` | Modeler | Generates PlantUML class diagrams |

### `single_prompt/`

| File | Purpose |
|------|----------|
| `generate_plantuml.md` | Direct metamodel generation without pipeline |

## Note

Prompts may evolve in the system during continued experimentation. This directory preserves the exact versions used for the results in the paper.