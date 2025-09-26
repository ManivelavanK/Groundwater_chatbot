# services/mongo_service.py

import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId
import json

class MongoService:
    def __init__(self, db_name, collection_name):
        """
        Initializes the MongoService, connecting to the specified database and collection.
        """
        load_dotenv()
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI not found in environment variables.")

        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        print(f"Connected to MongoDB collection: {db_name}.{collection_name}")

    def get_schema_info(self):
        """
        Retrieves a sample document to infer the schema of the collection.
        Returns a string representation of the schema.
        """
        try:
            sample_doc = self.collection.find_one()
            if not sample_doc:
                return "No documents in collection to infer schema from."

            # Remove the '_id' field as it's not usually queried by users directly
            if '_id' in sample_doc:
                del sample_doc['_id']

            schema = {field: type(value).__name__ for field, value in sample_doc.items()}
            return json.dumps(schema, indent=2)
        except Exception as e:
            print(f"Error getting schema info: {e}")
            return "Could not retrieve schema information."

    def execute_query(self, query_object):
        """
        Executes a find query on the collection.
        """
        try:
            # Limit results to 20 to avoid overwhelming the AI and user
            results = list(self.collection.find(query_object).limit(20))

            # Convert MongoDB's ObjectId to a string so it can be sent as JSON
            for result in results:
                if '_id' in result:
                    result['_id'] = str(result['_id'])

            return results
        except Exception as e:
            print(f"An error occurred while executing query: {e}")
            return

    def close_connection(self):
        """
        Closes the MongoDB connection.
        """
        self.client.close()