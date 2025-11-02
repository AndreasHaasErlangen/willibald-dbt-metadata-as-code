# Entity Relationship Matrix

## Complete Relationship Overview

| From Entity | To Entity | Type | Relationship Name | Description |
|-------------|-----------|------|-------------------|-------------|
| Customer | Order | 1:M | places_orders | Customer can place multiple orders over time |
| Customer | Residence | 1:M | has_residences | Customer may have lived at multiple addresses |
| Customer | ClubPartner | M:1 | member_of_club | Customer may be member of partner club |
| Order | OrderItem | 1:M | contains_items | Order consists of one or more line items |
| Order | Delivery | 1:M | results_in_deliveries | Order may be fulfilled through multiple deliveries |
| Product | OrderItem | 1:M | appears_in_items | Product can appear in multiple order items |
| ProductCategory | ProductCategory | M:1 | has_parent | Category may have one parent category |
| ProductCategory | ProductCategory | 1:M | has_children | Category may contain multiple child subcategories |
| ProductCategory | Product | 1:M | contains_products | Category groups multiple products |
| DeliveryAddress | Delivery | 1:M | receives_deliveries | Address can receive multiple deliveries |
| ClubPartner | Customer | 1:M | has_members | Club can have multiple customer members |

## Relationship Types Breakdown

### One-to-Many (1:M) - 9 relationships
Represents parent-child relationships where one parent can have multiple children:
- Customer → Order (customer's order history)
- Customer → Residence (customer's address history)
- Order → OrderItem (order's line items)
- Order → Delivery (order's shipments)
- Product → OrderItem (product's order appearances)
- ProductCategory → Product (category's products)
- ProductCategory → ProductCategory (parent's subcategories)
- DeliveryAddress → Delivery (address's delivery history)
- ClubPartner → Customer (club's members)

### Many-to-One (M:1) - 2 relationships
Represents child-to-parent relationships:
- Customer → ClubPartner (customer's club membership)
- ProductCategory → ProductCategory (subcategory's parent)

### Many-to-Many (M:M) - 0 relationships
No direct M:M relationships in this model. Potential M:M relationships are resolved through junction entities:
- Product ←→ Order resolved through OrderItem

### One-to-One (1:1) - 0 relationships
No 1:1 relationships in this model.

## Relationship Patterns

### Standard Parent-Child
Most relationships follow standard parent-child patterns suitable for Links in Data Vault.

### Self-Referential (Hierarchical)
**ProductCategory → ProductCategory**
- Special case: entity relates to itself
- Creates tree structure (taxonomy)
- Requires hierarchical link in Data Vault
- Example path: Seeds → Vegetable Seeds → Tomato Seeds

### Multi-Active Temporal
**Customer → Residence**
- One-to-many with temporal validity
- Multiple residences can be active at different time periods
- Requires multi-active satellite in Data Vault
- FromDate and ToDate define validity periods

### Optional Relationships
Several relationships are optional (nullable foreign keys):
- Customer → ClubPartner (not all customers are club members)
- ProductCategory → ProductCategory (root categories have no parent)
- Residence.ToDate (current residence has no end date)

## Entity Connectivity Analysis

### Highly Connected Entities (Hub Candidates)
1. **Customer** (3 outgoing): Central to business, connects to orders, residences, clubs
2. **Order** (2 outgoing): Links customers to products and deliveries
3. **ProductCategory** (2 outgoing + self): Organizes products hierarchically
4. **Product** (1 outgoing): Connects categories to orders

### Weakly Connected Entities
1. **Residence** (0 outgoing): Leaf entity, only connected as child
2. **OrderItem** (0 outgoing): Junction entity between Order and Product
3. **Delivery** (0 outgoing): Leaf entity for shipment tracking
4. **CategoryAdherence** (0 outgoing): Standalone reference table

### Isolated Entities (No Relationships Defined)
- **CategoryAdherence**: Reference/lookup table with no formal relationships
  - Note: In reality, would be referenced by Delivery for adherence classification

## Data Vault Mapping Considerations

### Hub Entities (Business Keys)
- Customer (CustomerId)
- Order (OrderId)
- OrderItem (OrderItemId)
- Product (ProductId)
- ProductCategory (CategoryId)
- Delivery (DeliveryId)
- DeliveryAddress (AddressId)
- ClubPartner (ClubPartnerId)
- Residence (ResidenceId)
- CategoryAdherence (CategoryId) - Reference Hub

### Link Entities (Relationships)
- Customer-Order Link
- Customer-Residence Link (with effectivity)
- Customer-ClubPartner Link
- Order-OrderItem Link
- Order-Delivery Link
- Product-OrderItem Link
- ProductCategory-Product Link
- ProductCategory-ProductCategory Link (hierarchical)
- DeliveryAddress-Delivery Link

### Satellite Candidates
All descriptive attributes from each entity become satellites attached to their respective hubs.

## Cardinality Notes

### Why 1:M Defined in Parent
Following the ownership rule, 1:M relationships are defined in the "1" (parent) side because:
- Parent controls the relationship
- Parent exists independently
- Children depend on parent for context
- Avoids relationship duplication

### Bidirectional Consistency
When a relationship is defined in one entity, the inverse should NOT be defined in the target entity:
- ✓ Customer defines `places_orders` (1:M to Order)
- ✗ Order should NOT define `placed_by` (M:1 to Customer)

This prevents duplicate relationship definitions and maintains single source of truth.

## Special Patterns Summary

| Pattern | Entities | Data Vault Impact |
|---------|----------|-------------------|
| Hierarchical | ProductCategory | Hierarchical Link structure |
| Multi-Active | Customer-Residence | Multi-active Satellite with dates |
| Multi-Source | Customer, Order | Union in staging, merge in Hub |
| Reference | CategoryAdherence | Reference Hub, no relationships |
| Optional | Multiple | Nullable foreign keys in Links |

---

**Document Version**: 1.0  
**Last Updated**: November 2025