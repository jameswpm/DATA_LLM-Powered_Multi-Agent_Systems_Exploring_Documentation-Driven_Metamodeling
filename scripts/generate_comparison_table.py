"""
Generate Markdown Comparison Table

Compares all LLM-MAS runs against the manual baseline reference
and outputs a markdown table with precision, recall, and F1-score metrics.

Usage:
    python generate_comparison_table.py
"""

import sys
from pathlib import Path

# Add scripts directory to path for import
sys.path.insert(0, str(Path(__file__).parent))

from compare_plantuml_models import compare_models


def compute_mean_metrics(comparisons, metric_type):
    """Compute mean of metrics across all comparisons for a given metric type."""
    if not comparisons:
        return None
    
    n = len(comparisons)
    totals = {
        'precision': 0.0,
        'recall': 0.0,
        'f1_score': 0.0,
        'true_positives': 0,
        'false_positives': 0,
        'false_negatives': 0
    }
    
    for comp in comparisons:
        m = comp["metrics"][metric_type]
        for key in totals:
            totals[key] += m[key]
    
    return {key: val / n for key, val in totals.items()}


def generate_markdown_table():
    """Generate a markdown table comparing all runs against the baseline."""
    
    # Define paths
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / "data"
    
    reference_path = data_dir / "manual_baseline" / "plantuml_agentic.puml"
    llm_mas_dir = data_dir / "llm-mas"
    
    # Find all run directories
    run_dirs = sorted(llm_mas_dir.glob("run_*"))
    model_paths = [run_dir / "plantuml_agentic.puml" for run_dir in run_dirs]
    
    # Validate files exist
    if not reference_path.exists():
        print(f"Error: Reference file not found: {reference_path}")
        return 1
    
    for model_path in model_paths:
        if not model_path.exists():
            print(f"Error: Model file not found: {model_path}")
            return 1
    
    # Run comparison
    results = compare_models(reference_path, model_paths)
    
    # Generate markdown table
    print("## Model Comparison Results\n")
    print(f"**Reference Model:** `{reference_path.relative_to(data_dir.parent)}`\n")
    print(f"- Classes: {results['reference_stats']['classes']}")
    print(f"- Relationships: {results['reference_stats']['relationships']}")
    print(f"- Attributes: {results['reference_stats']['attributes']}\n")
    
    # Compute average model stats across all runs
    n_models = len(results["comparisons"])
    avg_classes = sum(comp["model_stats"]["classes"] for comp in results["comparisons"]) / n_models
    avg_relationships = sum(comp["model_stats"]["relationships"] for comp in results["comparisons"]) / n_models
    avg_attributes = sum(comp["model_stats"]["attributes"] for comp in results["comparisons"]) / n_models
    
    print("**Average Model Statistics (across all runs):**\n")
    print(f"- Classes: {avg_classes:.1f}")
    print(f"- Relationships: {avg_relationships:.1f}")
    print(f"- Attributes: {avg_attributes:.1f}\n")
    
    # Classes metrics table
    print("### Classes\n")
    print("| Run | Precision | Recall | F1-Score | TP | FP | FN |")
    print("|-----|-----------|--------|----------|----|----|-----|")
    for comp in results["comparisons"]:
        run_name = Path(comp["model_path"]).parent.name
        m = comp["metrics"]["classes"]
        print(f"| {run_name} | {m['precision']:.4f} | {m['recall']:.4f} | {m['f1_score']:.4f} | {m['true_positives']} | {m['false_positives']} | {m['false_negatives']} |")
    mean = compute_mean_metrics(results["comparisons"], "classes")
    print(f"| **Mean** | **{mean['precision']:.4f}** | **{mean['recall']:.4f}** | **{mean['f1_score']:.4f}** | {mean['true_positives']:.1f} | {mean['false_positives']:.1f} | {mean['false_negatives']:.1f} |")
    print()
    
    # Relationships metrics table
    print("### Relationships\n")
    print("| Run | Precision | Recall | F1-Score | TP | FP | FN |")
    print("|-----|-----------|--------|----------|----|----|-----|")
    for comp in results["comparisons"]:
        run_name = Path(comp["model_path"]).parent.name
        m = comp["metrics"]["relationships"]
        print(f"| {run_name} | {m['precision']:.4f} | {m['recall']:.4f} | {m['f1_score']:.4f} | {m['true_positives']} | {m['false_positives']} | {m['false_negatives']} |")
    mean = compute_mean_metrics(results["comparisons"], "relationships")
    print(f"| **Mean** | **{mean['precision']:.4f}** | **{mean['recall']:.4f}** | **{mean['f1_score']:.4f}** | {mean['true_positives']:.1f} | {mean['false_positives']:.1f} | {mean['false_negatives']:.1f} |")
    print()
    
    # Attributes metrics table
    print("### Attributes\n")
    print("| Run | Precision | Recall | F1-Score | TP | FP | FN |")
    print("|-----|-----------|--------|----------|----|----|-----|")
    for comp in results["comparisons"]:
        run_name = Path(comp["model_path"]).parent.name
        m = comp["metrics"]["attributes"]
        print(f"| {run_name} | {m['precision']:.4f} | {m['recall']:.4f} | {m['f1_score']:.4f} | {m['true_positives']} | {m['false_positives']} | {m['false_negatives']} |")
    mean = compute_mean_metrics(results["comparisons"], "attributes")
    print(f"| **Mean** | **{mean['precision']:.4f}** | **{mean['recall']:.4f}** | **{mean['f1_score']:.4f}** | {mean['true_positives']:.1f} | {mean['false_positives']:.1f} | {mean['false_negatives']:.1f} |")
    print()
    
    # Overall metrics table
    print("### Overall\n")
    print("| Run | Precision | Recall | F1-Score | TP | FP | FN |")
    print("|-----|-----------|--------|----------|----|----|-----|")
    for comp in results["comparisons"]:
        run_name = Path(comp["model_path"]).parent.name
        m = comp["metrics"]["overall"]
        print(f"| {run_name} | {m['precision']:.4f} | {m['recall']:.4f} | {m['f1_score']:.4f} | {m['true_positives']} | {m['false_positives']} | {m['false_negatives']} |")
    mean = compute_mean_metrics(results["comparisons"], "overall")
    print(f"| **Mean** | **{mean['precision']:.4f}** | **{mean['recall']:.4f}** | **{mean['f1_score']:.4f}** | {mean['true_positives']:.1f} | {mean['false_positives']:.1f} | {mean['false_negatives']:.1f} |")
    print()
    
    # Summary table (just F1 scores for quick comparison)
    print("### Summary (F1-Scores)\n")
    print("| Run | Classes | Relationships | Attributes | Overall |")
    print("|-----|---------|---------------|------------|---------|")
    for comp in results["comparisons"]:
        run_name = Path(comp["model_path"]).parent.name
        m = comp["metrics"]
        print(f"| {run_name} | {m['classes']['f1_score']:.4f} | {m['relationships']['f1_score']:.4f} | {m['attributes']['f1_score']:.4f} | {m['overall']['f1_score']:.4f} |")
    # Compute means for summary
    mean_classes = compute_mean_metrics(results["comparisons"], "classes")
    mean_rels = compute_mean_metrics(results["comparisons"], "relationships")
    mean_attrs = compute_mean_metrics(results["comparisons"], "attributes")
    mean_overall = compute_mean_metrics(results["comparisons"], "overall")
    print(f"| **Mean** | **{mean_classes['f1_score']:.4f}** | **{mean_rels['f1_score']:.4f}** | **{mean_attrs['f1_score']:.4f}** | **{mean_overall['f1_score']:.4f}** |")
    
    return 0


if __name__ == "__main__":
    exit(generate_markdown_table())
