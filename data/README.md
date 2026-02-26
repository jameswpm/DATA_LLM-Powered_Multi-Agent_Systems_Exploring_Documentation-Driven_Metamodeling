# Data Directory

This folder contains all experimental data used in the paper.

## Structure

| Directory | Description |
|-----------|-------------|
| `input/` | Source data: list of 26 AI agent frameworks analyzed |
| `manual_baseline/` | Expert-created reference artifacts for comparison |
| `llm-mas/` | Outputs from LLM multi-agent system (5 runs) |
| `prompt_chaining/` | Outputs from sequential prompt approach |
| `single_prompt/` | Outputs from single prompt approach |

## Artifact Types

Each experimental directory contains:

| File | Description |
|------|-------------|
| `terms.csv` | Raw terminology extracted from documentation |
| `scored_terms.csv` | Consolidated and scored terminology |
| `plantuml_agentic.puml` | Generated PlantUML class diagram |

## Input Data

The `input/frameworks_list.csv` contains 26 AI agent frameworks analyzed:
- Agno, Atomic Agents, AutoChain, BeeAI, BESSER, CAMEL, CrewAI, Eclipse LMOS, Google ADK, KaibanJS, LangGraph, Langroid, LlamaIndex, Marvin, Mastra, MetaGPT, PocketFlow, PraisonAI, Pydantic AI, Rig, SemanticKernel, smolagents, Swarm RS, uAgents, Upsonic, VoltAgent
