# This file handles database interactions with PostgreSQL.

from django.db import connection

def run_sql_query(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        if cursor.description:  # This means it’s a SELECT query
            columns = [col[0] for col in cursor.description]  # Get column names
            return [dict(zip(columns, row)) for row in cursor.fetchall()]  # Return result as a list of dicts
        return {"status": "success"}  # Return success for non-SELECT queries


# Schema Exploration Functions
# Show all tables in our database
def list_tables():
    sql = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """
    return run_sql_query(sql)

# View table attributes
def describe_table(table_name):
    sql = f"""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
        ORDER BY ordinal_position;
    """
    return run_sql_query(sql)

# Get sample data
def sample_rows(table_name, limit=5):
    sql = f"SELECT * FROM {table_name} LIMIT {limit};"
    return run_sql_query(sql)


# Data Modification Functions
# Insert data into our table
def insert_into_table(table_name, column_values: dict):
    cols = ', '.join(column_values.keys())
    placeholders = ', '.join(['%s'] * len(column_values))
    values = list(column_values.values())

    sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders});"
    with connection.cursor() as cursor:
        cursor.execute(sql, values)
    return {"status": "inserted"}

# Update our table information
def update_table(table_name, set_values: dict, where_clause: str):
    set_exprs = ', '.join([f"{k} = %s" for k in set_values.keys()])
    values = list(set_values.values())

    sql = f"UPDATE {table_name} SET {set_exprs} WHERE {where_clause};"
    with connection.cursor() as cursor:
        cursor.execute(sql, values)
    return {"status": "updated"}

# Delete a record from our table
def delete_from_table(table_name, where_clause):
    sql = f"DELETE FROM {table_name} WHERE {where_clause};"
    with connection.cursor() as cursor:
        cursor.execute(sql)
    return {"status": "deleted"}


# Special handler: Auto-increment payment_id for inserts into payment
def insert_into_payment_auto_id(column_values: dict):
    with connection.cursor() as cursor:
        cursor.execute("SELECT MAX(payment_id) FROM payment;")
        max_id = cursor.fetchone()[0] or 0
        new_id = max_id + 1

        # Prepend payment_id to the insert
        full_data = {"payment_id": new_id, **column_values}
        cols = ', '.join(full_data.keys())
        placeholders = ', '.join(['%s'] * len(full_data))
        values = list(full_data.values())

        sql = f"INSERT INTO payment ({cols}) VALUES ({placeholders});"
        cursor.execute(sql, values)

    return {
        "status": "inserted",
        "record": full_data
    }



