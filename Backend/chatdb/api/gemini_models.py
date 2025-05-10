# This file contains the logic for interacting with Google Gemini.

import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Hardcode the API key for Gemini
# NOTE: Replace this with environment variable loading in production for security
genai.configure(api_key="AIzaSyAeW2r6Dnv7KuYU1zqMVxt8G6f_JejL-Xk")
model = genai.GenerativeModel('gemini-1.5-pro')
print("Loaded API Key: Successfully loaded")

# --------------------------
# PostgreSQL SCHEMA DETAILS
# --------------------------
POSTGRES_SCHEMA = '''
PostgreSQL Tables:
1. customer(customer_id (INT), store_id (INT), first_name (TEXT), last_name (TEXT), email (TEXT), activebool (BOOLEAN), create_date (DATE), last_update (TIMESTAMPTZ), active (INT))
2. rental(Columns: rental_id (INT), rental_date (TIMESTAMPTZ), inventory_id (INT), customer_id (INT), return_date (TIMESTAMPTZ), staff_id (INT), last_update (TIMESTAMPTZ))
3. payment(payment_id (INT), customer_id (INT), staff_id (INT), rental_id (INT), amount (NUMERIC), payment_date (TIMESTAMPTZ))
'''

POSTGRES_RELATIONSHIPS = '''
Table Relationships:
- customer.customer_id = rental.customer_id
- rental.rental_id = payment.rental_id
- customer.customer_id = payment.customer_id
'''

POSTGRES_FIELD_DESCRIPTIONS = '''
customer table:
- customer_id: Primary key; uniquely identifies each customer.
- store_id: Indicates which store the customer belongs to.
- first_name, last_name: Customer's full name.
- email: Email address.
- activebool: A boolean indicating if the account is currently active.
- create_date: The date when the customer was created.
- last_update: Timestamp of last profile update.
- active: Integer flag, 1 = active, 0 = inactive.

rental table:
- rental_id: Primary key; unique ID for each rental transaction.
- rental_date: When the rental started.
- inventory_id: ID of the inventory item rented (not currently joined).
- customer_id: Foreign key linked to customer table.
- return_date: When the rental was returned.
- staff_id: Employee who processed the rental.
- last_update: Last update timestamp.

payment table:
- payment_id: Primary key; unique ID for each payment.
- customer_id: Foreign key referencing who made the payment.
- staff_id: The employee who processed the payment.
- rental_id: Linked to the rental being paid.
- amount: The amount paid.
- payment_date: Timestamp of payment.
'''

# --------------------------
# MongoDB SCHEMA DETAILS
# --------------------------
MONGODB_SCHEMA = '''
MongoDB Collections:

1. customers
- _id (STRING, UUID format): Unique identifier for each customer
- name (STRING): Customer's name
- email (STRING): Customer's email address
- address (STRING): Customer's mailing address

2. orders
- _id (STRING, UUID format): Unique identifier for each order
- customer_id (STRING, UUID format): Refers to customers._id
- order_date (STRING, e.g., "2022-10-15"): The date of the order
- total_amount (FLOAT): Total dollar amount for the order

3. order_items
- _id (STRING, UUID format): Unique identifier for each order item
- order_id (STRING, UUID format): Refers to orders._id
- product_name (STRING): Name of the product
- quantity (INT): Number of units purchased
- price (FLOAT): Price per unit
'''

MONGODB_RELATIONSHIPS = '''
Collection Relationships:
- customers._id = orders.customer_id
- orders._id = order_items.order_id
'''

MONGODB_FIELD_DESCRIPTIONS = '''
customers collection:
- _id: Unique identifier for each customer.
- name: Full name of the customer.
- email: Customer's email address.
- address: Customer's mailing address.

orders collection:
- _id: Unique identifier for each order.
- customer_id: References the _id in customers collection.
- order_date: Date the order was placed (string format).
- total_amount: Total amount of the order.

order_items collection:
- _id: Unique identifier for the item record.
- order_id: References the _id in orders collection.
- product_name: Name of the product.
- quantity: Number of units ordered.
- price: Price per unit.
'''

# --------------------------
# Prompt Handler Function
# --------------------------
def convert_nl_to_query(nl_query):
    try:
        prompt = f"""
        You are an expert in SQL and MongoDB query generation.
        
        You are connected to a system that has two databases:
        
        You may refer to the following notes for field meanings or assumptions.
        
        {POSTGRES_SCHEMA}
        
        {POSTGRES_RELATIONSHIPS}
        
        {POSTGRES_FIELD_DESCRIPTIONS}
        
        {MONGODB_SCHEMA}
        
        {MONGODB_RELATIONSHIPS}
        
        {MONGODB_FIELD_DESCRIPTIONS}

        Instructions:
        - If the user asks for database structure, such as:
            - "List all tables"
            - "Show columns of a table"
            - "Sample 5 rows from a table"
          then generate SQL using `information_schema.tables` or `information_schema.columns`.
        - For MongoDB schema exploration tasks, if the user asks:
            - "What collections exist?"
            - "List all collections"
            - "What are the tables in MongoDB?"
            - "Show me all collections"
          Then generate a MongoDB query like:

          {{
            "query": {{
              "action": "list_collections"
            }},
            "database": "MongoDB"
          }}
        - For MongoDB Queries:
            Always include the following keys:
            - "action": one of "find", "insertOne", "insertMany", "updateOne", "updateMany", "deleteOne", "deleteMany", "aggregate", "list_collections".
            - "collection": REQUIRED. Must be one of "customers", "orders", or "order_items".
            - Include action-specific fields:
              - insertOne: requires "document"
              - updateOne: requires "filter" and "update"
              - deleteOne: requires "filter"
              - aggregate: requires "pipeline" (array of stages)
            
            Do NOT return any MongoDB query without a "collection" field, except for "list_collections"


        - Note on naming:
            - PostgreSQL uses singular table names like `customer`, `payment`, and `rental`.
            - MongoDB uses plural collection names like `customers`, `orders`, and `order_items`.
            - Please match the naming exactly when generating SQL or MongoDB queries.
        - If the user query refers to structured transactional data such as customers, rentals, payments, dates, or amounts, generate a SQL query using the PostgreSQL schema.
        - If the query refers to user interactions, orders, products, or data with UUID-based _id fields, use MongoDB.
        - If both PostgreSQL and MongoDB contain similar-named entities (e.g., 'customers'), decide based on field characteristics:
            - Use PostgreSQL if the query includes: first_name, last_name, active, store_id, rental, payment, or integer-based customer_id.
            - Use MongoDB if the query includes: _id as UUID, address, orders, product_name, quantity, price.
        - Use JOINs when relationships between tables are needed (e.g., link customer_id between customer and rental).
        - Output strictly in JSON format with two fields:
            - "query": the query string (SQL or MongoDB-style JSON)
            - "database": one of "PostgreSQL" or "MongoDB"
        - Do not include any explanation or commentary. Output only the JSON object.
        - Do NOT assume existence of film or inventory details; only use the existing tables and collections.
        - Always use WHERE instead of HAVING unless using aggregate functions.
        - Only output a valid JSON object with two keys: "query" and "database". Do NOT explain anything.
        - If you cannot generate a query, return: {{ "query": null, "database": null }}
        - When listing PostgreSQL tables, exclude system tables such as those starting with 'django_', 'auth_', or 'admin_'.
        - If the MongoDB query uses multiple stages like $match, $lookup, and $project, wrap them in a pipeline list under "pipeline", and set action to "aggregate".
        - Please use these exact actions for mongodb: 'find', 'insertOne', 'updateOne', 'deleteOne', 'aggregate'.


        
        User Query: "{nl_query}"
        """

        response = model.generate_content(prompt)

        print("\n==== Gemini Raw Response ====")
        print(response)

        # Get generated text
        generated_text = response.candidates[0].content.parts[0].text

        print("\n==== Gemini Generated Text ====")
        print(generated_text)

        # Clean Markdown wrapping if present
        cleaned = generated_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:].strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()

        # Parse the JSON text
        parsed_result = json.loads(cleaned)


        # Final debug print
        print("\n==== Final Parsed Result ====")
        print(json.dumps(parsed_result, indent=2))

        return parsed_result

    except Exception as e:
        print("\n==== Gemini Parse Error ====")
        print("Error:", str(e))
        return {
            "error": "Gemini conversion failed",
            "details": str(e)
        }