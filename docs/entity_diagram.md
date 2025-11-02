# Willibald Conceptual Entity Diagram

## Business Entity Relationships

```mermaid
erDiagram
    AssociationPartner {
        string associationpartner_bk
        string KundeIDVerein
        decimal Rabatt1
        decimal Rabatt2
        decimal Rabatt3
    }
    Customer {
        string customer_bk
        string Email
        date Geburtsdatum
        string Geschlecht
        date GueltigBis
    }
    Delivery {
        string deliveryadress_bk
        string deliveryservice_bk
        string order_bk
        string position_bk
        string BestellungID

    }
    DeliveryAddress {
        string Deliveryadress_bk
        string Adresszusatz
        string Hausnummer
        string Land
        string Ort

    }
    DeliveryService {
        string deliveryservice_bk
        string Email
        string Fax
        string Hausnummer
        string Land

    }
    Order {
        string order_bk
        string AllgLieferAdrID
        date Bestelldatum
        decimal Rabatt
        date Wunschdatum
    }
    Position {
        string Position_bk
        date GueltigBis
        date Kaufdatum
        string KKFirma
        string Kreditkarte

    }
    Product {
        string product_bk
        string Bezeichnung
        number Pflanzabstand
        string Pflanzort
        decimal Preis

    }
    ProductCategory {
        string productcategory_bk
        string productcategory_parent_bk
        string Name
    }

    AssociationPartner ||--o{ Customer : can_be_a
    Customer ||--o{ Order : makes_a
    Customer ||--o{ DeliveryAddress : has_a
    Customer }o--|| AssociationPartner : can_be_member_of
    Delivery ||--o{ Position : contain_one_or_more
    Delivery }o--|| DeliveryService : is_done_by
    Delivery }o--|| DeliveryAddress : sends_to
    Order ||--o{ Position : is_composed_of
    Order }o--|| AssociationPartner : can_be_linked_to
    Position }o--|| Product : contains_a
    Position }o--|| DeliveryAddress : can_have_a_special
    Product }o--|| ProductCategory : is_assigned_to
    ProductCategory }o--|| ProductCategory : is_grouped_into
```

## Entity Descriptions

### AssociationPartner
Garden association or club that has a partnership agreement with Willibald. Members receive special discounts. The association is represented by a customer contact person.

### Customer
Individual or organization that purchases seeds, plants, and gardening products from the Willibald shop. Customers can place orders through webshop or roadshow channels, have delivery addresses, and may be members of partner associations. Historical residence information is tracked as multi-active attributes.

### Delivery
Physical shipment record tracking when and how positions are delivered. Links orders and positions to delivery addresses and delivery services. Contains the actual delivery date for adherence tracking.

### DeliveryAddress
Physical address where deliveries can be sent. Customers can have multiple delivery addresses. Addresses can be used as general order addresses or special position addresses.

### DeliveryService
Logistics provider or carrier company that handles physical delivery of orders. Delivery services have contact information and address details for coordination.

### Order
Purchase transaction from customer requesting products. Orders originate from webshop or roadshow channels, contain one or more positions, and may be linked to associations for roadshow orders.

### Position
Individual line item within an order representing a specific product with quantity and pricing. Positions may have special delivery addresses and payment details, particularly for roadshow orders.

### Product
Item available for purchase in the Willibald catalog including seeds, plants, tools, and gardening supplies. Each product has pricing, planting information, and belongs to a product category.

### ProductCategory
Hierarchical classification system for organizing products. Categories can have parent categories creating a multi-level taxonomy for seeds, plants, tools, and accessories.
