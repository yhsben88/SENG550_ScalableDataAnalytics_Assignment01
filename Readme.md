# Introduction

You will build a simple PostgreSQL-based database system for a store. The database includes
information about customers, orders, and deliveries. You will:

1. Create the schema and load data from provided CSV files
2. Use Python to interact with the database via dynamic queries and data manipulation
   functions
3. Write SQL queries to extract insights from the database

# Pre-installations & Installations

Read `venv-setup/README.md` and follow `steps 1 - 4` for virtual environment setup. Then follow to following code in `step 5` to recreate the environment:

```bash
# Copy code
pip install -r requirements.txt
```

# Walkthrough

Note: All screenshots for proof of execution have been included in the `screenshots/` folder

## Step 1 : Creating Tables for Schema

The following DML query is manually inserted through postgresql IDE `Postico 2`

```sql
CREATE TABLE customers (
customer_id SERIAL PRIMARY KEY
,NAME TEXT
,email TEXT
,phone TEXT
,address TEXT
);
CREATE TABLE orders (
order_id SERIAL PRIMARY KEY
,customer_id INT REFERENCES customers(customer_id)
,order_date DATE
,total_amount NUMERIC
,product_id INT
,product_category TEXT
,product_name TEXT
);
CREATE TABLE deliveries (
delivery_id SERIAL PRIMARY KEY
,order_id INT REFERENCES orders(order_id)
,delivery_date DATE
,STATUS TEXT
);
```

## Step 2 : Load CSV into database

`main.py` uses a function in `load.py` to load csv files located in `data/` into the postgresql database.

To load the csv files,
In `main.py` go to the following code block and change `load_initial_data = False` to `load_initial_data = True`:

```python
""" Step 2 """
load_initial_data = False
if load_initial_data:
    Data_Folder_Dir = "data"
    load_csv_to_table(conn, cur, os.path.join(Data_Folder_Dir,"customers.csv"), "customers", ["name", "email", "phone", "address"])
    load_csv_to_table(conn, cur, os.path.join(Data_Folder_Dir,"orders.csv"), "orders", ["customer_id","order_date","total_amount","product_id","product_category","product_name"])
    load_csv_to_table(conn, cur, os.path.join(Data_Folder_Dir,"deliveries.csv"), "deliveries", ["order_id", "delivery_date", "status"])
    print(f"✅ Loaded original dataset.")
```

Change `load_initial_data = True` back to `load_initial_data = False` after successful execution to prevent duplication of data loading.

## Step 3 : Add and Update Data with Python Functions

### Step 3.A Writing Python DML Queries

Query functions are written in `queries.py`

### step 3.B Use python written DML Queries

Queries are run by `main.py` using query functions written in `queries.py`

## Step 4 : Perform Analytic Queries through Postico 2 IDE

DML & DDL queries in `queries-used.sql` are performed in `postico 2 IDE` on the postgresql database. Corresponding results are located in the `screenshots/` folder.

## Step 5 : Expanding the Schema

Located in the `expanding-schema/` folder is a ReadMe `.md` file describing the schema expansion & a `.sql` file containing the corresponding DCL Query for creating the tables.

## Others

The Assignment `pdf` Handout is located in the `assignment-resources` folder.

Testing for step 3.A is available. `main.py` uses `test.py` for testing purposes of python queries.

Navigate to the following block code in `main.py` and change `test.perform_test(conn, cur)` to e.g. `test.perform_test(conn, cur, 1)`, to perform tests corresponding to the python DQL queries.

```python
""" Test Step 3A : Add & Update queries """
test.perform_test(conn, cur)
```
