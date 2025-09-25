'''
  File: main.py
'''

import psycopg2
import os
import test
import queries
from load import load_csv_to_table



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

        
    """ Step 1 : Tables created manually with IDE. """

    """ Step 2 """
    load_initial_data = False
    if load_initial_data:
        Data_Folder_Dir = "data"
        load_csv_to_table(conn, cur, os.path.join(Data_Folder_Dir,"customers.csv"), "customers", ["name", "email", "phone", "address"])
        load_csv_to_table(conn, cur, os.path.join(Data_Folder_Dir,"orders.csv"), "orders", ["customer_id","order_date","total_amount","product_id","product_category","product_name"])
        load_csv_to_table(conn, cur, os.path.join(Data_Folder_Dir,"deliveries.csv"), "deliveries", ["order_id", "delivery_date", "status"])
        print(f"✅ Loaded original dataset.")
    
    """ Test Step 3A : Add & Update queries """
    # test.perform_test(conn, cur)
    
    """ Step 3B """


    """ Clean up """
    if cur:
        cur.close()
    if conn:
        conn.close()
        print("PostgreSQL connection closed.")