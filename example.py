import random
from datetime import datetime, timedelta

# Record table information in MySQL and save it as a dict for easy access
TABLE_FIELDS = {
    "transactions": {
        "transaction_id": {"type": "int"},
        "transaction_qty": {"type": "float"},
        "transaction_date": {"type": "date", "range": ("2023-01-01", "2023-12-31")},
        "store_id": {"type": "int", "foreign_key": "stores.store_id"},
        "product_id": {"type": "int", "foreign_key": "products.product_id"},
    },
    "stores": {
        "store_id": {"type": "int"},
        "store_location": {"type": "string", "values": ["Astoria", "Lower Manhattan", "Hell's Kitchen"]},
    },
    "products": {
        "product_id": {"type": "int"},
        "product_type": {"type": "string", "values": ["Scone", "Brewed Chai tea", "Drip coffee", "Gourmet brewed coffee", "Pastry", "Biscotti"]},
        "product_category": {"type": "string", "values": ["Bakery", "Coffee", "Tea", "Drinking Chocolate"]},
        "unit_price": {"type": "float"},
    },
}

def random_date(start, end):
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    random_days = random.randint(0, (end_date - start_date).days)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")


# Generate corresponding example SQL queries based on the keywords entered by the user
# keyword: string
# tables: list(TABLE_FIELDS.keys())
def generate_sql(keyword, tables):
    query = ""
    explanation = ""

    if keyword.lower() == "join":
        main_table = "transactions"
        join_table_candidates = [
            t for t in tables if any(
                TABLE_FIELDS[main_table].get(f, {}).get("foreign_key", "").startswith(t)
                for f in TABLE_FIELDS[main_table]
            )
        ]
        if not join_table_candidates:
            return "No valid JOIN query could be generated.", "No foreign key relationship found for JOIN."
        join_table = random.choice(join_table_candidates)

        join_condition = None
        for field, details in TABLE_FIELDS[main_table].items():
            if "foreign_key" in details and details["foreign_key"].startswith(join_table):
                foreign_key_field = details["foreign_key"].split(".")[1]
                join_condition = f"{main_table}.{field} = {join_table}.{foreign_key_field}"
                break

        if not join_condition:
            return "No valid JOIN condition found.", "Could not determine JOIN condition."

        field_main = random.choice(list(TABLE_FIELDS[main_table].keys()))
        field_join = random.choice(list(TABLE_FIELDS[join_table].keys()))
        query = f"""SELECT {main_table}.{field_main}, {join_table}.{field_join} FROM {main_table} JOIN {join_table} ON {join_condition};"""
        explanation = (
            f"This query retrieves data by joining '{main_table}' with '{join_table}' "
            f"on the condition '{join_condition}'. It selects '{field_main}' from '{main_table}' "
            f"and '{field_join}' from '{join_table}'."
        )

    if keyword.lower() == "group by":
        table_name = random.choice(['products'])
        fields = TABLE_FIELDS[table_name]
        field = random.choice([f for f in fields if fields[f]["type"] == "string"])
        agg_field = random.choice([f for f in fields if fields[f]["type"] in ["float"]])
        agg_func = random.choice(["SUM", "AVG", "COUNT"])
        query = f"SELECT {field}, {agg_func}({agg_field}) FROM {table_name} GROUP BY {field};"
        explanation = f"This query groups the data by {field} and calculates the {agg_func.lower()} of {agg_field} for each {field}."

    elif keyword.lower() == "having":
        table_name = random.choice(['products'])
        fields = TABLE_FIELDS[table_name]
        field = random.choice([f for f in fields if fields[f]["type"] == "string"])
        agg_field = random.choice([f for f in fields if fields[f]["type"] in ["float"]])
        agg_func = "SUM"
        threshold = random.randint(50, 200)
        query = f"SELECT {field}, {agg_func}({agg_field}) AS total FROM {table_name} GROUP BY {field} HAVING total > {threshold};"
        explanation = f"This query groups the data by {field} and shows only those groups where the {agg_func.lower()} of {agg_field} is greater than {threshold}."

    elif keyword.lower() == "order by":
        table_name = random.choice(['transactions', 'products'])
        fields = TABLE_FIELDS[table_name]
        field = random.choice([f for f in fields if fields[f]["type"] in ["int", "float"]])
        order = random.choice(["ASC", "DESC"])
        query = f"SELECT * FROM {table_name} ORDER BY {field} {order};"
        explanation = f"This query retrieves all records and orders them by {field} in {order.lower()}ending order."

    elif keyword.lower() == "where":
        table_name = random.choice(['products'])
        fields = TABLE_FIELDS[table_name]
        field = random.choice([f for f in fields])
        if fields[field]["type"] == "string" and "values" in fields[field]:
            value = random.choice(TABLE_FIELDS[field]["values"])
            query = f"SELECT * FROM {table_name} WHERE {field} = '{value}';"
            explanation = f"This query retrieves all records where {field} is '{value}'."
        elif fields[field]["type"] == "int":
            value = random.randint(1, 100)
            query = f"SELECT * FROM {table_name} WHERE {field} > {value};"
            explanation = f"This query retrieves all records where {field} is greater than {value}."
        elif fields[field]["type"] == "float":
            value = round(random.uniform(1.0, 100.0), 2)
            query = f"SELECT * FROM {table_name} WHERE {field} < {value};"
            explanation = f"This query retrieves all records where {field} is less than {value}."
        elif fields[field]["type"] == "date" and "range" in fields[field]:
            start_date, end_date = TABLE_FIELDS[field]["range"]
            value = random_date(start_date, end_date)
            query = f"SELECT * FROM {table_name} WHERE {field} = '{value}';"
            explanation = f"This query retrieves all records where {field} is '{value}'."

    elif keyword.lower() == "limit":
        table_name = random.choice(tables)
        limit_value = random.randint(1, 10) 
        query = f"SELECT * FROM {table_name} LIMIT {limit_value};"
        explanation = f"This query retrieves the first {limit_value} records from the {table_name} table."

    elif keyword.lower() == "avg":
        table_name = random.choice(['products'])
        fields = TABLE_FIELDS[table_name]
        field = random.choice([f for f in fields if fields[f]["type"] == "float"])
        group_by_field = random.choice([f for f in fields if fields[f]["type"] == "string"])
        query = f"SELECT {group_by_field}, AVG({field}) AS average_{field} FROM {table_name} GROUP BY {group_by_field};"
        explanation = f"This query groups the data by {group_by_field} and calculates the average of {field} for each {group_by_field}."

    elif keyword.lower() == "sum":
        table_name = random.choice(['products'])
        fields = TABLE_FIELDS[table_name]
        field = random.choice([f for f in fields if fields[f]["type"] == "float"])
        group_by_field = random.choice([f for f in fields if fields[f]["type"] == "string"])
        query = f"SELECT {group_by_field}, SUM({field}) AS total_{field} FROM {table_name} GROUP BY {group_by_field};"
        explanation = f"This query groups the data by {group_by_field} and calculates the sum of {field} for each {group_by_field}."

    return query.strip(), explanation


def generate_example_queries(user_input):
    keyword_list = ['group by', 'having', 'order by', 'where', 'limit', 'avg', 'sum', 'join']
    example_queries = []
    tables = list(TABLE_FIELDS.keys())

    matched_keywords = [keyword for keyword in keyword_list if keyword in user_input.lower()]
    
    if matched_keywords:
        for keyword in matched_keywords:
            for _ in range(3):
                query, explanation = generate_sql(keyword, tables)
                example_queries.append((query, explanation))
    else:
        for _ in range(3):
            keyword = random.choice(keyword_list)
            query, explanation = generate_sql(keyword, tables)
            example_queries.append((query, explanation))

    print("\nHere are some example SQL queries with explanations:\n")
    for query, description in example_queries:
        print(f"Query: {query}\nExplanation: {description}\n")