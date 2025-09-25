"""
queries.py

This module contains functions for adding and updating records in the PostgreSQL database.  
It serves as the data access layer for customer, order, and delivery records.

Functions:
    add_customer(conn, cur, name, email, phone, address) -> int | None
    add_order(conn, cur, customer_id, order_date, total_amount, product_id, product_category, product_name) -> int | None
    add_delivery(conn, cur, order_id, delivery_date, status) -> int | None
    update_delivery_status(conn, cur, delivery_id, new_status) -> bool

Notes:
    - On success, add_* functions return the ID of the newly inserted row.
    - update_delivery_status returns True on success, False if the delivery ID was not found or an error occurred.
    - All functions commit the transaction on success, rollback on failure.
"""

from psycopg2.extensions import connection, cursor


def add_customer(conn: connection, cur: cursor, name: str, email: str, phone: str, address: str) -> int | None:
    """
    Insert a new customer record into the database.

    Args:
        conn (connection): Active psycopg2 database connection.
        cur (cursor): psycopg2 cursor for executing queries.
        name (str): Customer's full name.
        email (str): Customer's email address.
        phone (str): Customer's phone number.
        address (str): Customer's street address.

    Returns:
        int | None: ID of the newly added customer, or None if an error occurred.
    """
    query = """
        INSERT INTO customers (name, email, phone, address)
        VALUES (%s, %s, %s, %s)
        RETURNING customer_id
    """
    values = [name, email, phone, address]
    try:
        cur.execute(query, values)
        customer_id = cur.fetchone()[0]
        return customer_id
    except Exception as e:
        print(f"❌ Error inserting into customers: {e}")
        return None


def add_order(conn: connection, cur: cursor, customer_id: int, order_date: str, total_amount: float,
              product_id: int, product_category: str, product_name: str) -> int | None:
    """
    Insert a new order record into the database.

    Args:
        conn (connection): Active psycopg2 database connection.
        cur (cursor): psycopg2 cursor for executing queries.
        customer_id (int): ID of the customer placing the order.
        order_date (str): Date the order was placed (format: YYYY-MM-DD).
        total_amount (float): Total monetary value of the order.
        product_id (int): Unique identifier for the product in the order.
        product_category (str): Category or type of the product.
        product_name (str): Descriptive name of the product.

    Returns:
        int | None: ID of the newly added order, or None if an error occurred.
    """
    query = """
        INSERT INTO orders (customer_id, order_date, total_amount, product_id, product_category, product_name)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING order_id
    """
    values = (customer_id, order_date, total_amount, product_id, product_category, product_name)
    try:
        cur.execute(query, values)
        order_id = cur.fetchone()[0]
        return order_id
    except Exception as e:
        print(f"❌ Error inserting into orders: {e}")
        return None


def add_delivery(conn: connection, cur: cursor, order_id: int, delivery_date: str, status: str) -> int | None:
    """
    Insert a new delivery record into the database.

    Args:
        conn (connection): Active psycopg2 database connection.
        cur (cursor): psycopg2 cursor for executing queries.
        order_id (int): ID of the associated order.
        delivery_date (str): Date the delivery is scheduled or completed (format: YYYY-MM-DD).
        status (str): Current status of the delivery (e.g., 'Pending', 'Shipped', 'Delivered').

    Returns:
        int | None: ID of the newly added delivery, or None if an error occurred.
    """
    query = """
        INSERT INTO deliveries (order_id, delivery_date, status)
        VALUES (%s, %s, %s)
        RETURNING delivery_id
    """
    values = (order_id, delivery_date, status)
    try:
        cur.execute(query, values)
        delivery_id = cur.fetchone()[0]
        return delivery_id
    except Exception as e:
        print(f"❌ Error inserting into deliveries: {e}")
        return None


def update_delivery_status(conn: connection, cur: cursor, delivery_id: int, new_status: str) -> bool:
    """
    Update the status of an existing delivery in the database.

    Args:
        conn (connection): Active psycopg2 database connection.
        cur (cursor): psycopg2 cursor for executing queries.
        delivery_id (int): Unique identifier of the delivery record to update.
        new_status (str): Updated status value (e.g., 'Delivered', 'Cancelled').

    Returns:
        bool: True if the update succeeded, False otherwise (e.g., delivery ID not found or error).
    """
    query = """
        UPDATE deliveries
        SET status = %s
        WHERE delivery_id = %s
    """
    values = (new_status, delivery_id)
    try:
        cur.execute(query, values)
        if cur.rowcount == 0:
            print(f"⚠️ No delivery found with ID {delivery_id}")
            return False
        return True
    except Exception as e:
        print(f"❌ Error updating delivery status: {e}")
        return False
