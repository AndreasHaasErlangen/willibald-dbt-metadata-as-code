# Willibald Entity Overview

## Business Context

The Willibald seed shop is a specialized retailer selling seeds, plants, tools, and gardening supplies to individual customers and garden clubs. The business operates through two primary channels:

1. **Webshop**: Online ordering platform for customers
2. **Roadshow**: Mobile sales events at garden shows and club meetings

## Entity Descriptions

### Customer
**Type**: Core Entity | **Pattern**: Multi-source

Individuals or organizations that purchase products from Willibald. Customers can:
- Place orders through webshop or roadshow channels
- Have multiple delivery addresses (home, work, vacation property)
- Be members of partner garden clubs for special discounts
- Change residences over time (tracked for marketing analytics)

**Key Attributes**: CustomerId, Name, Email, Phone, RegistrationDate

**Special Considerations**: 
- Customer data may come from both Webshop and Roadshow systems
- Roadshow may create "ghost" customer records that later get matched to real customers

---

### Order
**Type**: Core Entity | **Pattern**: Multi-source

Purchase transactions representing a customer's request to buy products. Each order:
- Originates from either webshop or roadshow channel
- Contains one or more line items (products with quantities)
- May result in one or more separate deliveries
- Tracks total amount and current status

**Key Attributes**: OrderId, OrderDate, TotalAmount, OrderStatus, Source

**Special Considerations**:
- Orders can be split into multiple deliveries based on product availability
- Total amount is redundant (calculated from line items)

---

### OrderItem
**Type**: Detail Entity | **Pattern**: Standard

Individual line items within an order. Each order item:
- Links one product to one order
- Specifies quantity and unit price at time of order
- Has its own processing status
- Calculates line total (quantity × unit price)

**Key Attributes**: OrderItemId, Quantity, UnitPrice, LineTotal, ItemStatus

**Special Considerations**:
- Unit price is captured at order time (may differ from current product price)
- Line total is redundant but useful for auditing

---

### Product
**Type**: Core Entity | **Pattern**: Standard

Items available for purchase in the Willibald catalog. Products include:
- Seeds (vegetables, flowers, herbs)
- Plants (seedlings, bulbs)
- Tools and gardening supplies
- Belongs to a product category
- Has current pricing and stock levels

**Key Attributes**: ProductId, ProductName, Description, Price, StockLevel

**Special Considerations**:
- Price changes over time (order items capture price at time of order)
- Stock levels change frequently with orders and replenishments

---

### ProductCategory
**Type**: Reference Entity | **Pattern**: Hierarchical (Self-referential)

Hierarchical classification system for organizing products. Categories:
- Form a tree structure (parent-child relationships)
- Can have multiple levels (e.g., Seeds → Vegetable Seeds → Tomato Seeds)
- Each category can contain products and/or subcategories
- Track their depth level in the hierarchy

**Key Attributes**: CategoryId, CategoryName, Description, Level

**Special Considerations**:
- **Self-referential relationship**: Categories can have parent categories
- Root categories have no parent (null parent)
- Level attribute is redundant but useful for queries

---

### Delivery
**Type**: Core Entity | **Pattern**: Standard

Physical shipments of products to fulfill orders. Each delivery:
- Fulfills one or more orders (or parts of orders)
- Tracks planned vs. actual delivery dates
- Has carrier tracking information
- Classified by delivery adherence (on-time, early, late)

**Key Attributes**: DeliveryId, PlannedDeliveryDate, ActualDeliveryDate, DeliveryStatus, TrackingNumber

**Special Considerations**:
- Delivery adherence is calculated by comparing planned vs. actual dates
- One order may result in multiple deliveries

---

### DeliveryAddress
**Type**: Reference Entity | **Pattern**: Standard

Physical addresses where deliveries can be sent. Addresses:
- Belong to customers (customers can have multiple addresses)
- Receive multiple deliveries over time
- Classified by type (Primary, Secondary, Vacation, etc.)
- Include full postal information for routing

**Key Attributes**: AddressId, Street, City, PostalCode, Country, AddressType

**Special Considerations**:
- Different from Residence (which tracks historical locations for analytics)
- Active addresses for current/future deliveries

---

### ClubPartner
**Type**: Reference Entity | **Pattern**: Standard

Garden clubs or associations with partnership agreements. Partner clubs:
- Have negotiated discount rates for their members
- Offer different membership tiers (Premium, Standard, Basic)
- Track partnership start date
- Have multiple customer members enrolled

**Key Attributes**: ClubPartnerId, ClubName, MembershipType, JoinDate, DiscountRate

**Special Considerations**:
- Discount rates vary by membership type
- Partnership agreements may change over time

---

### Residence
**Type**: Historical Entity | **Pattern**: Multi-active (Temporal)

Historical records of where customers have lived over time. Residence records:
- Track customer locations for regional marketing and analytics
- Have validity periods (FromDate, ToDate)
- Multiple residences per customer (person moves over time)
- Used for understanding customer mobility patterns

**Key Attributes**: ResidenceId, City, State, Country, PostalCode, FromDate, ToDate

**Special Considerations**:
- **Multi-active satellite pattern**: Customers can have multiple active residences over time
- ToDate is null for current residence
- Used for analytics, not for delivery routing (use DeliveryAddress instead)

---

### CategoryAdherence
**Type**: Reference Data | **Pattern**: Static Lookup

Reference table defining delivery performance categories. Contains:
- Three categories: "Pünktlich" (On-time), "Zu früh" (Early), "Zu spät" (Late)
- Business definitions for each category
- Sort order for reporting
- Static data maintained by business rules

**Key Attributes**: CategoryId, CategoryName, Description, SortOrder

**Special Considerations**:
- **Reference table**: Rarely changes, no relationships to other entities
- Used to classify deliveries for KPI reporting
- German category names reflect business language

---

## Entity Relationship Summary

```
Customer (1) ----< (M) Order
Customer (1) ----< (M) Residence [Multi-active]
Customer (M) >---- (1) ClubPartner

Order (1) ----< (M) OrderItem
Order (1) ----< (M) Delivery

Product (1) ----< (M) OrderItem
ProductCategory (1) ----< (M) Product
ProductCategory (M) >---- (1) ProductCategory [Hierarchical]

DeliveryAddress (1) ----< (M) Delivery
```

## Data Vault Patterns Identified

1. **Multi-source Hubs**: Customer, Order (Webshop + Roadshow)
2. **Hierarchical Link**: ProductCategory (self-referential)
3. **Multi-active Satellite**: Residence (temporal addresses)
4. **Reference Tables**: CategoryAdherence (static lookup)
5. **Ghost Records**: Roadshow customer records without full data
6. **Effectivity Satellites**: Residence with FromDate/ToDate

---

**Document Version**: 1.0  
**Last Updated**: November 2025