#!/usr/bin/env python3
"""Validate all conceptual entity YAML files against JSON Schema."""

import sys
import yaml
import json
from pathlib import Path
from jsonschema import validate, ValidationError

def validate_entities():
    """Validate all entity YAML files against the JSON Schema."""
    schema_path = Path("schemas/conceptual_entity_schema.json")
    entities_dir = Path("entities")
    
    # Load schema
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        print(f"✓ Loaded schema from {schema_path}")
    except FileNotFoundError:
        print(f"✗ Schema file not found: {schema_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON in schema: {e}")
        sys.exit(1)
    
    # Find all YAML files
    yaml_files = sorted(entities_dir.glob("*.yaml"))
    if not yaml_files:
        print(f"✗ No YAML files found in {entities_dir}")
        sys.exit(1)
    
    print(f"\nValidating {len(yaml_files)} entity files...\n")
    
    errors = []
    valid_count = 0
    
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                entity = yaml.safe_load(f)
            
            # Validate against schema
            validate(instance=entity, schema=schema)
            print(f"✓ {yaml_file.name:30s} - Valid")
            valid_count += 1
            
        except yaml.YAMLError as e:
            errors.append(f"✗ {yaml_file.name}: YAML parsing error - {e}")
        except ValidationError as e:
            errors.append(f"✗ {yaml_file.name}: {e.message}")
        except Exception as e:
            errors.append(f"✗ {yaml_file.name}: Unexpected error - {e}")
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Validation Summary: {valid_count}/{len(yaml_files)} files valid")
    print(f"{'='*60}")
    
    if errors:
        print(f"\n❌ Validation errors found:\n")
        for error in errors:
            print(f"  {error}")
        sys.exit(1)
    else:
        print(f"\n✅ All entities are valid!\n")
        sys.exit(0)

if __name__ == "__main__":
    validate_entities()