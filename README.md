# LLM-Powered Multi-Agent Systems: Exploring Documentation-Driven Metamodeling

Data repository for the research paper: **LLM-Powered Multi-Agent Systems: Exploring Documentation-Driven Metamodeling** submitted to *The 22nd European Conference on Modelling Foundations and Applications (ECMFA)*

## Overview

This repository contains experimental data and artifacts for a study exploring how LLM-powered multi-agent systems (LLM-MAS) can automatically generate metamodels from framework documentation. The research compares different approaches to metamodel generation:

1. **Manual baseline** - Expert-created metamodel for reference
2. **LLM-MAS** - Multi-agent system with specialized agents
3. **Prompt chaining** - Sequential prompts without agentic orchestration
4. **Single prompt** - Direct generation without pipeline

## Repository Structure

```
├── data/                    # Experimental outputs and inputs
│   ├── input/              # Source data (26 AI agent frameworks)
│   ├── manual_baseline/    # Expert-created reference artifacts
│   ├── llm-mas/            # LLM-MAS outputs (5 independent runs)
│   ├── prompt_chaining/    # Prompt chaining outputs
│   └── single_prompt/      # Single prompt outputs
├── prompts/                 # All prompts used in experiments
│   ├── llm-mas/            # Agent-specific prompts
│   └── single_prompt/      # Single prompt approach
├── scripts/                 # Analysis and comparison scripts
└── figures/                 # Generated PlantUML diagrams
```

## Metrics

Comparison uses Precision, Recall, and F1-Score on:  
- **Classes** - Metamodel entities
- **Relationships** - Associations/inheritance between classes
- **Attributes** - Properties within classes

### Comparison Methodology

Element equivalence is determined as follows:
- **Classes:** Two classes are considered equivalent if their normalized names are identical.
- **Relationships:** A relationship is defined as a tuple `(source, type, target)` and considered equivalent when all three components match after normalization.
- **Attributes:** An attribute is defined as a pair `(class, attribute_name)` and considered equivalent when both elements match after normalization.

### Limitations

- **Cardinalities ignored:** Relationship comparisons do not consider cardinality constraints (e.g., `1..*`, `0..1`).
- **No semantic analysis:** Matching is purely syntactic after name normalization; semantically equivalent but differently named elements are not matched.
- **Enums as classes:** Enumeration structures are counted and compared as class-like entities.

---

## Model Comparison Results

**Reference Model:** `data\manual_baseline\plantuml_agentic.puml`

- Classes: 43
- Relationships: 72
- Attributes: 37

### Classes

| Run | Precision | Recall | F1-Score | TP | FP | FN |
|-----|-----------|--------|----------|----|----|-----|
| run_1 | 0.5926 | 0.3721 | 0.4571 | 16 | 11 | 27 |
| run_2 | 0.5000 | 0.9535 | 0.6560 | 41 | 41 | 2 |
| run_3 | 0.6721 | 0.9535 | 0.7885 | 41 | 20 | 2 |
| run_4 | 0.6119 | 0.9535 | 0.7455 | 41 | 26 | 2 |
| run_5 | 0.9535 | 0.9535 | 0.9535 | 41 | 2 | 2 |
| **Mean** | **0.6660** | **0.8372** | **0.7201** | 36.0 | 20.0 | 7.0 |

### Relationships

| Run | Precision | Recall | F1-Score | TP | FP | FN |
|-----|-----------|--------|----------|----|----|-----|
| run_1 | 0.3333 | 0.1528 | 0.2095 | 11 | 22 | 61 |
| run_2 | 0.3893 | 0.8056 | 0.5249 | 58 | 91 | 14 |
| run_3 | 0.5370 | 0.8056 | 0.6444 | 58 | 50 | 14 |
| run_4 | 0.6444 | 0.8056 | 0.7160 | 58 | 32 | 14 |
| run_5 | 0.8923 | 0.8056 | 0.8467 | 58 | 7 | 14 |
| **Mean** | **0.5593** | **0.6750** | **0.5883** | 48.6 | 40.4 | 23.4 |

### Attributes

| Run | Precision | Recall | F1-Score | TP | FP | FN |
|-----|-----------|--------|----------|----|----|-----|
| run_1 | 0.3784 | 0.3784 | 0.3784 | 14 | 23 | 23 |
| run_2 | 0.3936 | 1.0000 | 0.5649 | 37 | 57 | 0 |
| run_3 | 0.4512 | 1.0000 | 0.6218 | 37 | 45 | 0 |
| run_4 | 0.4868 | 1.0000 | 0.6549 | 37 | 39 | 0 |
| run_5 | 0.7255 | 1.0000 | 0.8409 | 37 | 14 | 0 |
| **Mean** | **0.4871** | **0.8757** | **0.6122** | 32.4 | 35.6 | 4.6 |

### Overall

| Run | Precision | Recall | F1-Score | TP | FP | FN |
|-----|-----------|--------|----------|----|----|-----|
| run_1 | 0.4227 | 0.2697 | 0.3293 | 41 | 56 | 111 |
| run_2 | 0.4185 | 0.8947 | 0.5702 | 136 | 189 | 16 |
| run_3 | 0.5418 | 0.8947 | 0.6749 | 136 | 115 | 16 |
| run_4 | 0.5837 | 0.8947 | 0.7065 | 136 | 97 | 16 |
| run_5 | 0.8553 | 0.8947 | 0.8746 | 136 | 23 | 16 |
| **Mean** | **0.5644** | **0.7697** | **0.6311** | 117.0 | 96.0 | 35.0 |

### Summary (F1-Scores)

| Run | Classes | Relationships | Attributes | Overall |
|-----|---------|---------------|------------|---------|
| run_1 | 0.4571 | 0.2095 | 0.3784 | 0.3293 |
| run_2 | 0.6560 | 0.5249 | 0.5649 | 0.5702 |
| run_3 | 0.7885 | 0.6444 | 0.6218 | 0.6749 |
| run_4 | 0.7455 | 0.7160 | 0.6549 | 0.7065 |
| run_5 | 0.9535 | 0.8467 | 0.8409 | 0.8746 |
| **Mean** | **0.7201** | **0.5883** | **0.6122** | **0.6311** |

**Best Run:** `run_5` achieved the highest overall F1-score (0.8746), with strong performance across all categories: classes (0.9535), relationships (0.8467), and attributes (0.8409).

---

## Reproducing Results

```bash
# Generate comparison table
python scripts/generate_comparison_table.py

# Compare individual PlantUML models
python scripts/compare_plantuml_models.py data/manual_baseline/plantuml_agentic.puml data/llm-mas/run_1/plantuml_agentic.puml

# Compare terminology CSVs
python scripts/compare_terms_csv.py data/manual_baseline/terms.csv data/llm-mas/run_1/terms.csv
```

## Citation

Include bibtex if accepted


## License

Include License information if accepted