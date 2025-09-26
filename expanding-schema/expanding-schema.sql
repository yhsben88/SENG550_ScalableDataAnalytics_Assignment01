CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_id),
    payment_date DATE NOT NULL,
    amount NUMERIC NOT NULL,
    payment_method TEXT NOT NULL,
    status TEXT CHECK (status IN ('Completed', 'Pending', 'Failed'))
);

CREATE TABLE carrier (
    carrier_id SERIAL PRIMARY KEY,
    delivery_id INTEGER NOT NULL REFERENCES deliveries(delivery_id),
    name TEXT NOT NULL,
    contact_number TEXT,
    service_type TEXT
);