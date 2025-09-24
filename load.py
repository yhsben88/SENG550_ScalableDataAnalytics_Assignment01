'''
# load.py
  Step 2
  Loads original data from provided csv files to database.
'''

import psycopg2
import csv
import os

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

Data_Folder_Dir = "data"
load_csv_to_table(os.path.join(Data_Folder_Dir,"customers.csv"), "customers", ["name", "email", "phone", "address"])
load_csv_to_table(os.path.join(Data_Folder_Dir,"orders.csv"), "orders", ["customer_id","order_date","total_amount","product_id","product_category","product_name"])
load_csv_to_table(os.path.join(Data_Folder_Dir,"deliveries.csv"), "deliveries", ["order_id", "delivery_date", "status"])

if cur:
    cur.close()
if conn:
    conn.close()
    print("PostgreSQL connection closed.")