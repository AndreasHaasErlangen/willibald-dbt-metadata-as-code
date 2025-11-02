# Updated Entity YAML Files - Aligned with Willibald.json (Relationships Corrected)

Save each section below as a separate file in the `entities/` directory.

---

## File: entities/customer.yaml

```yaml
layer: conceptual
entity: Customer
description: "Individual or organization that purchases seeds, plants, and gardening products from the Willibald shop. Customers can place orders through webshop or roadshow channels, have delivery addresses, and may be members of partner associations. Historical residence information is tracked as multi-active attributes."

attributes:
  - name: customer_bk
    description: "Unique identifier for the customer (business key)"
    type: string
    example: "K12345"
    
  - name: Email
    description: "Primary contact email address for order confirmations"
    type: string
    example: "maria.schmidt@example.com"
    
  - name: Geburtsdatum
    description: "Customer birth date for demographics and marketing"
    type: date
    example: "1980-05-15"
    
  - name: Geschlecht
    description: "Customer gender"
    type: string
    example: "F"
    
  - name: GueltigBis
    description: "Credit card expiration date"
    type: date
    example: "2025-12-31"
    
  - name: KKFirma
    description: "Credit card company name"
    type: string
    example: "VISA"
    
  - name: Kreditkarte
    description: "Credit card number for payment"
    type: string
    example: "4111111111111111"
    
  - name: Mobil
    description: "Mobile phone number"
    type: string
    example: "+49 151 12345678"
    
  - name: Name
    description: "Customer last name or company name"
    type: string
    example: "Schmidt"
    
  - name: Telefon
    description: "Primary landline phone number"
    type: string
    example: "+49 9131 123456"
    
  - name: Vorname
    description: "Customer first name"
    type: string
    example: "Maria"
    
  - name: Von
    description: "Start date for multi-active residence period"
    type: date
    example: "2020-01-01"
    
  - name: Adresszusatz
    description: "Address supplement for residence (apartment, floor)"
    type: string
    example: "2. OG"
    
  - name: Bis
    description: "End date for multi-active residence period"
    type: date
    example: "2023-12-31"
    
  - name: Hausnummer
    description: "House number for residence"
    type: string
    example: "45"
    
  - name: Land
    description: "Country for residence"
    type: string
    example: "Deutschland"
    
  - name: Ort
    description: "City for residence"
    type: string
    example: "Erlangen"
    
  - name: Plz
    description: "Postal code for residence"
    type: string
    example: "91054"
    
  - name: Strasse
    description: "Street name for residence"
    type: string
    example: "Hauptstrasse"

relationships:
  - name: makes_a
    target: Order
    type: 1:M
    description: "Customer makes orders"
    
  - name: has_a
    target: DeliveryAddress
    type: 1:M
    description: "Customer has delivery addresses"
    
  - name: can_be_member_of
    target: AssociationPartner
    type: M:1
    description: "Customer can be member of association partner"

normalization_hints:
  multi_valued: 
    - Von
    - Adresszusatz
    - Bis
    - Hausnummer
    - Land
    - Ort
    - Plz
    - Strasse
  redundant: []
  constrained: 
    - Email
    - Geschlecht
    - Kreditkarte
```

---

## File: entities/association_partner.yaml

```yaml
layer: conceptual
entity: AssociationPartner
description: "Garden association or club that has a partnership agreement with Willibald. Members receive special discounts. The association is represented by a customer contact person."

attributes:
  - name: associationpartner_bk
    description: "Unique identifier for the partner association (business key)"
    type: string
    example: "VP001"
    
  - name: KundeIDVerein
    description: "Customer ID of the association's contact person"
    type: string
    example: "K12345"
    
  - name: Rabatt1
    description: "First discount rate tier for association members"
    type: decimal
    example: "10.0"
    
  - name: Rabatt2
    description: "Second discount rate tier for association members"
    type: decimal
    example: "15.0"
    
  - name: Rabatt3
    description: "Third discount rate tier for association members"
    type: decimal
    example: "20.0"

relationships:
  - name: can_be_a
    target: Customer
    type: 1:M
    description: "Association partner can be represented by customers"

normalization_hints:
  multi_valued: []
  redundant: []
  constrained: 
    - Rabatt1
    - Rabatt2
    - Rabatt3
```

---

## File: entities/order.yaml

```yaml
layer: conceptual
entity: Order
description: "Purchase transaction from customer requesting products. Orders originate from webshop or roadshow channels, contain one or more positions, and may be linked to associations for roadshow orders."

attributes:
  - name: order_bk
    description: "Unique identifier for the order (business key)"
    type: string
    example: "B2022-00123"
    
  - name: AllgLieferAdrID
    description: "General delivery address ID for the entire order"
    type: string
    example: "A7890"
    
  - name: Bestelldatum
    description: "Date when the order was placed"
    type: date
    example: "2022-03-07"
    
  - name: Rabatt
    description: "Discount applied to the order"
    type: decimal
    example: "10.50"
    
  - name: Wunschdatum
    description: "Customer's desired delivery date"
    type: date
    example: "2022-03-14"

relationships:
  - name: is_composed_of
    target: Position
    type: 1:M
    description: "Order is composed of positions"
    
  - name: can_be_linked_to
    target: AssociationPartner
    type: M:1
    description: "Order can be linked to association partner (roadshow only)"

normalization_hints:
  multi_valued: []
  redundant: 
    - Rabatt
  constrained: []
```

---

## File: entities/position.yaml

```yaml
layer: conceptual
entity: Position
description: "Individual line item within an order representing a specific product with quantity and pricing. Positions may have special delivery addresses and payment details, particularly for roadshow orders."

attributes:
  - name: Position_bk
    description: "Unique identifier for the position (business key)"
    type: string
    example: "BP2022-00123-001"
    
  - name: GueltigBis
    description: "Credit card expiration date for this position"
    type: date
    example: "2025-12-31"
    
  - name: Kaufdatum
    description: "Purchase date for this position"
    type: date
    example: "2022-03-07"
    
  - name: KKFirma
    description: "Credit card company for this position"
    type: string
    example: "VISA"
    
  - name: Kreditkarte
    description: "Credit card number used for this position"
    type: string
    example: "4111111111111111"
    
  - name: Menge
    description: "Quantity of product ordered"
    type: number
    example: "3"
    
  - name: PosID
    description: "Position number within the order"
    type: number
    example: "1"
    
  - name: Preis
    description: "Unit price of the product at time of order"
    type: decimal
    example: "12.50"
    
  - name: Rabatt
    description: "Discount applied to this position"
    type: decimal
    example: "1.25"
    
  - name: SpezLieferAdrID
    description: "Special delivery address ID for this specific position"
    type: string
    example: "A7891"

relationships:
  - name: contains_a
    target: Product
    type: M:1
    description: "Position contains a product"
    
  - name: can_have_a_special
    target: DeliveryAddress
    type: M:1
    description: "Position can have a special delivery address"

normalization_hints:
  multi_valued: []
  redundant: 
    - Rabatt
  constrained: []
```

---

## File: entities/product.yaml

```yaml
layer: conceptual
entity: Product
description: "Item available for purchase in the Willibald catalog including seeds, plants, tools, and gardening supplies. Each product has pricing, planting information, and belongs to a product category."

attributes:
  - name: product_bk
    description: "Unique identifier for the product (business key)"
    type: string
    example: "P5001"
    
  - name: Bezeichnung
    description: "Product name or description"
    type: string
    example: "Tomate Roma Bio-Saatgut"
    
  - name: Pflanzabstand
    description: "Recommended planting distance in centimeters"
    type: number
    example: "50"
    
  - name: Pflanzort
    description: "Recommended planting location (sun, shade, greenhouse)"
    type: string
    example: "Sonnig"
    
  - name: Preis
    description: "Current retail price of the product"
    type: decimal
    example: "4.99"
    
  - name: productcategory_bk
    description: "Foreign key reference to product category"
    type: string
    example: "CAT-001"
    
  - name: Typ
    description: "Product type classification"
    type: string
    example: "Saatgut"
    
  - name: Umfang
    description: "Package size or quantity"
    type: string
    example: "50 Korn"

relationships:
  - name: is_assigned_to
    target: ProductCategory
    type: M:1
    description: "Product is assigned to a product category"

normalization_hints:
  multi_valued: []
  redundant: []
  constrained: 
    - Preis
```

---

## File: entities/product_category.yaml

```yaml
layer: conceptual
entity: ProductCategory
description: "Hierarchical classification system for organizing products. Categories can have parent categories creating a multi-level taxonomy for seeds, plants, tools, and accessories."

attributes:
  - name: productcategory_bk
    description: "Unique identifier for the product category (business key)"
    type: string
    example: "CAT-001"
    
  - name: productcategory_parent_bk
    description: "Parent category business key for hierarchical structure"
    type: string
    example: "CAT-000"
    
  - name: Name
    description: "Category name"
    type: string
    example: "Gemüsesamen"

relationships:
  - name: is_grouped_into
    target: ProductCategory
    type: M:1
    description: "Category is grouped into parent category (self-referential hierarchy)"

normalization_hints:
  multi_valued: []
  redundant: []
  constrained: []
```

---

## File: entities/delivery.yaml

```yaml
layer: conceptual
entity: Delivery
description: "Physical shipment record tracking when and how positions are delivered. Links orders and positions to delivery addresses and delivery services. Contains the actual delivery date for adherence tracking."

attributes:
  - name: deliveryadress_bk
    description: "Delivery address business key (business key component)"
    type: string
    example: "A7890"
    
  - name: deliveryservice_bk
    description: "Delivery service provider business key (business key component)"
    type: string
    example: "DS001"
    
  - name: order_bk
    description: "Order business key (business key component)"
    type: string
    example: "B2022-00123"
    
  - name: position_bk
    description: "Position business key (business key component)"
    type: string
    example: "BP2022-00123-001"
    
  - name: BestellungID
    description: "Order ID reference for the delivery"
    type: string
    example: "B2022-00123"
    
  - name: PosID
    description: "Position number reference"
    type: number
    example: "1"
    
  - name: LieferDatum
    description: "Actual delivery date when shipment arrived"
    type: date
    example: "2022-03-13"

relationships:
  - name: contain_one_or_more
    target: Position
    type: 1:M
    description: "Delivery contains one or more positions"
    
  - name: is_done_by
    target: DeliveryService
    type: M:1
    description: "Delivery is done by a delivery service"
    
  - name: sends_to
    target: DeliveryAddress
    type: M:1
    description: "Delivery sends to a delivery address"

normalization_hints:
  multi_valued: []
  redundant: []
  constrained: []
```

---

## File: entities/delivery_address.yaml

```yaml
layer: conceptual
entity: DeliveryAddress
description: "Physical address where deliveries can be sent. Customers can have multiple delivery addresses. Addresses can be used as general order addresses or special position addresses."

attributes:
  - name: Deliveryadress_bk
    description: "Unique identifier for the delivery address (business key)"
    type: string
    example: "A7890"
    
  - name: Adresszusatz
    description: "Address supplement (apartment number, floor, building)"
    type: string
    example: "Appartement 2B"
    
  - name: Hausnummer
    description: "House or building number"
    type: string
    example: "45"
    
  - name: Land
    description: "Country name"
    type: string
    example: "Deutschland"
    
  - name: Ort
    description: "City or town name"
    type: string
    example: "Erlangen"
    
  - name: Plz
    description: "Postal code for delivery routing"
    type: string
    example: "91054"
    
  - name: Strasse
    description: "Street name"
    type: string
    example: "Hauptstrasse"

relationships: []

normalization_hints:
  multi_valued: []
  redundant: []
  constrained: 
    - Land
```

---

## File: entities/delivery_service.yaml

```yaml
layer: conceptual
entity: DeliveryService
description: "Logistics provider or carrier company that handles physical delivery of orders. Delivery services have contact information and address details for coordination."

attributes:
  - name: deliveryservice_bk
    description: "Unique identifier for the delivery service provider (business key)"
    type: string
    example: "DS001"
    
  - name: Email
    description: "Email address for service provider contact"
    type: string
    example: "info@dhl.de"
    
  - name: Fax
    description: "Fax number for service provider"
    type: string
    example: "+49 9131 999999"
    
  - name: Hausnummer
    description: "House number of service provider office"
    type: string
    example: "100"
    
  - name: Land
    description: "Country where service provider is based"
    type: string
    example: "Deutschland"
    
  - name: Name
    description: "Name of the delivery service company"
    type: string
    example: "DHL Express"
    
  - name: Ort
    description: "City where service provider office is located"
    type: string
    example: "Bonn"
    
  - name: Plz
    description: "Postal code of service provider office"
    type: string
    example: "53113"
    
  - name: Strasse
    description: "Street of service provider office"
    type: string
    example: "Charles-de-Gaulle-Strasse"
    
  - name: Telefon
    description: "Phone number for service provider contact"
    type: string
    example: "+49 228 12345678"

relationships: []

normalization_hints:
  multi_valued: []
  redundant: []
  constrained: []
```

---

## Summary of Relationship Updates Based on Willibald.json:

### Relationships from JSON:

1. **AssociationPartner → Customer**: "can be a" (not the reverse)
2. **Customer → AssociationPartner**: "can be member of"
3. **Customer → DeliveryAddress**: "has a"
4. **Customer → Order**: "makes a"
5. **Delivery → Position**: "contain one or more"
6. **Delivery → DeliveryService**: "is done by"
7. **Delivery → DeliveryAddress**: "sends to"
8. **Order → AssociationPartner**: "can be linked to" (roadshow only)
9. **Order → Position**: "is composed of"
10. **Position → DeliveryAddress**: "can have a special"
11. **Position → Product**: "contains a"
12. **Product → ProductCategory**: "is assigned to"
13. **ProductCategory → ProductCategory**: "is grouped into" (hierarchical)

Note: DeliveryAddress and DeliveryService have no outgoing relationships defined in the JSON.