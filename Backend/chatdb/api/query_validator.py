# This file contains functions for validating the SQL and MongoDB queries, and it’s essential for the safety of the queries.

# check if it's a valid SQL query
import re

# Allowed SQL operations
ALLOWED_SQL_COMMANDS = {"select", "insert", "update", "delete"}
DANGEROUS_SQL_KEYWORDS = {"drop", "truncate", "alter", "exec", "union"}




def validate_sql(query):
    if not query or not isinstance(query, str):
        return False

    query_cleaned = query.strip().lower()


    if query_cleaned.endswith(";"):
        query_cleaned = query_cleaned[:-1].strip()

    print("🔥 validate_sql cleaned query:", query_cleaned)

    allowed_cmds = {"select", "insert", "update", "delete"}
    if not any(query_cleaned.startswith(cmd) for cmd in allowed_cmds):
        return False

    risky_keywords = {"drop", "truncate", "alter", "exec", "union"}
    if any(bad_kw in query_cleaned for bad_kw in risky_keywords):
        return False

    if '--' in query_cleaned or '/*' in query_cleaned or '*/' in query_cleaned:
        return False

    return True




def check_sql_references(query):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
            valid_tables = {row[0] for row in cursor.fetchall()}

            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema='public';")
            valid_columns = {row[0] for row in cursor.fetchall()}

        tokens = query.lower().replace(",", " ").split()
        referenced_tables = [t for t in tokens if t in valid_tables]

        if "from" in tokens and not referenced_tables:
            return False

        return True

    except Exception as e:
        print(f"[SQL Ref Check Failed]: {e}")
        return True  # Fail-open


def validate_mongo(query):
    if not query or not isinstance(query, dict):
        return False

    action = query.get("action")

    if action == "list_collections":
        return True  # ✅ Allow list_collections directly!

    if action not in ["find", "insertOne", "insertMany", "updateOne", "updateMany","deleteOne", "deleteMany", "aggregate", "list_collections"]:
        return False

    if action == "aggregate":
        pipeline = query.get("pipeline", [])
        if not isinstance(pipeline, list):
            return False

        allowed_operators = [
            "$match", "$group", "$sort", "$lookup", "$unwind", "$project",
            "$limit", "$skip", "$count", "$addFields", "$set", "$unset",
            "$replaceRoot", "$replaceWith"
        ]

        for stage in pipeline:
            if not isinstance(stage, dict):
                return False
            if len(stage) != 1:
                return False
            op = list(stage.keys())[0]
            if op not in allowed_operators:
                return False

    return True



def log_invalid_query(query, source="unknown"):
    with open("invalid_queries.log", "a") as f:
        f.write(f"[{source}] Invalid query: {query}\n")
