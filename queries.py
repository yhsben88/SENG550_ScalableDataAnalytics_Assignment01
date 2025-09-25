"""
queries.py

This module contains functions for adding and updating records in the PostgreSQL database.  
It serves as the data access layer for customer, order, and delivery records.

Functions:
    add_customer(conn, cur, name, email, phone, address) -> cursor | None
    add_order(conn, cur, customer_id, order_date, total_amount, product_id, product_category, product_name) -> cursor | None
    add_delivery(conn, cur, order_id, delivery_date, status) -> cursor | None
    update_delivery_status(conn, cur, delivery_id, new_status) -> cursor | int | None

Notes:
    - On success, functions return the active cursor positioned after the executed query.
    - On error, functions return None (and roll back the transaction).
    - `update_delivery_status` may also return the integer 1 if no matching delivery record is found.

Appendix:
    psycopg2:
        1. conn (connection): Connection object that establishes a connection with the database.
        2. cur (cursor): Cursor object derived from conn to execute SQL queries.
"""

from psycopg2.extensions import connection, cursor


def add_customer(conn: connection, cur: cursor, name: str, email: str, phone: str, address: str) -> cursor | None:
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
        cursor | None: The cursor after successful execution, or None if an error occurred.
    """
    placeholders = ', '.join(['%s'] * 4)
    query = f"INSERT INTO customers (name, email, phone, address) VALUES ({placeholders})"
    values = [name, email, phone, address]
    try:
        cur.execute(query, values)
        conn.commit()
        return cur
    except Exception as e:
        print(f"❌ Error inserting into customers: {e}")
        conn.rollback()
        return


def add_order(conn: connection, cur: cursor, customer_id: int, order_date: str, total_amount: float,
              product_id: int, product_category: str, product_name: str) -> cursor | None:
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
        cursor | None: The cursor after successful execution, or None if an error occurred.
    """
    query = """
        INSERT INTO orders (customer_id, order_date, total_amount, product_id, product_category, product_name)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (customer_id, order_date, total_amount, product_id, product_category, product_name)
    try:
        cur.execute(query, values)
        conn.commit()
        return cur
    except Exception as e:
        print(f"❌ Error inserting into orders: {e}")
        conn.rollback()
        return


def add_delivery(conn: connection, cur: cursor, order_id: int, delivery_date: str, status: str) -> cursor | None:
    """
    Insert a new delivery record into the database.

    Args:
        conn (connection): Active psycopg2 database connection.
        cur (cursor): psycopg2 cursor for executing queries.
        order_id (int): ID of the associated order.
        delivery_date (str): Date the delivery is scheduled or completed (format: YYYY-MM-DD).
        status (str): Current status of the delivery (e.g., 'Pending', 'Shipped', 'Delivered').

    Returns:
        cursor | None: The cursor after successful execution, or None if an error occurred.
    """
    query = """
        INSERT INTO deliveries (order_id, delivery_date, status) 
        VALUES (%s, %s, %s)
    """
    values = (order_id, delivery_date, status)
    try:
        cur.execute(query, values)
        conn.commit()
        return cur
    except Exception as e:
        print(f"❌ Error inserting into deliveries: {e}")
        conn.rollback()
        return


def update_delivery_status(conn: connection, cur: cursor, delivery_id: int, new_status: str) -> cursor | int | None:
    """
    Update the status of an existing delivery in the database.

    Args:
        conn (connection): Active psycopg2 database connection.
        cur (cursor): psycopg2 cursor for executing queries.
        delivery_id (int): Unique identifier of the delivery record to update.
        new_status (str): Updated status value (e.g., 'Delivered', 'Cancelled').

    Returns:
        cursor | int | None:
            - cursor: The cursor after a successful update.
            - int: The value 1 if no delivery record with the given ID was found.
            - None: If an error occurred.
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
            conn.rollback()
            return 1
        conn.commit()
        return cur
    except Exception as e:
        print(f"❌ Error updating delivery status: {e}")
        conn.rollback()
        return
