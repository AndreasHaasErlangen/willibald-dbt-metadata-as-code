# Conceptual Models Repository
## Willibald Data Vault - Business Entity Layer

**Version:** 1.0  
**Date:** November 2025  
**Purpose:** Business-friendly entity definitions for the Willibald seed shop Data Vault implementation

---

## Overview

This repository contains conceptual models for all business entities in the Willibald challenge. These models are:

- **Technology-agnostic**: No database or implementation details
- **Business-friendly**: Understandable by domain experts
- **Validated**: JSON Schema ensures consistency
- **Foundation for automation**: Used to generate logical Data Vault models

## Repository Structure

```
conceptual-models/
├── README.md                    # This file
├── .gitignore
├── requirements.txt
├── schemas/
│   └── conceptual_entity_schema.json  # Validation schema
├── entities/                    # 10 business entity definitions
│   ├── customer.yaml
│   ├── order.yaml
│   ├── order_item.yaml
│   ├── product.yaml
│   ├── product_category.yaml
│   ├── delivery.yaml
│   ├── delivery_address.yaml
│   ├── club_partner.yaml
│   ├── residence.yaml
│   └── category_adherence.yaml
├── scripts/
│   ├── validate_all.py         # Validate all entities
│   └── generate_diagram.py     # Create ER diagram
├── docs/
│   ├── entity_overview.md
│   └── relationship_matrix.md
└── tests/
    └── test_validation.py
```

## Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

### Validate All Entities

```bash
python scripts/validate_all.py
```

### Generate ER Diagram

```bash
python scripts/generate_diagram.py
```

### Run Tests

```bash
pytest tests/
```

## Entity Overview

| Entity | Description | Key Patterns |
|--------|-------------|--------------|
| Customer | Individuals purchasing seeds/plants | Multi-source |
| Order | Purchase transactions | Multi-source |
| OrderItem | Individual order line items | Standard |
| Product | Catalog items | Standard |
| ProductCategory | Hierarchical product classification | Self-referential |
| Delivery | Shipment tracking | Standard |
| DeliveryAddress | Customer shipping addresses | Standard |
| ClubPartner | Club membership affiliations | Standard |
| Residence | Customer address history | Multi-active |
| CategoryAdherence | Delivery performance reference | Reference data |

## Usage Guidelines

### Adding a New Entity

1. Copy an existing entity YAML as template
2. Follow naming conventions (PascalCase for entities/attributes)
3. Define relationships according to ownership rules
4. Add normalization hints for special patterns
5. Validate: `python scripts/validate_all.py`

### Modifying an Entity

1. Edit the YAML file in `entities/`
2. Maintain business-friendly language
3. Update relationships in both entities if needed
4. Validate changes
5. Update documentation if adding new patterns

### Relationship Ownership Rules

- **1:M relationships**: Define in the "1" side entity
- **M:M relationships**: Define in primary actor entity
- **1:1 relationships**: Define in dependent entity
- **Self-referential**: Define both directions explicitly

## Validation

The JSON Schema enforces:
- Required fields: layer, entity, description
- Naming conventions (PascalCase entities, snake_case relationships)
- Valid relationship types (1:1, 1:M, M:1, M:M)
- Minimum description lengths
- Unique attribute names within entities

## Contributing

This repository serves as the business layer foundation. Changes should:
1. Maintain business-focused language (no technical jargon)
2. Be validated against the schema
3. Include clear descriptions
4. Consider downstream impacts on logical models

## Next Steps

Once conceptual models are complete and validated:
1. Generate logical Data Vault models (Phase 3)
2. Create Python generator for SQL code
3. Implement in dbt with datavault4dbt

## Contact

For questions about business entities, consult domain experts.  
For technical implementation, see the `willibald-metadata-driven` repository.

---

**Last Updated:** November 2025