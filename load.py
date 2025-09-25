'''
  File: load.py
'''

import psycopg2
import csv
import os
import queries

def load_csv_to_table(filename, table_name, columns):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            placeholders = ', '.join(['%s'] * len(columns))
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            values = [row[col] for col in columns]
            try:
                cur.execute(query, values)
            except Exception as e:
                print(f"❌ Error inserting into {table_name}: {e}")
                conn.rollback()
        conn.commit()
        print(f"✅ Loaded data into {table_name}")

if __name__ == "__main__":
    try: 
        conn = psycopg2.connect(
            dbname="storedb",
            user="ben",
            password="",
            host="localhost", 
            port="5432" 
        )
        print("Connected to PostgreSQL successfully!")
    except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL: {e}")
            conn = None
    if conn:
        cur = conn.cursor()

    """ Step 2 """
    load_initial_data = False
    if load_initial_data:
        Data_Folder_Dir = "data"
        load_csv_to_table(os.path.join(Data_Folder_Dir,"customers.csv"), "customers", ["name", "email", "phone", "address"])
        load_csv_to_table(os.path.join(Data_Folder_Dir,"orders.csv"), "orders", ["customer_id","order_date","total_amount","product_id","product_category","product_name"])
        load_csv_to_table(os.path.join(Data_Folder_Dir,"deliveries.csv"), "deliveries", ["order_id", "delivery_date", "status"])
        print(f"✅ Loaded original dataset.")
    
    """ Step 3 """
    # Map numbers to step names
    step_dict = {
        1: "add_a_test_customer",
        2: "add_a_test_order",
        3: "add_a_test_delivery",
        4: "update_a_delivery_status"
    }

    # Pick the step number
    active_step_number = 0  # change this number to choose a step
    active_step = step_dict.get(active_step_number, None)
    if active_step:
        print("performing operation: "+ active_step)
    exit_code = -1 
    match active_step:
        case "add_a_test_customer":
            exit_code = queries.add_customer(conn, cur, "Test Subject", "test@gmail.com", "999-9999", "99 fake road")

        case "add_a_test_order":
            exit_code = queries.add_order(conn, cur, 1, "2020-12-14", 120.50, 101, "Test", "Test")

        case "add_a_test_delivery":
            exit_code = queries.add_delivery(conn, cur, 1, "1890-09-05", "Testing")

        case "update_a_delivery_status":
            exit_code = queries.update_delivery_status(conn, cur, 1, "Delivered")

        case _:
            print("⚠️ No valid step selected")
            

    print("Exit with code : " + str(exit_code))
    
    """ Clean up """
    if cur:
        cur.close()
    if conn:
        conn.close()
        print("PostgreSQL connection closed.")