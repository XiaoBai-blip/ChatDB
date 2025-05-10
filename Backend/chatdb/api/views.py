# Main execution file!!!  business logic for our application!!!

# For handling the logic behind HTTP requests and returning the appropriate HTTP responses. In Django, when a user interacts with your application (e.g., by visiting a URL, submitting a form, or making an API request), the views are responsible for processing these HTTP requests. Each view is linked to a specific URL pattern (defined in urls.py), which means when a user accesses a specific endpoint, a corresponding view function will be triggered. After processing the request, the view generates an HTTP response.

# views interact with databases (PostgreSQL or MongoDB) and external APIs (e.g., Google Gemini) to process requests and return results.


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from bson import ObjectId
from .gemini_models import convert_nl_to_query
from .query_validator import validate_sql, validate_mongo
from .postgres_models import (
    run_sql_query, list_tables, describe_table, sample_rows,
    insert_into_table, update_table, delete_from_table,
    insert_into_payment_auto_id  
)
from .mongo_connector import (
    run_mongo_query, list_collections, sample_documents,
    insert_query_log, get_all_logged_queries, delete_logged_query, clear_logged_queries
)

def convert_objectids(obj):
    if isinstance(obj, dict):
        return {k: convert_objectids(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_objectids(v) for v in obj]
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj

@csrf_exempt
def process_nl_query(request):
    try:
        print("\n==== Raw Request Body ====\n", request.body)

        try:
            data = json.loads(request.body)
        except Exception as e:
            return JsonResponse({"error": "Invalid JSON format", "details": str(e)}, status=400)

        print("\n==== Parsed JSON Body ====\n", data)

        nl_query = data.get("query")
        if not nl_query:
            return JsonResponse({"error": "Missing 'query' field in request body"}, status=400)

        result = convert_nl_to_query(nl_query)

        if "error" in result:
            return JsonResponse({
                "error": "Gemini model failed",
                "details": result.get("details", "Unknown error from Gemini.")
            }, status=500)

        query = result.get("query")
        db_type = result.get("database")

        if query is None or db_type is None:
            return JsonResponse({
                "error": "Gemini could not generate a query for this request.",
                "raw_response": result
            }, status=400)

        if db_type == "PostgreSQL":

            query = query.strip().rstrip(";")
            print("🔥 Cleaned query before validation:", query)
        

            if not validate_sql(query):
                return JsonResponse({"error": "Unsafe SQL detected"}, status=400)
        

            if query.lower().startswith("insert into payment"):
                try:
                    import re
                    match = re.match(r"INSERT INTO payment\s*\((.*?)\)\s*VALUES\s*\((.*?)\)", query, re.IGNORECASE)
                    if not match:
                        return JsonResponse({"error": "Invalid INSERT syntax"}, status=400)
        
                    cols = [col.strip() for col in match.group(1).split(",")]
                    vals = [val.strip().strip("'") for val in match.group(2).split(",")]
                    if len(cols) != len(vals):
                        return JsonResponse({"error": "Mismatch between columns and values"}, status=400)
        
                    record = dict(zip(cols, vals))
                    result = insert_into_payment_auto_id(record)
        
                    return JsonResponse({"message": "✅ Record inserted successfully ✌️", **result})
        
                except Exception as e:
                    return JsonResponse({
                        "error": "Failed to insert payment",
                        "details": str(e),
                        "original_query": query
                    }, status=500)
        

            execution_result = run_sql_query(query)
            return JsonResponse({"query": query, "result": execution_result})


        elif db_type == "MongoDB":
            if isinstance(query, str):
                try:
                    query_dict = json.loads(query)
                except Exception as e:
                    return JsonResponse({"error": "Invalid MongoDB JSON query", "details": str(e)}, status=400)
            else:
                query_dict = query

            if not validate_mongo(query_dict):
                return JsonResponse({"error": "Unsupported MongoDB action"}, status=400)

            try:
                execution_result = run_mongo_query(query_dict)
                print("✅ Mongo result (raw):", execution_result)

                safe_result = convert_objectids(execution_result)
                print("✅ Mongo result (clean):", safe_result)

                return JsonResponse({
                    "query": query_dict,
                    "result": safe_result
                }, json_dumps_params={"default": str})

            except Exception as e:
                print("❌ MongoDB error:", traceback.format_exc())
                return JsonResponse({
                    "error": "MongoDB execution error",
                    "details": str(e),
                    "trace": traceback.format_exc()
                }, status=500)

        else:
            return JsonResponse({"error": "Unknown database type generated"}, status=500)

    except Exception as e:
        print("\n==== Fatal Server Error ====\n", traceback.format_exc())
        return JsonResponse({
            "error": "Internal server error",
            "details": str(e),
            "trace": traceback.format_exc()
        }, status=500)



def get_postgres_tables(request):
    return JsonResponse({"tables": list_tables()})

def describe_postgres_table(request, table):
    return JsonResponse({"columns": describe_table(table)})

def sample_postgres_table(request, table):
    return JsonResponse({"rows": sample_rows(table)})

@csrf_exempt
def insert_postgres_data(request, table):
    data = json.loads(request.body)
    return JsonResponse(insert_into_table(table, data))

@csrf_exempt
def update_postgres_data(request, table):
    data = json.loads(request.body)
    set_values = data.get("set")
    where_clause = data.get("where")
    return JsonResponse(update_table(table, set_values, where_clause))

@csrf_exempt
def delete_postgres_data(request, table):
    data = json.loads(request.body)
    where_clause = data.get("where")
    return JsonResponse(delete_from_table(table, where_clause))

def get_mongo_collections(request):
    try:
        collections = list_collections()
        return JsonResponse({"collections": collections})
    except Exception as e:
        return JsonResponse({"error": "Failed to list collections", "details": str(e)}, status=500)

def sample_mongo_documents(request, collection):
    try:
        documents = sample_documents(collection)
        return JsonResponse({"documents": documents})
    except Exception as e:
        return JsonResponse({"error": f"Failed to sample documents from '{collection}'", "details": str(e)}, status=500)

@csrf_exempt
def run_manual_mongo_query(request):
    try:
        data = json.loads(request.body)
    except Exception as e:
        return JsonResponse({"error": "Invalid JSON format", "details": str(e)}, status=400)

    if not validate_mongo(data):
        return JsonResponse({"error": "Unsupported MongoDB action"}, status=400)

    try:
        result = run_mongo_query(data)
        return JsonResponse({"result": result})
    except Exception as e:
        return JsonResponse({"error": "MongoDB query execution failed", "details": str(e)}, status=500)

@csrf_exempt
def get_query_logs(request):
    try:
        queries = get_all_logged_queries()
        return JsonResponse({"queries": queries})
    except Exception as e:
        return JsonResponse({"error": "Failed to retrieve query logs", "details": str(e)}, status=500)

@csrf_exempt
def add_query_log(request):
    try:
        data = json.loads(request.body)
        query = data.get("query")
        if not query:
            return JsonResponse({"error": "Query is required"}, status=400)
        insert_query_log(query)
        return JsonResponse({"message": "Query logged"})
    except Exception as e:
        return JsonResponse({"error": "Failed to log query", "details": str(e)}, status=500)

@csrf_exempt
def remove_query_log(request):
    try:
        data = json.loads(request.body)
        query = data.get("query")
        if not query:
            return JsonResponse({"error": "Query is required"}, status=400)
        delete_logged_query(query)
        return JsonResponse({"message": "Query removed"})
    except Exception as e:
        return JsonResponse({"error": "Failed to remove query", "details": str(e)}, status=500)

@csrf_exempt
def clear_query_logs(request):
    try:
        clear_logged_queries()
        return JsonResponse({"message": "All query logs cleared"})
    except Exception as e:
        return JsonResponse({"error": "Failed to clear query logs", "details": str(e)}, status=500)
