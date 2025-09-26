from psycopg2.extensions import connection, cursor
import csv
def load_csv_to_table(conn:connection, cur:cursor, filename, table_name, columns):
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
        print(f"✅ Loaded data into {table_name}")