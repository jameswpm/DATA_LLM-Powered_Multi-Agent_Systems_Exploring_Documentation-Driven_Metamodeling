"""
CSV Terms Comparison Script

Compares terms extracted from CSV files by normalizing term names
and computing precision, recall, and F1-score metrics.

Usage:
    python compare_terms_csv.py <reference_terms.csv> <model_terms.csv> [--scored-reference <ref_scored.csv>] [--scored-model <model_scored.csv>] [--output results.json]

Examples:
    # Compare only terms.csv files
    python compare_terms_csv.py paper_data/manual_baseline/terms.csv paper_data/llm-mas/run_1/terms.csv

    # Compare both terms.csv and scored_terms.csv files
    python compare_terms_csv.py paper_data/manual_baseline/terms.csv paper_data/llm-mas/run_1/terms.csv \
        --scored-reference paper_data/manual_baseline/scored_terms.csv \
        --scored-model paper_data/llm-mas/run_1/scored_terms.csv
"""

import argparse
import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Set


@dataclass
class MetricResult:
    """Holds precision, recall, and F1 metrics."""
    precision: float
    recall: float
    f1_score: float
    true_positives: int
    false_positives: int
    false_negatives: int
    tp_terms: Set[str]
    fp_terms: Set[str]
    fn_terms: Set[str]


def normalize_term(term: str) -> str:
    """
    Normalize a term by:
    - Lowercasing
    - Removing whitespace and special characters
    - Canonicalizing naming conventions (camelCase, snake_case, etc.)
    
    Args:
        term: The term to normalize
        
    Returns:
        Normalized term string
    """
    if not term:
        return ""
    
    # Remove leading/trailing whitespace
    term = term.strip()
    
    # Remove special characters except underscores (temporarily keep for snake_case detection)
    term = re.sub(r'[^\w\s]', '', term)
    
    # Convert to lowercase
    term = term.lower()
    
    # Remove all whitespace
    term = re.sub(r'\s+', '', term)
    
    # Canonicalize by removing underscores (converts snake_case to a standard form)
    term = term.replace('_', '')
    
    return term


def extract_terms_from_csv(file_path: Path) -> Set[str]:
    """
    Extract and normalize terms from a CSV file.
    
    Handles multiple column naming conventions:
    - 'Term', 'term', 'TERM'
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        Set of normalized term strings
    """
    terms = set()
    
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        
        # Find the term column (case-insensitive)
        term_column = None
        if reader.fieldnames:
            for col in reader.fieldnames:
                if col.lower().strip() == 'term':
                    term_column = col
                    break
        
        if term_column is None:
            raise ValueError(f"Could not find 'term' column in {file_path}. "
                           f"Available columns: {reader.fieldnames}")
        
        for row in reader:
            term = row.get(term_column, '').strip()
            if term:
                normalized = normalize_term(term)
                if normalized:
                    terms.add(normalized)
    
    return terms


def extract_terms_with_original(file_path: Path) -> Dict[str, str]:
    """
    Extract terms from a CSV file, returning a mapping from normalized to original.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        Dictionary mapping normalized term to original term
    """
    terms = {}
    
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        
        # Find the term column (case-insensitive)
        term_column = None
        if reader.fieldnames:
            for col in reader.fieldnames:
                if col.lower().strip() == 'term':
                    term_column = col
                    break
        
        if term_column is None:
            raise ValueError(f"Could not find 'term' column in {file_path}. "
                           f"Available columns: {reader.fieldnames}")
        
        for row in reader:
            term = row.get(term_column, '').strip()
            if term:
                normalized = normalize_term(term)
                if normalized:
                    terms[normalized] = term
    
    return terms


def calculate_metrics(reference: Set[str], evaluated: Set[str],
                     reference_original: Dict[str, str] = None,
                     evaluated_original: Dict[str, str] = None) -> MetricResult:
    """
    Calculate precision, recall, and F1-score for a set of terms.
    
    Args:
        reference: Reference set (ground truth) - normalized terms
        evaluated: Evaluated set (model being tested) - normalized terms
        reference_original: Optional mapping to original terms for reference
        evaluated_original: Optional mapping to original terms for evaluated
        
    Returns:
        MetricResult with calculated metrics
    """
    tp_normalized = reference & evaluated  # True Positives
    fp_normalized = evaluated - reference  # False Positives
    fn_normalized = reference - evaluated  # False Negatives
    
    # Map back to original terms if mappings provided
    if reference_original and evaluated_original:
        tp_terms = {evaluated_original.get(t, t) for t in tp_normalized}
        fp_terms = {evaluated_original.get(t, t) for t in fp_normalized}
        fn_terms = {reference_original.get(t, t) for t in fn_normalized}
    else:
        tp_terms = tp_normalized
        fp_terms = fp_normalized
        fn_terms = fn_normalized
    
    tp = len(tp_normalized)
    fp = len(fp_normalized)
    fn = len(fn_normalized)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return MetricResult(
        precision=precision,
        recall=recall,
        f1_score=f1_score,
        true_positives=tp,
        false_positives=fp,
        false_negatives=fn,
        tp_terms=tp_terms,
        fp_terms=fp_terms,
        fn_terms=fn_terms
    )


def compare_csv_files(reference_path: Path, model_path: Path, 
                      file_type: str = "terms") -> Dict:
    """
    Compare two CSV files and calculate metrics.
    
    Args:
        reference_path: Path to the reference CSV file
        model_path: Path to the model CSV file
        file_type: Label for this comparison (e.g., "terms", "scored_terms")
        
    Returns:
        Dictionary containing comparison results
    """
    # Extract terms with original mappings
    reference_original = extract_terms_with_original(reference_path)
    model_original = extract_terms_with_original(model_path)
    
    reference_terms = set(reference_original.keys())
    model_terms = set(model_original.keys())
    
    # Calculate metrics
    metrics = calculate_metrics(
        reference_terms, 
        model_terms,
        reference_original,
        model_original
    )
    
    return {
        "file_type": file_type,
        "reference_path": str(reference_path),
        "model_path": str(model_path),
        "reference_count": len(reference_terms),
        "model_count": len(model_terms),
        "metrics": {
            "precision": round(metrics.precision, 4),
            "recall": round(metrics.recall, 4),
            "f1_score": round(metrics.f1_score, 4),
            "true_positives": metrics.true_positives,
            "false_positives": metrics.false_positives,
            "false_negatives": metrics.false_negatives
        },
        "details": {
            "matched_terms": sorted(metrics.tp_terms),
            "false_positives": sorted(metrics.fp_terms),
            "false_negatives": sorted(metrics.fn_terms)
        }
    }


def format_results(results: Dict) -> str:
    """Format comparison results for console output."""
    output_lines = []
    
    output_lines.append("=" * 70)
    output_lines.append("TERMS CSV COMPARISON RESULTS")
    output_lines.append("=" * 70)
    
    for comparison in results.get("comparisons", []):
        output_lines.append(f"\n--- {comparison['file_type'].upper()} ---")
        output_lines.append(f"Reference: {comparison['reference_path']}")
        output_lines.append(f"Model:     {comparison['model_path']}")
        output_lines.append(f"\nCounts:")
        output_lines.append(f"  Reference terms: {comparison['reference_count']}")
        output_lines.append(f"  Model terms:     {comparison['model_count']}")
        
        metrics = comparison["metrics"]
        output_lines.append(f"\nMetrics:")
        output_lines.append(f"  Precision: {metrics['precision']:.4f}")
        output_lines.append(f"  Recall:    {metrics['recall']:.4f}")
        output_lines.append(f"  F1-Score:  {metrics['f1_score']:.4f}")
        output_lines.append(f"\n  True Positives:  {metrics['true_positives']}")
        output_lines.append(f"  False Positives: {metrics['false_positives']}")
        output_lines.append(f"  False Negatives: {metrics['false_negatives']}")
        
        details = comparison["details"]
        output_lines.append(f"\nMatched Terms ({len(details['matched_terms'])}):")
        for term in details["matched_terms"]:
            output_lines.append(f"  + {term}")
        
        output_lines.append(f"\nFalse Positives - in model but not in reference ({len(details['false_positives'])}):")
        for term in details["false_positives"]:
            output_lines.append(f"  - {term}")
        
        output_lines.append(f"\nFalse Negatives - in reference but not in model ({len(details['false_negatives'])}):")
        for term in details["false_negatives"]:
            output_lines.append(f"  ! {term}")
    
    output_lines.append("\n" + "=" * 70)
    
    return "\n".join(output_lines)


def main():
    parser = argparse.ArgumentParser(
        description="Compare terms from CSV files and calculate precision, recall, and F1-score."
    )
    parser.add_argument(
        "reference_terms",
        type=Path,
        help="Path to the reference terms.csv file (ground truth)"
    )
    parser.add_argument(
        "model_terms",
        type=Path,
        help="Path to the model's terms.csv file to evaluate"
    )
    parser.add_argument(
        "--scored-reference",
        type=Path,
        help="Path to the reference scored_terms.csv file (optional)"
    )
    parser.add_argument(
        "--scored-model",
        type=Path,
        help="Path to the model's scored_terms.csv file (optional)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output file path for JSON results (optional)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON to stdout"
    )
    
    args = parser.parse_args()
    
    # Validate input files
    if not args.reference_terms.exists():
        print(f"Error: Reference terms file not found: {args.reference_terms}")
        return 1
    if not args.model_terms.exists():
        print(f"Error: Model terms file not found: {args.model_terms}")
        return 1
    
    results = {"comparisons": []}
    
    # Compare terms.csv files
    terms_comparison = compare_csv_files(
        args.reference_terms, 
        args.model_terms, 
        "terms"
    )
    results["comparisons"].append(terms_comparison)
    
    # Compare scored_terms.csv files if provided
    if args.scored_reference and args.scored_model:
        if not args.scored_reference.exists():
            print(f"Error: Scored reference file not found: {args.scored_reference}")
            return 1
        if not args.scored_model.exists():
            print(f"Error: Scored model file not found: {args.scored_model}")
            return 1
        
        scored_comparison = compare_csv_files(
            args.scored_reference,
            args.scored_model,
            "scored_terms"
        )
        results["comparisons"].append(scored_comparison)
    
    # Output results
    if args.json:
        # Convert sets to lists for JSON serialization
        for comparison in results["comparisons"]:
            comparison["details"]["matched_terms"] = list(comparison["details"]["matched_terms"])
            comparison["details"]["false_positives"] = list(comparison["details"]["false_positives"])
            comparison["details"]["false_negatives"] = list(comparison["details"]["false_negatives"])
        print(json.dumps(results, indent=2))
    else:
        print(format_results(results))
    
    # Save to file if requested
    if args.output:
        # Convert sets to lists for JSON serialization
        for comparison in results["comparisons"]:
            if isinstance(comparison["details"]["matched_terms"], set):
                comparison["details"]["matched_terms"] = sorted(comparison["details"]["matched_terms"])
            if isinstance(comparison["details"]["false_positives"], set):
                comparison["details"]["false_positives"] = sorted(comparison["details"]["false_positives"])
            if isinstance(comparison["details"]["false_negatives"], set):
                comparison["details"]["false_negatives"] = sorted(comparison["details"]["false_negatives"])
        
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, indent=2, fp=f)
        print(f"\nResults saved to: {args.output}")
    
    return 0


if __name__ == "__main__":
    exit(main())
