# Need to run once on the main thread when creating database tables
# You can find dataset in kaggle
# https://www.kaggle.com/datasets/ahmedabbas757/coffee-sales
# Manually split the data of the 'Coffee_shop_stales' table into three tables: 'Stores', 'Products', and 'Transactions', 
# to meet the testing requirements of the 'join' statement
# The file will be called in the future to implement the function of uploading and updating data


import mysql.connector
import csv
from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from mysql_conn import connect_to_database

# CREATE TABLE Stores (
#     store_id INT PRIMARY KEY,
#     store_location VARCHAR(255) NOT NULL
# );

# CREATE TABLE Products (
#     product_id INT PRIMARY KEY,
#     product_detail VARCHAR(255),
#     product_type VARCHAR(255),
#     product_category VARCHAR(255),
#     unit_price DECIMAL(10, 2)
# );

# CREATE TABLE Transactions (
#     transaction_id INT PRIMARY KEY,
#     transaction_date DATE NOT NULL,
#     transaction_time TIME NOT NULL,
#     transaction_qty INT NOT NULL,
#     store_id INT,
#     product_id INT,
#     FOREIGN KEY (store_id) REFERENCES Stores(store_id),
#     FOREIGN KEY (product_id) REFERENCES Products(product_id)
# );

# Create the table structure of the database, theoretically only run once in main
def create_tables():
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Stores (
                store_id INT PRIMARY KEY,
                store_location VARCHAR(255) NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                product_id INT PRIMARY KEY,
                product_detail VARCHAR(255),
                product_type VARCHAR(255),
                product_category VARCHAR(255),
                unit_price DECIMAL(10, 2)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Transactions (
                transaction_id INT PRIMARY KEY,
                transaction_date DATE NOT NULL,
                transaction_time TIME NOT NULL,
                transaction_qty INT NOT NULL,
                store_id INT,
                product_id INT,
                FOREIGN KEY (store_id) REFERENCES Stores(store_id),
                FOREIGN KEY (product_id) REFERENCES Products(product_id)
            );
        """)
        connection.commit()
        print("Tables created successfully.")
    finally:
        cursor.close()
        connection.close()

FIELD_VALIDATORS = {
    "store_id": int,
    "store_location": str,
    "product_id": int,
    "product_detail": str,
    "product_type": str,
    "product_category": str,
    "unit_price": float,
    "transaction_id": int,
    "transaction_date": lambda x: datetime.strptime(x, '%m/%d/%Y'),
    "transaction_time": lambda x: datetime.strptime(x, '%H:%M:%S'),
    "transaction_qty": int,
}

def validate_field_names(csv_fieldnames):
    expected_fieldnames = set(FIELD_VALIDATORS.keys())
    csv_fieldnames_set = set(csv_fieldnames)
    
    if csv_fieldnames_set != expected_fieldnames:
        missing_fields = expected_fieldnames - csv_fieldnames_set
        extra_fields = csv_fieldnames_set - expected_fieldnames
        error_message = []
        if missing_fields:
            error_message.append(f"Missing fields: {', '.join(missing_fields)}")
        if extra_fields:
            error_message.append(f"Unexpected fields: {', '.join(extra_fields)}")
        raise ValueError("Field name validation failed. " + "; ".join(error_message))
    return True

def validate_row(row):
    for field, validator in FIELD_VALIDATORS.items():
        if field in row:
            value = row[field]
            try:
                validator(value)
            except Exception as e:
                print(f"Validation error for field '{field}' with value '{value}': {e}")
                return False
    return True

def format_date(date_str):
    return datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')

def insert_data(csv_file):
    connection = connect_to_database()
    cursor = connection.cursor()
    try:
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)

            validate_field_names(reader.fieldnames)
            print("Field names validation passed.")

            for row in reader:
                if not validate_row(row):
                    print(f"Skipping row: {row}")
                    continue

                cursor.execute("""
                    INSERT IGNORE INTO Stores (store_id, store_location)
                    VALUES (%s, %s)
                """, (row['store_id'], row['store_location']))

                cursor.execute("""
                    INSERT IGNORE INTO Products (product_id, product_detail, product_type, product_category, unit_price)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    row['product_id'],
                    row['product_detail'],
                    row['product_type'],
                    row['product_category'],
                    row['unit_price']
                ))

                cursor.execute("""
                    INSERT INTO Transactions (transaction_id, transaction_date, transaction_time, transaction_qty, store_id, product_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    row['transaction_id'],
                    format_date(row['transaction_date']),
                    row['transaction_time'],
                    row['transaction_qty'],
                    row['store_id'],
                    row['product_id']
                ))
        connection.commit()
        print("Data inserted successfully.")
    finally:
        cursor.close()
        connection.close()

def upload_csv():
    print("Please select a CSV file...")
    root = Tk()
    root.withdraw() 
    root.attributes("-topmost", True)
    csv_file_path = askopenfilename(
        title="Select CSV file",
        filetypes=[("CSV file", "*.csv"), ("All files", "*.*")]
    )
    if not csv_file_path:
        print("No file selected. Exiting.")
        return
    try:
        insert_data(csv_file_path)
    except ValueError as e:
        print(f"Unexpected error: {e}")
        print("Please try selecting another file.")
        # if csv_file_path:
        #     print(f"The file you selected is: {csv_file_path}")
        #     insert_data(csv_file_path)
        # else:
        #     print("No selected file.")

if __name__ == "__main__":
    create_tables()
    csv_file_path = 'data/coffee_shop_sales_test.csv'
    insert_data(csv_file_path)