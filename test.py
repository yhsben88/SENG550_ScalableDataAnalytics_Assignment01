"""
test.py

This module provides a utility function to perform test operations on the
PostgreSQL database using the `queries` module. The operations include adding
a test customer, adding a test order, adding a test delivery, and updating
the status of a delivery. The specific operation is selected via a step number.

Functions:
    perform_test(conn, cur, active_step_number: int) -> int
        Executes the selected test operation and returns an exit code.
"""

from psycopg2.extensions import connection, cursor
import queries

def perform_test(conn: connection, cur: cursor, active_step_number: int = 0) -> int:
    """
    Perform a database test operation based on the given step number.

    Args:
        conn (connection): Active psycopg2 database connection.
        cur (cursor): psycopg2 cursor for executing queries.
        active_step_number (int): Number representing the test step to execute:
            1 - Add a test customer
            2 - Add a test order
            3 - Add a test delivery
            4 - Update a delivery status

    Returns:
        int: Exit code of the operation (0 = success, 1 = failure, -1 = no valid step).
    """
    # Map numbers to test operation names
    test_step_map = {
        1: "add_test_customer",
        2: "add_test_order",
        3: "add_test_delivery",
        4: "update_delivery_status"
    }

    # Get the selected operation
    selected_test = test_step_map.get(active_step_number, None)
    if selected_test:
        print(f"Performing operation: {selected_test}")
    exit_code = -1

    # Execute the selected test operation
    match selected_test:
        case "add_test_customer":
            exit_code = queries.add_customer(conn, cur, "Test Subject", "test@gmail.com", "999-9999", "99 Fake Road Fake Direction")

        case "add_test_order":
            exit_code = queries.add_order(conn, cur, 1, "2020-12-14", 120.50, 101, "Test", "Test Product")

        case "add_test_delivery":
            exit_code = queries.add_delivery(conn, cur, 1, "1890-09-05", "Testing")

        case "update_delivery_status":
            exit_code = queries.update_delivery_status(conn, cur, 1, "Delivered")

        case _:
            print("⚠️ No valid test step selected")

    print(f"Exit with code: {exit_code}")
    return exit_code
