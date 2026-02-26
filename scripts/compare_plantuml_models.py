"""
PlantUML Model Comparison Script

Compares PlantUML class diagrams by extracting and normalizing classes, relationships,
and attributes, then computing precision, recall, and F1-score metrics.

Usage:
    python compare_plantuml_models.py <reference.puml> <model1.puml> <model2.puml> [--output results.json]
"""

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Tuple


@dataclass
class ModelElements:
    """Holds extracted elements from a PlantUML model."""
    classes: Set[str] = field(default_factory=set)
    relationships: Set[Tuple[str, str, str]] = field(default_factory=set) 
    attributes: Set[Tuple[str, str]] = field(default_factory=set)


@dataclass
class MetricResult:
    """Holds precision, recall, and F1 metrics."""
    precision: float
    recall: float
    f1_score: float
    true_positives: int
    false_positives: int
    false_negatives: int


def normalize_identifier(identifier: str) -> str:
    """
    Normalize an identifier by:
    - Lowercasing
    - Removing whitespace and special characters
    - Canonicalizing naming conventions (camelCase, snake_case, etc.)
    
    Args:
        identifier: The identifier to normalize
        
    Returns:
        Normalized identifier string
    """
    if not identifier:
        return ""
    
    # Remove leading/trailing whitespace
    identifier = identifier.strip()
    
    # Remove special characters except underscores (keep for snake_case detection)
    identifier = re.sub(r'[^\w\s]', '', identifier)
    
    # Convert to lowercase
    identifier = identifier.lower()
    
    # Remove all whitespace
    identifier = re.sub(r'\s+', '', identifier)
    
    # Canonicalize by removing underscores (converts snake_case to a standard form)
    identifier = identifier.replace('_', '')
    
    return identifier


def parse_plantuml_file(file_path: Path) -> ModelElements:
    """
    Parse a PlantUML file and extract classes, relationships, and attributes.
    
    Args:
        file_path: Path to the PlantUML file
        
    Returns:
        ModelElements containing extracted and normalized elements
    """
    elements = ModelElements()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove comments
    content = re.sub(r"'.*?$", '', content, flags=re.MULTILINE)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    
    # Extract classes (considering various PlantUML syntaxes)
    # Match: class ClassName, abstract class ClassName, interface ClassName, enum ClassName
    # Also handles: class "Quoted Name" as Alias, class Name as Alias, class "Quoted Name"
    # Group 1: quoted name (optional)
    # Group 2: simple/qualified name (optional)
    # Group 3: alias (optional)
    class_pattern = r'(?:class|abstract\s+class|interface|enum)\s+(?:"([^"]+)"|([\w.]+))(?:\s+as\s+(\w+))?'
    
    for match in re.finditer(class_pattern, content, re.IGNORECASE):
        quoted_name = match.group(1)
        simple_name = match.group(2)
        
        # Determine the raw class name (without namespace prefix)
        raw_name = quoted_name if quoted_name else simple_name
        
        # Extract just the class name (last part if qualified)
        simple_class_name = raw_name.split('.')[-1] if '.' in raw_name else raw_name
        
        # Normalize the simple class name for storage (ignoring package hierarchy)
        normalized_class = normalize_identifier(simple_class_name)
        
        if normalized_class:
            elements.classes.add(normalized_class)
    
    # Extract relationships (various types)
    # Patterns: ClassA --> ClassB, ClassA -- ClassB, ClassA -|> ClassB, etc.
    # Optional cardinality: ClassA "1" *-- "1..*" ClassB : label
    # CARD matches optional quoted cardinality like "1" or "1..*"
    CARD = r'(?:\s*"[^"]*")?'  # optional cardinality e.g. "1", "1..*", "0..1"
    LABEL = r'(?:\s*:\s*[^\n]+)?'  # optional label e.g. ": uses"
    # CLASS matches either a quoted name or a simple/qualified identifier
    CLASS = r'(?:"([^"]+)"|([\w.]+))'
    
    # Each pattern tuple: (regex, relationship_type, is_reverse)
    # is_reverse=True means the arrow points left, so source/target must be swapped
    # Example: A <|-- B means B inherits from A, so source=B, target=A
    relationship_patterns = [
        (rf'{CLASS}{CARD}\s*(<\|--){CARD}\s*{CLASS}{LABEL}', 'inheritance', True),   # inheritance (reverse)
        (rf'{CLASS}{CARD}\s*(--\|>){CARD}\s*{CLASS}{LABEL}', 'inheritance', False),  # inheritance
        (rf'{CLASS}{CARD}\s*(<\|\.\.){CARD}\s*{CLASS}{LABEL}', 'realization', True), # realization (reverse)
        (rf'{CLASS}{CARD}\s*(\.\.\|>){CARD}\s*{CLASS}{LABEL}', 'realization', False), # realization
        (rf'{CLASS}{CARD}\s*(\*--){CARD}\s*{CLASS}{LABEL}', 'composition', True),    # composition (diamond on left)
        (rf'{CLASS}{CARD}\s*(--\*){CARD}\s*{CLASS}{LABEL}', 'composition', False),   # composition (diamond on right)
        (rf'{CLASS}{CARD}\s*(o--){CARD}\s*{CLASS}{LABEL}', 'aggregation', True),     # aggregation (diamond on left)
        (rf'{CLASS}{CARD}\s*(--o){CARD}\s*{CLASS}{LABEL}', 'aggregation', False),    # aggregation (diamond on right)
        (rf'{CLASS}{CARD}\s*(-->){CARD}\s*{CLASS}{LABEL}', 'association', False),    # directed association
        (rf'{CLASS}{CARD}\s*(<--){CARD}\s*{CLASS}{LABEL}', 'association', True),     # directed association (reverse)
        (rf'{CLASS}{CARD}\s*((?<![<|*o])--(?![>|*o])){CARD}\s*{CLASS}{LABEL}', 'association', False),  # association (undirected, exclude special arrows)
        (rf'{CLASS}{CARD}\s*(\.\.>){CARD}\s*{CLASS}{LABEL}', 'dependency', False),   # dependency
        (rf'{CLASS}{CARD}\s*(<\.\.){CARD}\s*{CLASS}{LABEL}', 'dependency', True),    # dependency (reverse)
    ]
    
    for pattern, rel_type, is_reverse in relationship_patterns:
        for match in re.finditer(pattern, content):
            # CLASS pattern has 2 groups: (quoted_name, simple_name)
            # Left class is groups 1,2; operator is group 3; right class is groups 4,5
            left_quoted = match.group(1)
            left_simple = match.group(2)
            right_quoted = match.group(4)
            right_simple = match.group(5)
            
            left_name = left_quoted if left_quoted else left_simple
            right_name = right_quoted if right_quoted else right_simple
            
            # Extract just the class name (last part if qualified), ignoring package
            left = normalize_identifier(left_name.split('.')[-1] if '.' in left_name else left_name)
            right = normalize_identifier(right_name.split('.')[-1] if '.' in right_name else right_name)
            
            if left and right:
                # Swap source/target for reverse arrows to normalize direction
                if is_reverse:
                    source, target = right, left
                else:
                    source, target = left, right
                # Normalize relationship type
                normalized_rel = normalize_identifier(rel_type)
                elements.relationships.add((source, normalized_rel, target))
    
    # Extract attributes from class definitions
    # Pattern: class ClassName { attribute_name }
    # Handles: class Name, class "Quoted Name", class qualified.Name
    class_def_pattern = r'(?:class|abstract\s+class|interface)\s+(?:"([^"]+)"|([\w.]+))(?:\s+as\s+(\w+))?\s*\{([^}]*)\}'
    for match in re.finditer(class_def_pattern, content, re.IGNORECASE | re.DOTALL):
        quoted_name = match.group(1)
        simple_name = match.group(2)
        alias = match.group(3)
        attributes_block = match.group(4)
        
        # Get the simple class name (ignore package hierarchy)
        if alias:
            raw_name = alias
        elif quoted_name:
            raw_name = quoted_name
        else:
            raw_name = simple_name
        
        # Extract just the class name (last part if qualified)
        simple_class_name = raw_name.split('.')[-1] if '.' in raw_name else raw_name
        class_name = normalize_identifier(simple_class_name)
        
        # Process each line separately to avoid matching type names or method parts
        for line in attributes_block.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Remove inline comments (PlantUML uses ' for comments)
            line = re.sub(r"'.*$", '', line).strip()
            if not line:
                continue
            
            # Skip methods (lines containing parentheses)
            if '(' in line:
                continue
            
            # Skip stereotypes/modifiers like {abstract}, {static}, {field}, etc.
            if re.match(r'^\{.*\}$', line):
                continue
            
            # Skip annotation lines (starting with @)
            if line.startswith('@'):
                continue
            
            # Skip separator lines (-- or ==)
            if re.match(r'^[-=]+$', line):
                continue
            
            # Remove leading stereotype/modifier like {static} or {abstract}
            line = re.sub(r'\{[^}]+\}\s*', '', line).strip()
            if not line:
                continue
            
            # Match attribute pattern: [visibility] name : type [= default]
            # visibility: +, -, #, ~
            # Anchored regex to only capture the attribute name, not type names
            attr_match = re.match(r'^[+\-#~]?\s*(\w+)\s*(?::\s*.+)?(?:\s*=\s*.+)?$', line)
            if attr_match:
                attr_name = attr_match.group(1).strip()
                
                # Skip if the "attribute" is actually a modifier keyword
                if attr_name.lower() in ('static', 'abstract', 'final', 'const', 'readonly', 'virtual', 'override'):
                    continue
                
                normalized_attr = normalize_identifier(attr_name)
                if normalized_attr and class_name:
                    elements.attributes.add((class_name, normalized_attr))
    
    return elements


def calculate_metrics(reference: Set, evaluated: Set) -> MetricResult:
    """
    Calculate precision, recall, and F1-score for a set of elements.
    
    Args:
        reference: Reference set (ground truth)
        evaluated: Evaluated set (model being tested)
        
    Returns:
        MetricResult with calculated metrics
    """
    tp = len(reference & evaluated)  # True Positives
    fp = len(evaluated - reference)  # False Positives
    fn = len(reference - evaluated)  # False Negatives
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return MetricResult(
        precision=precision,
        recall=recall,
        f1_score=f1_score,
        true_positives=tp,
        false_positives=fp,
        false_negatives=fn
    )


def compare_models(reference_path: Path, model_paths: List[Path]) -> Dict:
    """
    Compare multiple PlantUML models against a reference model.
    
    Args:
        reference_path: Path to the reference PlantUML model
        model_paths: List of paths to models to compare
        
    Returns:
        Dictionary containing comparison results
    """
    # Parse reference model
    reference = parse_plantuml_file(reference_path)
    
    results = {
        "reference_model": str(reference_path),
        "reference_stats": {
            "classes": len(reference.classes),
            "relationships": len(reference.relationships),
            "attributes": len(reference.attributes)
        },
        "comparisons": []
    }
    
    # Compare each model
    for model_path in model_paths:
        model = parse_plantuml_file(model_path)
        
        # Calculate metrics for each element type
        class_metrics = calculate_metrics(reference.classes, model.classes)
        relationship_metrics = calculate_metrics(reference.relationships, model.relationships)
        attribute_metrics = calculate_metrics(reference.attributes, model.attributes)
        
        # Calculate overall metrics (micro-average across all elements)
        all_reference = reference.classes | reference.relationships | reference.attributes
        all_model = model.classes | model.relationships | model.attributes
        overall_metrics = calculate_metrics(all_reference, all_model)
        
        comparison = {
            "model_path": str(model_path),
            "model_stats": {
                "classes": len(model.classes),
                "relationships": len(model.relationships),
                "attributes": len(model.attributes)
            },
            "metrics": {
                "classes": {
                    "precision": round(class_metrics.precision, 4),
                    "recall": round(class_metrics.recall, 4),
                    "f1_score": round(class_metrics.f1_score, 4),
                    "true_positives": class_metrics.true_positives,
                    "false_positives": class_metrics.false_positives,
                    "false_negatives": class_metrics.false_negatives
                },
                "relationships": {
                    "precision": round(relationship_metrics.precision, 4),
                    "recall": round(relationship_metrics.recall, 4),
                    "f1_score": round(relationship_metrics.f1_score, 4),
                    "true_positives": relationship_metrics.true_positives,
                    "false_positives": relationship_metrics.false_positives,
                    "false_negatives": relationship_metrics.false_negatives
                },
                "attributes": {
                    "precision": round(attribute_metrics.precision, 4),
                    "recall": round(attribute_metrics.recall, 4),
                    "f1_score": round(attribute_metrics.f1_score, 4),
                    "true_positives": attribute_metrics.true_positives,
                    "false_positives": attribute_metrics.false_positives,
                    "false_negatives": attribute_metrics.false_negatives
                },
                "overall": {
                    "precision": round(overall_metrics.precision, 4),
                    "recall": round(overall_metrics.recall, 4),
                    "f1_score": round(overall_metrics.f1_score, 4),
                    "true_positives": overall_metrics.true_positives,
                    "false_positives": overall_metrics.false_positives,
                    "false_negatives": overall_metrics.false_negatives
                }
            },
            "differences": {
                "missing_classes": sorted(list(reference.classes - model.classes)),
                "extra_classes": sorted(list(model.classes - reference.classes)),
                "missing_relationships": sorted([f"{s} -{t}-> {d}" for s, t, d in (reference.relationships - model.relationships)]),
                "extra_relationships": sorted([f"{s} -{t}-> {d}" for s, t, d in (model.relationships - reference.relationships)]),
                "missing_attributes": sorted([f"{c}.{a}" for c, a in (reference.attributes - model.attributes)]),
                "extra_attributes": sorted([f"{c}.{a}" for c, a in (model.attributes - reference.attributes)])
            }
        }
        
        results["comparisons"].append(comparison)
    
    return results


def print_results(results: Dict):
    """
    Print comparison results in a human-readable format.
    
    Args:
        results: Results dictionary from compare_models
    """
    print("=" * 80)
    print("PlantUML Model Comparison Results")
    print("=" * 80)
    print(f"\nReference Model: {results['reference_model']}")
    print(f"  Classes: {results['reference_stats']['classes']}")
    print(f"  Relationships: {results['reference_stats']['relationships']}")
    print(f"  Attributes: {results['reference_stats']['attributes']}")
    print()
    
    for i, comp in enumerate(results["comparisons"], 1):
        print("-" * 80)
        print(f"Model {i}: {comp['model_path']}")
        print("-" * 80)
        print(f"  Classes: {comp['model_stats']['classes']}")
        print(f"  Relationships: {comp['model_stats']['relationships']}")
        print(f"  Attributes: {comp['model_stats']['attributes']}")
        print()
        
        print("  Metrics:")
        print("  " + "-" * 76)
        print(f"  {'Element Type':<20} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
        print("  " + "-" * 76)
        
        for elem_type in ["classes", "relationships", "attributes", "overall"]:
            metrics = comp["metrics"][elem_type]
            print(f"  {elem_type.capitalize():<20} "
                  f"{metrics['precision']:<12.4f} "
                  f"{metrics['recall']:<12.4f} "
                  f"{metrics['f1_score']:<12.4f}")
        
        print("  " + "-" * 76)
        print()
        
        # Print differences summary
        diffs = comp["differences"]
        print("  Differences Summary:")
        print(f"    Missing Classes: {len(diffs['missing_classes'])}")
        print(f"    Extra Classes: {len(diffs['extra_classes'])}")
        print(f"    Missing Relationships: {len(diffs['missing_relationships'])}")
        print(f"    Extra Relationships: {len(diffs['extra_relationships'])}")
        print(f"    Missing Attributes: {len(diffs['missing_attributes'])}")
        print(f"    Extra Attributes: {len(diffs['extra_attributes'])}")
        print()


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Compare PlantUML class diagram models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
                Examples:
                # Compare two models against a reference
                python compare_plantuml_models.py reference.puml model1.puml model2.puml
                
                # Save results to JSON file
                python compare_plantuml_models.py reference.puml model1.puml model2.puml --output results.json
                
                # Compare models in the data folder
                python compare_plantuml_models.py data/reference.puml data/model1.puml data/model2.puml
        """
    )
    
    parser.add_argument(
        "reference",
        type=Path,
        help="Path to the reference PlantUML model (ground truth)"
    )
    
    parser.add_argument(
        "models",
        type=Path,
        nargs="+",
        help="Paths to PlantUML models to compare against the reference"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output JSON file path (optional)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed differences"
    )
    
    args = parser.parse_args()
    
    # Validate files exist
    if not args.reference.exists():
        print(f"Error: Reference file not found: {args.reference}")
        return 1
    
    for model_path in args.models:
        if not model_path.exists():
            print(f"Error: Model file not found: {model_path}")
            return 1
    
    # Run comparison
    print(f"Comparing {len(args.models)} model(s) against reference...")
    results = compare_models(args.reference, args.models)
    
    # Print results
    print_results(results)
    
    # Show detailed differences if verbose
    if args.verbose:
        for i, comp in enumerate(results["comparisons"], 1):
            print(f"\nDetailed Differences for Model {i}:")
            print("=" * 80)
            diffs = comp["differences"]
            
            if diffs["missing_classes"]:
                print(f"\nMissing Classes ({len(diffs['missing_classes'])}):")
                for cls in diffs["missing_classes"]:
                    print(f"  - {cls}")
            
            if diffs["extra_classes"]:
                print(f"\nExtra Classes ({len(diffs['extra_classes'])}):")
                for cls in diffs["extra_classes"]:
                    print(f"  + {cls}")
            
            if diffs["missing_relationships"]:
                print(f"\nMissing Relationships ({len(diffs['missing_relationships'])}):")
                for rel in diffs["missing_relationships"]:
                    print(f"  - {rel}")
            
            if diffs["extra_relationships"]:
                print(f"\nExtra Relationships ({len(diffs['extra_relationships'])}):")
                for rel in diffs["extra_relationships"]:
                    print(f"  + {rel}")
            
            if diffs["missing_attributes"]:
                print(f"\nMissing Attributes ({len(diffs['missing_attributes'])}):")
                for attr in diffs["missing_attributes"]:
                    print(f"  - {attr}")
            
            if diffs["extra_attributes"]:
                print(f"\nExtra Attributes ({len(diffs['extra_attributes'])}):")
                for attr in diffs["extra_attributes"]:
                    print(f"  + {attr}")
    
    # Save to JSON if requested
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")
    
    return 0


if __name__ == "__main__":
    exit(main())
