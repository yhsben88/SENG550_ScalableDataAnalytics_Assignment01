'''
  File: main.py
'''

import psycopg2
import os
import test
import queries
from load import load_csv_to_table
import sys



if __name__ == "__main__":
    try:
        with psycopg2.connect(
                dbname="storedb",
                user="ben",
                password="",
                host="localhost", 
                port="5432"
        ) as conn:
            print("Connected to PostgreSQL successfully!")
            with conn.cursor() as cur:
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
                test.perform_test(conn, cur)
                
                """ Step 3B """
                # 1. Add customer: Liam Nelson
                liam_id = queries.add_customer(conn, cur, "Liam Nelson", "liam.nelson@example.com", "555-2468", "111 Elm Street")
                if liam_id:
                    print(f"✅ Added customer Liam Nelson with ID {liam_id}")
                else: 
                    print(f"❌ Error with Adding customer Liam Nelson")
                    sys.exit(1)

                # 2. Add order for Liam
                liam_order_id = queries.add_order(conn, cur, liam_id, "2025-06-01", 180.00, 116, "Electronics", "Bluetooth Speaker")
                if cur:
                    print(f"✅ Added order for Liam with ID {liam_order_id}")
                else: 
                    print(f"❌ Error with Adding order for Liam Nelson")
                    sys.exit(1)

                # 3. Add delivery for Liam’s order
                liam_delivery_id = queries.add_delivery(conn, cur, liam_order_id, "2025-06-03", "Pending")
                if liam_delivery_id:
                    print(f"✅ Added delivery for Liam with ID {liam_delivery_id}")
                else: 
                    print(f"❌ Error with Adding delivery for Liam Nelson")
                    sys.exit(1)

                # 4. Update Liam’s delivery status to Shipped
                if queries.update_delivery_status(conn, cur, liam_delivery_id, "Shipped"):
                    print(f"✅ Updated delivery {liam_delivery_id} status to Shipped")
                else:
                    print(f"❌ Error with Updating delivery {liam_delivery_id} status to Shipped")
                    sys.exit(1)

                # 5. Add another customer, order, and delivery
                anna_id = queries.add_customer(conn, cur, "Anna Smith", "anna.smith@example.com", "555-9999", "222 Oak Avenue")
                if anna_id:
                    print(f"✅ Added customer Anna Smith with ID {anna_id}")
                else:
                    print(f"❌ Error Adding customer Anna")
                    sys.exit(1)

                anna_order_id = queries.add_order(conn, cur, anna_id, "2025-06-05", 250.00, 120, "Home", "Vacuum Cleaner")
                if anna_order_id:
                    print(f"✅ Added order for Anna with ID {anna_order_id}")
                else:
                    print(f"❌ Error Adding order for Anna")
                    sys.exit(1)

                anna_delivery_id = queries.add_delivery(conn, cur, anna_order_id, "2025-06-08", "Pending")
                if anna_delivery_id:
                    print(f"✅ Added delivery for Anna with ID {anna_delivery_id}")
                else:
                    print(f"❌ Error Adding delivery for Anna")
                    sys.exit(1)

                # 6. Update delivery_id = 3 to Delivered
                if queries.update_delivery_status(conn, cur, 3, "Delivered"):
                    print("✅ Updated delivery 3 status to Delivered")
                else: 
                    print(f"❌ Error Updating delivery 3 status to Delivered")
                    sys.exit(1)

                """Successful Execution"""
                conn.commit()
                exit(0)
    except psycopg2.Error as e:
        print(f"❌ Error connecting to PostgreSQL: {e}")
        sys.exit(1)


                