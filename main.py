import mysql.connector
import re

from mysql_conn import execute_sql_tables_query, execute_sql_query
from example import generate_example_queries
from nlp import parse_user_input
from upload import upload_csv

def is_valid_sql_query(user_input):
    user_input = user_input.strip()
    
    if not user_input:
        return False
    
    sql_keywords = [
        'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 
        'ALTER', 'TRUNCATE', 'GRANT', 'REVOKE', 'COMMIT', 'ROLLBACK'
    ]
    if not any(user_input.upper().startswith(keyword) for keyword in sql_keywords):
        return False
    
    sql_pattern = re.compile(
        r"^\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER|TRUNCATE|GRANT|REVOKE|COMMIT|ROLLBACK)\s+.+",
        re.IGNORECASE
    )
    if not sql_pattern.match(user_input):
        return False
    
    common_clauses = ['FROM', 'WHERE', 'SET', 'VALUES', 'TABLE']
    if not any(clause in user_input.upper() for clause in common_clauses):
        return False

    return True

def show_table_structure(table_name):
    sql_query = f"DESCRIBE {table_name};"
    structure = execute_sql_tables_query(sql_query)
    print(f"\nThe Structure of Table {table_name}:")
    print("-" * 50)
    for row in structure:
        print(f"Field: {row[0]}, Type: {row[1]}, Is NULL: {row[2]}, Key Type: {row[3]}")
    print("-" * 50)

    sql_query_samples = f"SELECT * FROM {table_name} LIMIT 5;"
    samples = execute_sql_tables_query(sql_query_samples)
    print(f"\nSample Data from Table {table_name}:")
    print("-" * 50)
    if samples:
        field_names = [row[0] for row in structure]
        print("\t".join(field_names))
        print("-" * 50)
        for sample in samples:
            print("\t".join(str(value) if value is not None else "NULL" for value in sample))
    else:
        print("No sample data available (table is empty).")
    print("-" * 50)


def main():
    print("-----")
    print("    ")
    print("Welcome to ChatDB!")

    print("    ")
    print("-----")
    print("    ")
    print("This is a database that records data related to coffee shop sales.")
    print("You can view the table structure of the relevant data tables through terminal interaction,")
    print("fill in the data according to the requirements of the CSV file, upload it to the system,")
    print("output example SQL, execute relevant legal SQL, and generate SQL query results according to your ideas,")
    print("or you can follow the prompts of the system to operate.")
    print("You can type 'help' to see guildline. Anyway, have fun!")
    print("    ")
    print("-----")
    print("    ")

    while True:
        print("\nPlease select the database:")
        print("1. MySQL")
        
        choice = input("\nEnter your choice (1 to select MySQL): ").strip()

        if choice == "1":
            print("You have selected MySQL.")
            break
        else:
            print("Invalid choice. Please enter number to select database.")
    
    while True:
        user_input = input("\nEnter your query or chat (or type 'exit' to quit): ").strip()

        if user_input.lower() == 'exit':
            print("Exiting the system. Goodbye!")
            break

        elif user_input.lower() == 'help':
            print("    ")
            print("Here is the logic of the system processing user input:")
            print("If the user's input includes 'upload', you will be able to select a pre filled CSV file to upload the data to the system.")
            print("If the user's input includes 'show table', you will be able to view the existing data tables and table structures in the database.")
            print("If the user's input includes 'example', you will be able to get some example SQL from database.")
            print("And you can include some keyword such as 'group by', 'sum' to get specific SQL example.")
            print("IF the user inputs a valid SQL statement, the system will run directly and return the result to you.")
            print("If the above situations are not met, the system will attempt to understand the user's input and obtain corresponding SQL query statements and explanations.")
            print("If the input is incomprehensible to the system, the system will prompt the user to re-enter.")
            print("    ")

        elif 'upload' in user_input.lower():
            upload_csv()

        elif 'example' in user_input.lower():
            generate_example_queries(user_input)

        elif 'show table' in user_input.lower():
            sql_query = "SHOW TABLES;"
            print("Showing available tables:")
            tables = execute_sql_tables_query(sql_query)
            if tables:
                print("\nThe available tables are as follows:")
                for idx, table in enumerate(tables, start=1):
                    print(f"{idx}. {table[0]}")
                
                table_choice = input("\nPlease enter the table number to view the table structure, or enter 'b' to return: ").strip().lower()
                if table_choice.isdigit():
                    table_idx = int(table_choice) - 1
                    if 0 <= table_idx < len(tables):
                        show_table_structure(tables[table_idx][0])
                    else:
                        print("Invalid serial number, please re-enter.")
                elif table_choice == 'b':
                    continue
                else:
                    print("Invalid input, please try again.")
            else:
                print("There are currently no available tables.")

        elif is_valid_sql_query(user_input):
            print("Executing SQL query...")
            execute_sql_query(user_input)

        else:
            sql_query, explanation = parse_user_input(user_input)
            
            if sql_query:
                print(f"Generated SQL: {sql_query}")
                print(f"Explanation: {explanation}")
                print('')
                print("You can directely input valid SQL to retrieval related information.")
                print("Let me know if you'd like further assistance or a different analysis!")
                print("    ")

                user_input = input("Would you like to directly execute this SQL? (yes/else to skip): ").strip().lower()
                if user_input in ['yes', 'y']:
                    execute_sql_query(sql_query)
                else:
                    print("SQL execution skipped. Please enter your next command.")
                # execute_sql_query(sql_query)
            else:
                print("Could not parse the input. Please try again or enter a valid SQL query.")

if __name__ == "__main__":
    main()
