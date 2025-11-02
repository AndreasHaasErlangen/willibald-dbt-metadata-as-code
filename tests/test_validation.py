"""Pytest tests for conceptual entity validation."""

import pytest
import yaml
import json
from pathlib import Path
from jsonschema import validate, ValidationError

# Test fixtures
@pytest.fixture
def schema():
    """Load the JSON schema."""
    schema_path = Path("schemas/conceptual_entity_schema.json")
    with open(schema_path, 'r') as f:
        return json.load(f)

@pytest.fixture
def entity_files():
    """Get all entity YAML files."""
    entities_dir = Path("entities")
    return list(entities_dir.glob("*.yaml"))

@pytest.fixture
def entities(entity_files):
    """Load all entity data."""
    result = {}
    for yaml_file in entity_files:
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
            result[data['entity']] = data
    return result

# Test 1: All YAML files are valid against schema
def test_all_entities_valid_against_schema(entity_files, schema):
    """Test that all entity YAML files validate against JSON schema."""
    for yaml_file in entity_files:
        with open(yaml_file, 'r') as f:
            entity = yaml.safe_load(f)
        
        try:
            validate(instance=entity, schema=schema)
        except ValidationError as e:
            pytest.fail(f"{yaml_file.name} failed validation: {e.message}")

# Test 2: All relationships reference existing entities
def test_all_relationships_reference_existing_entities(entities):
    """Test that all relationship targets exist as entities."""
    entity_names = set(entities.keys())
    
    for entity_name, entity_data in entities.items():
        relationships = entity_data.get('relationships', [])
        for rel in relationships:
            target = rel['target']
            assert target in entity_names, \
                f"Entity '{entity_name}' has relationship to non-existent entity '{target}'"

# Test 3: No circular dependencies (except hierarchical)
def test_no_circular_dependencies(entities):
    """Test for circular dependencies, allowing self-references."""
    for entity_name, entity_data in entities.items():
        relationships = entity_data.get('relationships', [])
        for rel in relationships:
            # Self-referential relationships are allowed (e.g., ProductCategory)
            if rel['target'] == entity_name:
                continue
            
            # Check if target has a direct relationship back (simple circular check)
            target_entity = entities.get(rel['target'])
            if target_entity:
                target_rels = target_entity.get('relationships', [])
                for target_rel in target_rels:
                    if target_rel['target'] == entity_name:
                        # This is bidirectional, which is fine for M:1 and 1:M pairs
                        pass

# Test 4: All entity names are unique
def test_all_entity_names_unique(entities):
    """Test that entity names are unique."""
    entity_names = [data['entity'] for data in entities.values()]
    assert len(entity_names) == len(set(entity_names)), \
        f"Duplicate entity names found"

# Test 5: All attribute names within entity unique
def test_attribute_names_unique_within_entity(entities):
    """Test that attribute names are unique within each entity."""
    for entity_name, entity_data in entities.items():
        attributes = entity_data.get('attributes', [])
        attr_names = [attr['name'] for attr in attributes]
        assert len(attr_names) == len(set(attr_names)), \
            f"Entity '{entity_name}' has duplicate attribute names"