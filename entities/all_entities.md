# All Entity YAML Files

Save each section below as a separate file in the `entities/` directory.

---

## File: entities/customer.yaml

```yaml
layer: conceptual
entity: Customer
description: "Individual or organization that purchases seeds, plants, and gardening products from the Willibald shop. Customers can place orders, have multiple delivery addresses, and may be members of garden clubs."

attributes:
  - name: CustomerId
    description: "Unique identifier for the customer assigned by the system"
    type: string
    example: "K12345"
    
  - name: Name
    description: "Full name of the customer or company name for business customers"
    type: string
    example: "Maria Schmidt"
    
  - name: Email
    description: "Primary contact email address for order confirmations and communications"
    type: string
    example: "maria.schmidt@example.com"
    
  - name: Phone
    description: "Primary phone number for delivery coordination"
    type: string
    example: "+49 151 12345678"
    
  - name: RegistrationDate
    description: "Date when the customer first registered with Willibald shop"
    type: date
    example: "2022-01-15"

relationships:
  - name: places_orders
    target: Order
    type: 1:M
    description: "A customer can place multiple orders over time, tracking their purchase history"
    
  - name: has_residences
    target: Residence
    type: 1:M
    description: "Customer may have lived at multiple addresses over time, important for delivery and marketing analytics"
    
  - name: member_of_club
    target: ClubPartner
    type: M:1
    description: "Customer may optionally be a member of a partner garden club for special discounts"

normalization_hints:
  multi_valued: 
    - Residence
  redundant: []
  constrained: 
    - Email
```

---

## File: entities/order.yaml

```yaml
layer: conceptual
entity: Order
description: "Purchase transaction representing a customer's request to buy products. Orders can originate from the webshop or roadshow events, contain multiple items, and result in one or more deliveries."

attributes:
  - name: OrderId
    description: "Unique identifier for the order"
    type: string
    example: "B2022-00123"
    
  - name: OrderDate
    description: "Date and time when the customer placed the order"
    type: date
    example: "2022-03-07"
    
  - name: TotalAmount
    description: "Total monetary value of the order including all items and applicable discounts"
    type: decimal
    example: "127.50"
    
  - name: OrderStatus
    description: "Current processing status of the order"
    type: string
    example: "Completed"
    
  - name: Source
    description: "Channel through which the order was placed"
    type: string
    example: "Webshop"

relationships:
  - name: contains_items
    target: OrderItem
    type: 1:M
    description: "An order consists of one or more line items, each representing a product and quantity"
    
  - name: results_in_deliveries
    target: Delivery
    type: 1:M
    description: "An order may be fulfilled through one or more separate deliveries depending on product availability"

normalization_hints:
  multi_valued: []
  redundant: 
    - TotalAmount
  constrained: 
    - OrderStatus
    - Source
```

---

## File: entities/order_item.yaml

```yaml
layer: conceptual
entity: OrderItem
description: "Individual line item within an order representing a specific product, quantity, and price. Each order item links a product to an order with purchase details."

attributes:
  - name: OrderItemId
    description: "Unique identifier for the order line item"
    type: string
    example: "BP2022-00123-001"
    
  - name: Quantity
    description: "Number of units of the product ordered"
    type: number
    example: "3"
    
  - name: UnitPrice
    description: "Price per unit at the time of order"
    type: decimal
    example: "12.50"
    
  - name: LineTotal
    description: "Total amount for this line item"
    type: decimal
    example: "37.50"
    
  - name: ItemStatus
    description: "Processing status of this specific item"
    type: string
    example: "Shipped"

relationships: []

normalization_hints:
  multi_valued: []
  redundant: 
    - LineTotal
  constrained: []
```

---

## File: entities/product.yaml

```yaml
layer: conceptual
entity: Product
description: "Item available for purchase in the Willibald catalog, including seeds, plants, tools, and gardening supplies. Each product belongs to a category and has pricing and inventory information."

attributes:
  - name: ProductId
    description: "Unique identifier for the product in the catalog"
    type: string
    example: "P5001"
    
  - name: ProductName
    description: "Marketing name of the product displayed to customers"
    type: string
    example: "Organic Tomato Seeds - Roma"
    
  - name: Description
    description: "Detailed description of the product including growing instructions"
    type: string
    
  - name: Price
    description: "Current retail price of the product"
    type: decimal
    example: "4.99"
    
  - name: StockLevel
    description: "Current quantity available in inventory"
    type: number
    example: "150"

relationships:
  - name: appears_in_items
    target: OrderItem
    type: 1:M
    description: "A product can appear in multiple order items across different orders"

normalization_hints:
  multi_valued: []
  redundant: []
  constrained: 
    - Price
    - StockLevel
```

---

## File: entities/product_category.yaml

```yaml
layer: conceptual
entity: ProductCategory
description: "Hierarchical classification system for organizing products. Categories can have parent categories creating a multi-level taxonomy."

attributes:
  - name: CategoryId
    description: "Unique identifier for the product category"
    type: string
    example: "CAT-001"
    
  - name: CategoryName
    description: "Display name of the category"
    type: string
    example: "Vegetable Seeds"
    
  - name: Description
    description: "Explanation of what products belong in this category"
    type: string
    
  - name: Level
    description: "Depth in the category hierarchy"
    type: number
    example: "2"

relationships:
  - name: has_parent
    target: ProductCategory
    type: M:1
    description: "Category may have one parent category in the hierarchy"
    
  - name: has_children
    target: ProductCategory
    type: 1:M
    description: "Category may contain multiple child subcategories"
    
  - name: contains_products
    target: Product
    type: 1:M
    description: "Category groups multiple products for browsing and organization"

normalization_hints:
  multi_valued: []
  redundant: 
    - Level
  constrained: []
```

---

## File: entities/delivery.yaml

```yaml
layer: conceptual
entity: Delivery
description: "Physical shipment of products to fulfill one or more orders. Tracks expected and actual delivery dates, shipping status, and performance against delivery commitments."

attributes:
  - name: DeliveryId
    description: "Unique identifier for the delivery shipment"
    type: string
    example: "L2022-00089"
    
  - name: PlannedDeliveryDate
    description: "Date when delivery was promised to the customer"
    type: date
    example: "2022-03-14"
    
  - name: ActualDeliveryDate
    description: "Date when delivery was actually completed"
    type: date
    example: "2022-03-13"
    
  - name: DeliveryStatus
    description: "Current status of the delivery"
    type: string
    example: "Delivered"
    
  - name: TrackingNumber
    description: "Carrier tracking identifier for shipment"
    type: string
    example: "DHL123456789"

relationships: []

normalization_hints:
  multi_valued: []
  redundant: []
  constrained: 
    - DeliveryStatus
```

---

## File: entities/delivery_address.yaml

```yaml
layer: conceptual
entity: DeliveryAddress
description: "Physical address where deliveries can be sent. Customers may have multiple delivery addresses and addresses can receive multiple deliveries."

attributes:
  - name: AddressId
    description: "Unique identifier for the delivery address"
    type: string
    example: "A7890"
    
  - name: Street
    description: "Street address including house number"
    type: string
    example: "Hauptstrasse 45"
    
  - name: City
    description: "City or municipality name"
    type: string
    example: "Erlangen"
    
  - name: PostalCode
    description: "Postal code for delivery routing"
    type: string
    example: "91054"
    
  - name: Country
    description: "Country code or name"
    type: string
    example: "Germany"
    
  - name: AddressType
    description: "Classification of address use"
    type: string
    example: "Primary"

relationships:
  - name: receives_deliveries
    target: Delivery
    type: 1:M
    description: "An address can receive multiple deliveries over time"

normalization_hints:
  multi_valued: []
  redundant: []
  constrained: 
    - Country
    - AddressType
```

---

## File: entities/club_partner.yaml

```yaml
layer: conceptual
entity: ClubPartner
description: "Garden club or association that has a partnership agreement with Willibald. Members of partner clubs receive special discounts and benefits."

attributes:
  - name: ClubPartnerId
    description: "Unique identifier for the partner club"
    type: string
    example: "VP001"
    
  - name: ClubName
    description: "Official name of the garden club or association"
    type: string
    example: "Erlangen Garden Society"
    
  - name: MembershipType
    description: "Type of partnership agreement"
    type: string
    example: "Premium"
    
  - name: JoinDate
    description: "Date when the partnership agreement started"
    type: date
    example: "2021-06-01"
    
  - name: DiscountRate
    description: "Percentage discount offered to club members"
    type: decimal
    example: "15.0"

relationships:
  - name: has_members
    target: Customer
    type: 1:M
    description: "A club can have multiple customer members enrolled for discounts"

normalization_hints:
  multi_valued: []
  redundant: []
  constrained: 
    - MembershipType
    - DiscountRate
```

---

## File: entities/residence.yaml

```yaml
layer: conceptual
entity: Residence
description: "Historical record of where a customer has lived over time. Used for customer analytics and regional marketing campaigns. This is a temporal entity tracking address changes."

attributes:
  - name: ResidenceId
    description: "Unique identifier for this residence record"
    type: string
    example: "W001-2022"
    
  - name: City
    description: "City where the customer resided"
    type: string
    example: "Munich"
    
  - name: State
    description: "State or region"
    type: string
    example: "Bavaria"
    
  - name: Country
    description: "Country of residence"
    type: string
    example: "Germany"
    
  - name: PostalCode
    description: "Postal code of residence area"
    type: string
    example: "80331"
    
  - name: FromDate
    description: "Date when customer started living at this residence"
    type: date
    example: "2020-01-01"
    
  - name: ToDate
    description: "Date when customer moved away"
    type: date
    example: "2022-06-30"

relationships: []

normalization_hints:
  multi_valued: 
    - "Multiple residences per customer over time"
  redundant: []
  constrained: 
    - FromDate
    - ToDate
```

---

## File: entities/category_adherence.yaml

```yaml
layer: conceptual
entity: CategoryAdherence
description: "Reference data defining delivery performance categories. Used to classify deliveries as on-time, early, or late. This is a static lookup table maintained by business rules."

attributes:
  - name: CategoryId
    description: "Unique identifier for the adherence category"
    type: string
    example: "ADH-001"
    
  - name: CategoryName
    description: "Name of the delivery performance category"
    type: string
    example: "Pünktlich"
    
  - name: Description
    description: "Business definition of this category"
    type: string
    example: "Delivery completed within promised timeframe"
    
  - name: SortOrder
    description: "Display order for reporting"
    type: number
    example: "1"

relationships: []

normalization_hints:
  multi_valued: []
  redundant: []
  constrained: 
    - CategoryName
```