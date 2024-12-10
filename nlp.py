import re

TABLE_STRUCTURE = {
    "transactions": {
        "fields": ["transaction_id", "transaction_date", "transaction_time", "transaction_qty", "store_id", "product_id"]
    },
    "products": {
        "fields": ["product_id", "product_detail", "product_type", "product_category", "unit_price"]
    },
    "stores": {
        "fields": ["store_id", "store_location"]
    }
}

TABLE_FIELDS = {
    "sales": {
        "field": "transactions.transaction_qty * products.unit_price",
        "tables": ["transactions", "products"],
        "new": True,
    },
    # "sales quantity": {
    #     "field": "SUM(transactions.transaction_qty)",
    #     "tables": ["transactions"]
    # },
    # "sales day": {
    #     "field": "transactions.transaction_date, transactions.transaction_qty * products.unit_price",
    #     "tables": ["transactions", "products"]
    # },
    # "sales time": {
    #     "field": "transactions.transaction_time, transactions.transaction_qty * products.unit_price",
    #     "tables": ["transactions", "products"]
    # },
    # "sales quantity": "SUM(transactions.transaction_qty)",
    # "sales day": "transactions.transaction_date, SUM(transactions.transaction_qty * products.unit_price)",
    # "sales time": "transactions.transaction_time, SUM(transactions.transaction_qty * products.unit_price)",
    "day": {
        "field": "transaction_date",
        "tables": ["transactions"]
    },
    "date": {
        "field": "transaction_date",
        "tables": ["transactions"]
    },
    "time": {
        "field": "transaction_time",
        "tables": ["transactions"]
    },
    "product id": {
        "field": "product_id",
        "tables": ["products"]
    },
    "product category": {
        "field": "product_category",
        "tables": ["products"]
    },
    "type": {
        "field": "product_type",
        "tables": ["products"]
    },
    "product type": {
        "field": "product_type",
        "tables": ["products"]
    },
    "product detail": {
        "field": "product_detail",
        "tables": ["products"]
    },
    "unit price": {
        "field": "unit_price",
        "tables": ["products"]
    },
    "price": {
        "field": "unit_price",
        "tables": ["products"]
    },
    "transaction": {
        "field": "transaction_id",
        "tables": ["transactions"]
    },
    "transaction id": {
        "field": "transaction_id",
        "tables": ["transactions"]
    },
    "transaction date": {
        "field": "transaction_date",
        "tables": ["transactions"]
    },
    "transaction time": {
        "field": "transaction_time",
        "tables": ["transactions"]
    },
    "transaction quantity": {
        "field": "transaction_qty",
        "tables": ["transactions"]
    },
    "store": {
        "field": "store_location",
        "tables": ["stores"]
    },
    "store id": {
        "field": "store_id",
        "tables": ["stores"]
    },
    "location": {
        "field": "store_location",
        "tables": ["stores"]
    },
    "store location": {
        "field": "store_location",
        "tables": ["stores"]
    },
    "product": {
        "field": "product_detail",
        "tables": ["products"]
    },
    # "product category": "product_category",
    # "product type": "product_type",
    # "product detail": "product_detail",
    # "transaction id": "transaction_id",
    # "transaction date": "transaction_date",
    # "transaction time": "transaction_time",
    # "store": "store_location",
    # "location": "store_location",
    # "product": "product_detail",
    # "store location": "store_location",
}

PATTERN_SQL_MAP = {
    r"total (.+) by (.+)": "SELECT {field2}, {field3}SUM({field1}) AS total FROM {table} GROUP BY {field3}{field2};",
    r"count (.+) by (.+)": "SELECT {field2}, {field3}COUNT({field1}) AS count FROM {table} GROUP BY {field3}{field2};",
    r"average (.+) by (.+)": "SELECT {field2}, {field3}AVG({field1}) AS average FROM {table} GROUP BY {field3}{field2};",
    r"max (.+) by (.+)": "SELECT {field2}, {field3}SUM({field1}) AS total FROM {table} GROUP BY {field3}{field2} ORDER BY total DESC LIMIT 1;",
    r"min (.+) by (.+)": "SELECT {field2}, {field3}SUM({field1}) AS total FROM {table} GROUP BY {field3}{field2} ORDER BY total LIMIT 1;",
    r"top (\d+) (.+) by (.+)": "SELECT {field2}, {field3}SUM({field1}) AS total FROM {table} GROUP BY {field3}{field2} ORDER BY total DESC LIMIT {n};",
    r"filter (.+) where (.+)": "SELECT * FROM {table} WHERE {field1} = '{value}';",
    r"filter (.+) where (\d+)": "SELECT * FROM {table} WHERE {field1} = {value};",
    # r"find (.+) where (.+)": "SELECT * FROM {table} WHERE {field1} = '{value}';",
    r"highest (.+) for (.+)": "SELECT {field2}, {field3}SUM({field1}) AS total FROM {table} GROUP BY {field3}{field2} ORDER BY total DESC;",
    r"lowest (.+) for (.+)": "SELECT {field2}, {field3}SUM({field1}) AS total FROM {table} GROUP BY {field3}{field2} ORDER BY total;",

    r"total (.+) by (.+)_join": "SELECT {field2}, {field3}SUM({field1}) AS total FROM {table1} JOIN {table2} ON {join_condition} GROUP BY {field3}{field2};",
    r"count (.+) by (.+)_join": "SELECT {field2}, {field3}COUNT({field1}) AS count FROM {table1} JOIN {table2} ON {join_condition} GROUP BY {field3}{field2};",
    r"average (.+) by (.+)_join": "SELECT {field2}, {field3}AVG({field1}) AS average FROM {table1} JOIN {table2} ON {join_condition} GROUP BY {field3}{field2};",
    r"max (.+) by (.+)_join": "SELECT {field2}, {field3}MAX({field1}) AS max FROM {table1} JOIN {table2} ON {join_condition} GROUP BY {field3}{field2};",
    r"min (.+) by (.+)_join": "SELECT {field2}, {field3}MIN({field1}) AS min FROM {table1} JOIN {table2} ON {join_condition} GROUP BY {field3}{field2};",
    r"top (\d+) (.+) by (.+)_join": "SELECT {field2}, {field3}SUM{field1} AS total FROM {table1} JOIN {table2} ON {join_condition} GROUP BY {field3}{field2} ORDER BY total DESC LIMIT {n};",
    r"filter (.+) where (.+)_join": "SELECT {field1}, {field2} FROM {table1} JOIN {table2} ON {join_condition} WHERE {filter_condition};",
    r"filter (.+) where (\d+)_join": "SELECT {field1}, {field2} FROM {table1} JOIN {table2} ON {join_condition} WHERE {filter_condition};",
    # r"find (.+) where (.+)_join": "SELECT {field1}, {field2} FROM {table1} JOIN {table2} ON {join_condition} WHERE {filter_condition};",
    r"highest (.+) for (.+)_join": "SELECT {field2}, {field3}SUM({field1}) AS total FROM {table1} JOIN {table2} ON {join_condition} GROUP BY {field3}{field2} ORDER BY total DESC;",
    r"lowest (.+) for (.+)_join": "SELECT {field2}, {field3}SUM({field1}) AS total FROM {table1} JOIN {table2} ON {join_condition} GROUP BY {field3}{field2} ORDER BY total;",

    r"total (.+) by (.+)_join3": "SELECT {field2}, {field3}SUM({field1}) AS total FROM {join_condition} GROUP BY {field3}{field2};",
    r"count (.+) by (.+)_join3": "SELECT {field2}, {field3}COUNT({field1}) AS count FROM {join_condition} GROUP BY {field3}{field2};",
    r"average (.+) by (.+)_join3": "SELECT {field2}, {field3}AVG({field1}) AS average FROM {join_condition} GROUP BY {field3}{field2};",
    r"max (.+) by (.+)_join3": "SELECT {field2}, {field3}MAX({field1}) AS max FROM {join_condition} GROUP BY {field3}{field2};",
    r"min (.+) by (.+)_join3": "SELECT {field2}, {field3}MIN({field1}) AS min FROM {join_condition} GROUP BY {field3}{field2};",
    r"top (\d+) (.+) by (.+)_join3": "SELECT {field2}, {field3}SUM{field1} AS total FROM {join_condition} GROUP BY {field3}{field2} ORDER BY total DESC LIMIT {n};",
    r"filter (.+) where (.+)_join3": "SELECT {field1}, {field2} FROM {join_condition} WHERE {filter_condition};",
    r"filter (.+) where (\d+)_join3": "SELECT {field1}, {field2} FROM {join_condition} WHERE {filter_condition};",
    # r"find (.+) where (.+)_join3": "SELECT {field1}, {field2} FROM {join_condition} WHERE {filter_condition};",
    r"highest (.+) for (.+)_join3": "SELECT {field2}, {field3}SUM({field1}) AS total FROM {join_condition} GROUP BY {field3}{field2} ORDER BY total DESC;",
    r"lowest (.+) for (.+)_join3": "SELECT {field2}, {field3}SUM({field1}) AS total FROM {join_condition} GROUP BY {field3}{field2} ORDER BY total;",
}

FOREIGN_KEYS = {
    "transactions": {
        "store_id": "stores.store_id",
        "product_id": "products.product_id"
    }
}

def extract_matching_values(input_string, table_fields):
    input_string = input_string.lower()
    matched_values = []

    sorted_keys = sorted(table_fields.keys(), key=len, reverse=True)

    for key in sorted_keys:
        if key.lower() in input_string:
            matched_values.append(table_fields[key])
            input_string = input_string.replace(key.lower(), "", 1)

    return matched_values

def merge_fields_and_deduplicate_tables(data):
    merged_fields = []
    for item in data:
        if 'field' in item:
            if 'new' not in item:
                prefix = item['tables'][0] + '.' if 'tables' in item and item['tables'] else ''
                merged_fields.append(f"{prefix}{item['field']}")
            else:
                merged_fields.append(item['field'])

    merged_fields_str = ", ".join(merged_fields)

    return merged_fields_str

def merge_fields(data1, data2):
    field1, field2, field3 = '', '', ''
    if len(data1) == 2:
        for i, item in enumerate(data1):
            if 'field' in item and len(item['tables']) > 1:
                if 'new' not in item:
                    prefix = item['tables'][0] + '.' if 'tables' in item and item['tables'] else ''
                    if field1:
                        field3 = f"{prefix}{item['field']}, "
                    else:
                        field1 = f"{prefix}{item['field']}"
                else:
                    if field1:
                        field3 = f"{item['field']}, "
                    else:
                        field1 = f"{item['field']}"
            elif 'field' in item and len(item['tables']) == 1:
                if 'new' not in item:
                    prefix = item['tables'][0] + '.' if 'tables' in item and item['tables'] else ''
                    if not field1:
                        field1 = f"{prefix}{item['field']}"
                    else:
                        field3 = f"{prefix}{item['field']}, "
                else:
                    if not field1:
                        field1 = f"{item['field']}, "
                    else:
                        field3 = f"{item['field']}, "
    else:
        if 'new' not in data1[0]:
            prefix = data1[0]['tables'][0] + '.' if 'tables' in data1[0] and data1[0]['tables'] else ''
            field1 = f"{prefix}{data1[0]['field']}"
        else:
            field1 = f"{data1[0]['field']}"
    
    if 'new' not in data2[0]:
        prefix = data2[0]['tables'][0] + '.' if 'tables' in data2[0] and data2[0]['tables'] else ''
        field2 = f"{prefix}{data2[0]['field']}"
    else:
        field2 = f"{data2[0]['field']}"
    return field1, field2, field3

def find_table_for_field(field):
    for table, info in TABLE_STRUCTURE.items():
        if field in info["fields"]:
            return table
    return None

def find_join_condition(table1, table2):
    """Find the join condition between two tables based on foreign key definitions."""
    if table1 in FOREIGN_KEYS:
        for key, ref in FOREIGN_KEYS[table1].items():
            ref_table, ref_field = ref.split('.')
            if ref_table == table2:
                return f"{table1}.{key} = {table2}.{ref_field}"
    if table2 in FOREIGN_KEYS:
        for key, ref in FOREIGN_KEYS[table2].items():
            ref_table, ref_field = ref.split('.')
            if ref_table == table1:
                return f"{table2}.{key} = {table1}.{ref_field}"
    return None


def parse_user_input(user_input):
    for pattern, sql_template in PATTERN_SQL_MAP.items():
        match = re.search(pattern, user_input.lower(), re.IGNORECASE)
        if match:
            groups = match.groups()
            # print(groups)
            
            if len(groups) == 3:  # for "top N <A> by <B>" pattern
                n = groups[0]
                field1, field2 = groups[1], groups[2]
            elif len(groups) == 2:
                field1, field2 = groups

            field1_val = extract_matching_values(field1, TABLE_FIELDS)
            field2_val = extract_matching_values(field2, TABLE_FIELDS)
            # print(field1_val)
            
            # sql_field1_dict = TABLE_FIELDS.get(field1.lower(), field1.lower())
            # sql_field2_dict = TABLE_FIELDS.get(field2.lower(), field2.lower())

            # table_list = list(set(sql_field1_dict["tables"] + sql_field2_dict["tables"]))
            merged_tables = set()
            # merged_field1 = set()
            # merged_field2 = set()
            for item in field1_val:
                if "tables" in item:
                    merged_tables.update(item["tables"])
                # if "field" in item:
                #     merged_field1.update(item["field"])
            for item in field2_val:
                if "tables" in item:
                    merged_tables.update(item["tables"])
            table_list = list(merged_tables)
            # print(list(merged_tables))
            
            # table_list = list(set(field1_val["tables"] + sql_field2_dict["tables"]))

            # table1 = find_table_for_field(sql_field1)
            # table2 = find_table_for_field(sql_field2)
            # print(sql_field1, sql_field2, table1, table2)

            # if table1 and table2 and table1 == table2:
            if table_list and len(table_list) == 1:
                table = table_list[0]
                # sql_field1 = sql_field1_dict["field"]
                # sql_field2 = sql_field2_dict["field"]
                sql_field1  = ", ".join(item['field'] for item in field1_val if 'field' in item)
                sql_field2  = ", ".join(item['field'] for item in field2_val if 'field' in item)
                sql_field3 = ""
                if '{n}' in sql_template:
                    query = sql_template.format(field1=sql_field1, field2=sql_field2, field3=sql_field3, n=n, table=table)
                    explanation = f"This query retrieves the top {n} records of {field1} grouped by {field2}."
                elif 'filter' in pattern:
                    value = groups[1]
                    query = sql_template.format(field1=sql_field1, value=value, table=table)
                    explanation = f"This query filters the data where {field1} is '{value}'."
                else:
                    first_word = re.match(r"^\w+", pattern).group()
                    query = sql_template.format(field1=sql_field1, field2=sql_field2, field3=sql_field3, table=table)
                    explanation = f"This query groups the data by {field2} and calculates the {first_word} {field1.lower()} for each {field2}."
                
                return query, explanation
            
            # elif table1 and table2 and table1 != table2:
            elif table_list and len(table_list) == 2:
                table1, table2 = table_list[0], table_list[1]
                # sql_field1 = f"{sql_field1_dict['tables'][0]}.{sql_field1_dict['field']}"
                # sql_field2 = f"{sql_field2_dict['tables'][0]}.{sql_field2_dict['field']}"
                # sql_field1 = merge_fields_and_deduplicate_tables(field1_val)
                # sql_field2 = merge_fields_and_deduplicate_tables(field2_val)
                sql_field1, sql_field2, sql_field3 = merge_fields(field1_val, field2_val)
                # print("sql", sql_field1, sql_field2, sql_field3)

                join_condition = find_join_condition(table1, table2)
                if not join_condition:
                    return None, f"No join condition found between {table1} and {table2}."

                join_pattern = pattern + "_join"
                if join_pattern in PATTERN_SQL_MAP:
                    join_template = PATTERN_SQL_MAP[join_pattern]
                    if '{n}' in join_template:
                        query = join_template.format(field1=sql_field1, field2=sql_field2, field3=sql_field3, n=n, table1=table1, table2=table2, join_condition=join_condition)
                        explanation = f"This query retrieves the top {n} records of {field1} grouped by {field2}, using a JOIN between {table1} and {table2}."
                    elif 'filter' in join_template:
                        filter_condition = groups[1]
                        query = join_template.format(field1=sql_field1, field2=sql_field2, field3=sql_field3, filter_condition=filter_condition, table1=table1, table2=table2, join_condition=join_condition)
                        explanation = f"This query filters the data where {field1} is '{value}', using a JOIN between {table1} and {table2}."
                    else:
                        first_word = re.match(r"^\w+", pattern).group()
                        query = join_template.format(field1=sql_field1, field2=sql_field2, field3=sql_field3, table1=table1, table2=table2, join_condition=join_condition)
                        explanation = f"This query groups the data by {field2} and calculates the {first_word} {field1.lower()} for each {field2}, using a JOIN between {table1} and {table2}."
                        return query, explanation
                else:
                    return None, "No JOIN query template found for the pattern."
            
            elif table_list and len(table_list) == 3:
                join_condition = "transactions JOIN stores ON stores.store_id = transactions.store_id JOIN products ON products.product_id = transactions.product_id"
                # sql_field1 = sql_field1_dict["field"]
                # sql_field2 = f"{sql_field2_dict['tables'][0]}.{sql_field2_dict['field']}"
                sql_field1, sql_field2, sql_field3 = merge_fields(field1_val, field2_val)
                # print("sql", sql_field1, sql_field2, sql_field3)

                join_pattern = pattern + "_join3"
                if join_pattern in PATTERN_SQL_MAP:
                    join_template = PATTERN_SQL_MAP[join_pattern]
                    if '{n}' in join_template:
                        query = join_template.format(field1=sql_field1, field2=sql_field2, field3=sql_field3, n=n, join_condition=join_condition)
                        explanation = f"This query retrieves the top {n} records of {field1} grouped by {field2}, using a JOIN connect transactions, stores and products tables."
                    elif 'filter' in join_template:
                        filter_condition = groups[1]
                        query = join_template.format(field1=sql_field1, field2=sql_field2, field3=sql_field3, filter_condition=filter_condition, join_condition=join_condition)
                        explanation = f"This query filters the data where {field1} is '{value}', using a JOIN connect transactions, stores and products tables."
                    else:
                        first_word = re.match(r"^\w+", pattern).group()
                        query = join_template.format(field1=sql_field1, field2=sql_field2, field3=sql_field3, join_condition=join_condition)
                        explanation = f"This query groups the data by {field2} and calculates the {first_word} {field1.lower()} for each {field2}, using a JOIN connect transactions, stores and products tables."
                        return query, explanation
                else:
                    return None, "No JOIN query template found for the pattern."
            
            else:
                return None, "The fields do not belong to any recognized table."

    return None, None