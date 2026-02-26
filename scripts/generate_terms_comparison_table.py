"""
Generate Markdown Comparison Table for Terms CSV

Compares terms.csv and scored_terms.csv from all LLM-MAS runs 
against the manual baseline reference and outputs a markdown table 
with precision, recall, and F1-score metrics.

Usage:
    python generate_terms_comparison_table.py
"""

import sys
from pathlib import Path

# Add scripts directory to path for import
sys.path.insert(0, str(Path(__file__).parent))

from compare_terms_csv import compare_csv_files


def compute_mean_metrics(comparisons):
    """Compute mean of metrics across all comparisons."""
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
        m = comp["metrics"]
        for key in totals:
            totals[key] += m[key]
    
    return {key: val / n for key, val in totals.items()}


def generate_markdown_table():
    """Generate a markdown table comparing all runs against the baseline."""
    
    # Define paths
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / "data"
    
    baseline_dir = data_dir / "manual_baseline"
    llm_mas_dir = data_dir / "llm-mas"
    
    # Reference files
    ref_terms_path = baseline_dir / "terms.csv"
    ref_scored_terms_path = baseline_dir / "scored_terms.csv"
    
    # Find all run directories
    run_dirs = sorted(llm_mas_dir.glob("run_*"))
    
    # Validate reference files exist
    if not ref_terms_path.exists():
        print(f"Error: Reference file not found: {ref_terms_path}")
        return 1
    
    if not ref_scored_terms_path.exists():
        print(f"Error: Reference file not found: {ref_scored_terms_path}")
        return 1
    
    # Collect comparisons
    terms_comparisons = []
    scored_terms_comparisons = []
    
    for run_dir in run_dirs:
        run_name = run_dir.name
        
        # Compare terms.csv
        terms_path = run_dir / "terms.csv"
        if terms_path.exists():
            result = compare_csv_files(ref_terms_path, terms_path, "terms")
            result["run_name"] = run_name
            terms_comparisons.append(result)
        else:
            print(f"Warning: {terms_path} not found")
        
        # Compare scored_terms.csv
        scored_terms_path = run_dir / "scored_terms.csv"
        if scored_terms_path.exists():
            result = compare_csv_files(ref_scored_terms_path, scored_terms_path, "scored_terms")
            result["run_name"] = run_name
            scored_terms_comparisons.append(result)
        else:
            print(f"Warning: {scored_terms_path} not found")
    
    # Get reference counts
    ref_terms_result = compare_csv_files(ref_terms_path, ref_terms_path, "terms")
    ref_scored_result = compare_csv_files(ref_scored_terms_path, ref_scored_terms_path, "scored_terms")
    
    # Generate markdown output
    print("## Terms CSV Comparison Results\n")
    print(f"**Reference (Manual Baseline):**")
    print(f"- `terms.csv`: {ref_terms_result['reference_count']} terms")
    print(f"- `scored_terms.csv`: {ref_scored_result['reference_count']} terms\n")
    
    # Compute average terms across all runs
    if terms_comparisons:
        avg_terms = sum(c['model_count'] for c in terms_comparisons) / len(terms_comparisons)
    else:
        avg_terms = 0
    
    if scored_terms_comparisons:
        avg_scored_terms = sum(c['model_count'] for c in scored_terms_comparisons) / len(scored_terms_comparisons)
    else:
        avg_scored_terms = 0
    
    print("**Average Model Statistics (across all runs):**\n")
    print(f"- `terms.csv`: {avg_terms:.1f} terms")
    print(f"- `scored_terms.csv`: {avg_scored_terms:.1f} terms\n")
    
    # Terms.csv metrics table
    print("### terms.csv Comparison\n")
    print("| Run | Precision | Recall | F1-Score | TP | FP | FN | Model Terms |")
    print("|-----|-----------|--------|----------|----|----|-----|-------------|")
    for comp in terms_comparisons:
        m = comp["metrics"]
        print(f"| {comp['run_name']} | {m['precision']:.4f} | {m['recall']:.4f} | {m['f1_score']:.4f} | {m['true_positives']} | {m['false_positives']} | {m['false_negatives']} | {comp['model_count']} |")
    
    if terms_comparisons:
        mean = compute_mean_metrics(terms_comparisons)
        mean_model_count = sum(c['model_count'] for c in terms_comparisons) / len(terms_comparisons)
        print(f"| **Mean** | **{mean['precision']:.4f}** | **{mean['recall']:.4f}** | **{mean['f1_score']:.4f}** | {mean['true_positives']:.1f} | {mean['false_positives']:.1f} | {mean['false_negatives']:.1f} | {mean_model_count:.1f} |")
    print()
    
    # Scored_terms.csv metrics table
    print("### scored_terms.csv Comparison\n")
    print("| Run | Precision | Recall | F1-Score | TP | FP | FN | Model Terms |")
    print("|-----|-----------|--------|----------|----|----|-----|-------------|")
    for comp in scored_terms_comparisons:
        m = comp["metrics"]
        print(f"| {comp['run_name']} | {m['precision']:.4f} | {m['recall']:.4f} | {m['f1_score']:.4f} | {m['true_positives']} | {m['false_positives']} | {m['false_negatives']} | {comp['model_count']} |")
    
    if scored_terms_comparisons:
        mean = compute_mean_metrics(scored_terms_comparisons)
        mean_model_count = sum(c['model_count'] for c in scored_terms_comparisons) / len(scored_terms_comparisons)
        print(f"| **Mean** | **{mean['precision']:.4f}** | **{mean['recall']:.4f}** | **{mean['f1_score']:.4f}** | {mean['true_positives']:.1f} | {mean['false_positives']:.1f} | {mean['false_negatives']:.1f} | {mean_model_count:.1f} |")
    print()
    
    # Summary table (F1-Scores comparison)
    print("### Summary (F1-Scores)\n")
    print("| Run | terms.csv | scored_terms.csv |")
    print("|-----|-----------|------------------|")
    for i, terms_comp in enumerate(terms_comparisons):
        run_name = terms_comp['run_name']
        terms_f1 = terms_comp['metrics']['f1_score']
        scored_f1 = scored_terms_comparisons[i]['metrics']['f1_score'] if i < len(scored_terms_comparisons) else "N/A"
        if isinstance(scored_f1, float):
            print(f"| {run_name} | {terms_f1:.4f} | {scored_f1:.4f} |")
        else:
            print(f"| {run_name} | {terms_f1:.4f} | {scored_f1} |")
    
    if terms_comparisons and scored_terms_comparisons:
        mean_terms = compute_mean_metrics(terms_comparisons)
        mean_scored = compute_mean_metrics(scored_terms_comparisons)
        print(f"| **Mean** | **{mean_terms['f1_score']:.4f}** | **{mean_scored['f1_score']:.4f}** |")
    
    return 0


if __name__ == "__main__":
    exit(generate_markdown_table())
