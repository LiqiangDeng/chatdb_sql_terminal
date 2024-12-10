# The operation of this file has been abandoned
# We have modified the data used by chatDB, and this is an old version
# We previously used coffee_shop_sales, car_data，advertising_and_sales table
# You can find the corresponding dataset on Kaggle, the link is below
# https://www.kaggle.com/datasets/ahmedabbas757/coffee-sales
# https://www.kaggle.com/datasets/meruvulikith/90000-cars-data-from-1970-to-2024
# https://www.kaggle.com/datasets/ankitkr60/advertisement-and-sales-data-for-analysis
# Due to project requirements, it is preferable for the three tables involved to be related in order to better test the generation of 'joins' operation
# So I discarded this file


import mysql.connector
import csv
from datetime import datetime
from mysql_conn import connect_to_database

# CREATE TABLE coffee_shop_sales (
#     transaction_id INT AUTO_INCREMENT PRIMARY KEY,  
#     transaction_date DATE,                     
#     transaction_time TIME,                
#     transaction_qty INT,                      
#     store_id INT,                            
#     store_location VARCHAR(255),                
#     product_id INT,                        
#     unit_price DECIMAL(10, 2),                   
#     product_category VARCHAR(100),           
#     product_type VARCHAR(100),                  
#     product_detail VARCHAR(255)           
# );

# CREATE TABLE car_data (
#     id INT AUTO_INCREMENT PRIMARY KEY,   
#     model VARCHAR(100),                   
#     year INT,                               
#     price DECIMAL(10, 2),                
#     transmission VARCHAR(50),       
#     mileage INT,          
#     fuelType VARCHAR(50),       
#     tax DECIMAL(10, 2),             
#     mpg DECIMAL(5, 1),     
#     engineSize DECIMAL(3, 1),  
#     manufacturer VARCHAR(100)   
# );

# CREATE TABLE advertising_and_sales (
#     ID INT PRIMARY KEY,            
#     TV DECIMAL(6, 1),              -- in thousands of units
#     Radio DECIMAL(5, 1),           
#     Newspaper DECIMAL(5, 1),      
#     Sales DECIMAL(4, 1)           
# );

def format_date(date_str):
    return datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')

def import_csv_to_table(csv_file_path, table_name):
    connection = connect_to_database()
    cursor = connection.cursor()

    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        csv_data = csv.reader(csvfile)
        headers = next(csv_data)

        placeholders = ', '.join(['%s'] * len(headers))
        insert_query = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({placeholders})"

        for row in csv_data:
            row[1] = format_date(row[1])
            cursor.execute(insert_query, row)

    connection.commit()
    cursor.close()
    connection.close()
    print(f"Data from {csv_file_path} has been successfully imported into {table_name}.")

if __name__ == "__main__":
    csv_file_path = "data/coffee_shop_sales.csv"
    table_name = "coffee_shop_sales"

    import_csv_to_table(csv_file_path, table_name)