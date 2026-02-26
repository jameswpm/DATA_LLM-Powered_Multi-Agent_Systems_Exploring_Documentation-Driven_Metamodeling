# LLM Multi-Agent System (LLM-MAS) Outputs

This directory contains outputs from the LLM-MAS pipeline.

## Agents

The pipeline uses four specialized agents:
1. **Analyst** - Web page classifier for API documentation
2. **Doc Expert** - Extracts domain terminology from documentation
3. **Terminology Expert** - Consolidates and scores terminology
4. **Modeler** - Generates PlantUML class diagrams

## Runs

Each `run_*` directory is an independent execution with identical inputs. Multiple runs capture variability in LLM outputs.

## Files per Run

| File | Description |
|------|-------------|
| `terms.csv` | Raw terminology extracted from framework docs |
| `scored_terms.csv` | Consolidated terminology with importance scores |
| `plantuml_agentic.puml` | Generated PlantUML class diagram |

## Notes

- CSVs include headers
- PlantUML files can be rendered at [plantuml.com](https://www.plantuml.com/plantuml/)
- PNG versions of the PlantUML are in folder figures