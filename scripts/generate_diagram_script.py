#!/usr/bin/env python3
"""Generate Mermaid ER diagram from conceptual entity YAML files."""

import yaml
from pathlib import Path

def generate_mermaid_diagram():
    """Parse entity YAMLs and generate Mermaid ER diagram."""
    entities_dir = Path("entities")
    output_file = Path("docs/entity_diagram.md")
    
    # Load all entities
    entities = {}
    relationships = []
    
    yaml_files = sorted(entities_dir.glob("*.yaml"))
    
    for yaml_file in yaml_files:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            entity_data = yaml.safe_load(f)
        
        entity_name = entity_data['entity']
        entities[entity_name] = {
            'description': entity_data.get('description', ''),
            'attributes': entity_data.get('attributes', [])
        }
        
        # Collect relationships
        for rel in entity_data.get('relationships', []):
            relationships.append({
                'from': entity_name,
                'to': rel['target'],
                'type': rel['type'],
                'name': rel['name']
            })
    
    # Generate Mermaid diagram
    diagram_lines = [
        "# Willibald Conceptual Entity Diagram",
        "",
        "## Business Entity Relationships",
        "",
        "```mermaid",
        "erDiagram"
    ]
    
    # Add entities with attributes
    for entity_name, entity_info in sorted(entities.items()):
        diagram_lines.append(f"    {entity_name} {{")
        for attr in entity_info['attributes'][:5]:  # Limit to first 5 attributes
            attr_type = attr.get('type', 'string')
            diagram_lines.append(f"        {attr_type} {attr['name']}")
        if len(entity_info['attributes']) > 5:
            diagram_lines.append(f"        ... more_attributes")
        diagram_lines.append("    }")
    
    diagram_lines.append("")
    
    # Add relationships with cardinality
    cardinality_map = {
        '1:1': '||--||',
        '1:M': '||--o{',
        'M:1': '}o--||',
        'M:M': '}o--o{'
    }
    
    for rel in relationships:
        mermaid_rel = cardinality_map.get(rel['type'], '||--||')
        diagram_lines.append(f"    {rel['from']} {mermaid_rel} {rel['to']} : {rel['name']}")
    
    diagram_lines.append("```")
    diagram_lines.append("")
    diagram_lines.append("## Entity Descriptions")
    diagram_lines.append("")
    
    for entity_name, entity_info in sorted(entities.items()):
        diagram_lines.append(f"### {entity_name}")
        diagram_lines.append(f"{entity_info['description']}")
        diagram_lines.append("")
    
    # Write to file
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(diagram_lines))
    
    print(f"✓ Generated Mermaid diagram: {output_file}")
    print(f"  - {len(entities)} entities")
    print(f"  - {len(relationships)} relationships")

if __name__ == "__main__":
    generate_mermaid_diagram()