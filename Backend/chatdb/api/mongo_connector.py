# mongo_connector.py
# This file handles database interactions with MongoDB, including executing
# natural language-translated Mongo queries and sample schema exploration.

from pymongo import MongoClient
from datetime import datetime
import os

# MongoDB Client Setup
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client.chatdb



def run_mongo_query(query):
    """
    Execute a MongoDB operation from a structured dictionary query.
    Supported actions:
    - find (with optional projection)
    - insertOne, insertMany
    - updateOne, updateMany
    - deleteOne, deleteMany
    - aggregate (supports $match, $group, $sort, $limit, $skip, $project, $lookup)
    - list_collections (custom action to list MongoDB collections)
    """
    raw_action = query.get('action')
    if not raw_action:
        raise ValueError("Missing 'action' field in MongoDB query.")

    # Normalize Gemini or user-generated aliases
    action_map = {
        "insert": "insertOne",
        "insertone": "insertOne",
        "insert_one": "insertOne",  
        "insertmany": "insertMany",
        "insert_many": "insertMany",  
        "updateone": "updateOne",
        "update_one": "updateOne",  
        "updatemany": "updateMany",
        "update_many": "updateMany",  
        "deleteone": "deleteOne",
        "delete_one": "deleteOne",  
        "deletemany": "deleteMany",
        "delete_many": "deleteMany",  
        "listcollections": "list_collections",
        "list_collections": "list_collections"
    }
    action = action_map.get(raw_action.lower().replace("_", ""), raw_action)

    if action == "list_collections":
        return list_collections()

    collection_name = query.get('collection')
    if not collection_name:
        if action == "aggregate":
            collection_name = "orders"  
        else:
            raise ValueError("Missing 'collection' field in MongoDB query.")

    collection = db[collection_name]

    if action == 'find':
        filter_query = query.get('filter', {})
        projection = query.get('projection', {"_id": 0})
        limit = query.get('limit', 0)

        cursor = collection.find(filter_query, projection)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)

    elif action == 'insertOne':
        document = query.get('document')
        if document is None:
            raise ValueError("Missing 'document' for insertOne.")
        
        result = collection.insert_one(document)

        # Make sure to return the ObjectId as string
        return {
            "message": "✅ Successfully inserted one document.",
            "inserted_id": str(result.inserted_id)  # This avoids serialization issues
        }

    elif action == 'insertMany':
        documents = query.get('documents')
        print("📦 insertMany — Raw documents:", documents)
    
        if not documents or not isinstance(documents, list):
            raise ValueError("Missing or invalid 'documents' list for insertMany.")
    
        for i, doc in enumerate(documents):
            if not isinstance(doc, dict):
                raise ValueError(f"Document #{i + 1} is not a valid dictionary.")
    
        result = collection.insert_many(documents)
    
        inserted_ids = [str(_id) for _id in result.inserted_ids]
        print("✅ Inserted IDs:", inserted_ids)
    
        return {
            "message": f"✅ Successfully inserted {len(inserted_ids)} documents.",
            "inserted_ids": inserted_ids
        }

    elif action == 'updateOne':
        collection_name = query.get('collection')
        filter_ = query.get('filter')
        update = query.get('update')
        
        if not collection_name or filter_ is None or update is None:
            raise ValueError("Missing 'collection', 'filter', or 'update' for updateOne.")
        
        collection = db[collection_name]
        result = collection.update_one(filter_, update)

        return {
            "message": "✅ Document updated successfully.",
            "matched_count": result.matched_count,
            "modified_count": result.modified_count
        }


    elif action == 'deleteOne':
        filter_query = query.get('filter')
        if not filter_query:
            raise ValueError("Missing 'filter' for deleteOne.")
    
        result = collection.delete_one(filter_query)
    
        if result.deleted_count == 0:
            return {
                "message": "🤔Oops！No document matched the filter. Nothing was deleted.",
                "deleted_count": 0
            }
        else:
            return {
                "message": "🗑️ Successfully deleted one document.",
                "deleted_count": result.deleted_count
            }


    elif action == 'aggregate':
        pipeline = query.get('pipeline')
        if not isinstance(pipeline, list):
            raise ValueError("Missing or invalid 'pipeline' for aggregation.")
        return list(collection.aggregate(pipeline))

    else:
        raise ValueError(f"Unsupported MongoDB action: {action}")


# Schema Exploration Utilities
def list_collections():
    """
    Return the names of all collections in the MongoDB database.
    """
    return db.list_collection_names()

def sample_documents(collection_name, limit=5):
    """
    Retrieve a sample of documents from a collection (defaults to 5).
    """
    return list(db[collection_name].find({}, {"_id": 0}).limit(limit))


# Logging Helper Functions
def insert_query_log(nl_query):
    db.queries.insert_one({"query": nl_query, "created_at": datetime.utcnow()})

def get_all_logged_queries():
    return list(db.queries.find({}, {"_id": 0, "query": 1, "created_at": 1}))

def delete_logged_query(nl_query):
    db.queries.delete_one({"query": nl_query})

def clear_logged_queries():
    db.queries.delete_many({})
