# Database Schema Documentation

## Table: `payments`

### Attributes

| Column Name    | Data Type | Constraints                                          | Description                                                              |
| -------------- | --------- | ---------------------------------------------------- | ------------------------------------------------------------------------ |
| payment_id     | SERIAL    | Primary Key                                          | Unique identifier for each payment record                                |
| order_id       | INTEGER   | Foreign Key, NOT NULL, REFERENCES orders(order_id)   | References the orders(order_id) to connect a payment to a specific order |
| payment_date   | DATE      | NOT NULL                                             | Date when the payment was made                                           |
| amount         | NUMERIC   | NOT NULL                                             | The amount paid                                                          |
| payment_method | TEXT      | NOT NULL                                             | Method of payment (e.g., Credit Card, PayPal, Cash)                      |
| status         | TEXT      | CHECK (status IN ('Completed', 'Pending', 'Failed')) | Status of the payment (e.g., Completed, Pending, Failed)                 |

### Relationships

- Each payment must correspond to an existing order
- Ensures that payments cannot exist without an order (enforced by foreign key constraint)

### SQL Definition

```sql
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_id),
    payment_date DATE NOT NULL,
    amount NUMERIC NOT NULL,
    payment_method TEXT NOT NULL,
    status TEXT CHECK (status IN ('Completed', 'Pending', 'Failed'))
);
```

## Table: `carrier`

### Attributes

| Column Name    | Data Type | Constraints                                               | Description                                                          |
| -------------- | --------- | --------------------------------------------------------- | -------------------------------------------------------------------- |
| carrier_id     | SERIAL    | Primary Key                                               | Unique identifier for each carrier (e.g., FedEx, UPS)                |
| delivery_id    | INTEGER   | Foreign Key, NOT NULL, REFERENCES deliveries(delivery_id) | References deliveries(delivery_id) to link a delivery to the carrier |
| name           | TEXT      | NOT NULL                                                  | The name of the carrier company                                      |
| contact_number | TEXT      | -                                                         | Contact number of the carrier                                        |
| service_type   | TEXT      | -                                                         | Type of service (e.g., Standard, Express)                            |

### Relationships

- Each delivery is handled by exactly one carrier
- Models real-world logistics: deliveries are carried out by external or internal shipping companies

### Schema Changes Required

- Add a foreign key constraint: `carrier.delivery_id` references `deliveries(delivery_id)`
- Optional: Add `carrier_id` column to `deliveries` table for reverse relationship

### SQL Definition

```sql
CREATE TABLE carrier (
    carrier_id SERIAL PRIMARY KEY,
    delivery_id INTEGER NOT NULL REFERENCES deliveries(delivery_id),
    name TEXT NOT NULL,
    contact_number TEXT,
    service_type TEXT
);
```
