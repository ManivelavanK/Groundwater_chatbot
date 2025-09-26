# app.py

from flask import Flask, request, jsonify, render_template
from services.groq_service import GroqService
from services.mongo_service import MongoService
import json

app = Flask(__name__)

# --- Service Initialization ---
try:
    # These names must match what you used in ingest_data.py
    DATABASE_NAME = 'ingres_db'
    COLLECTION_NAME = 'information'

    mongo = MongoService(db_name=DATABASE_NAME, collection_name=COLLECTION_NAME)
    groq = GroqService()

    # Fetch the schema once when the app starts. This is efficient.
    SCHEMA_INFO = mongo.get_schema_info()
    print("Successfully loaded database schema.")

except Exception as e:
    print(f"Failed to initialize services: {e}")
    mongo = None
    groq = None
    SCHEMA_INFO = "Error: Could not load schema."

# --- Routes ---
@app.route('/')
def index():
    """Renders the main chat page."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """The main chat endpoint that orchestrates the RAG pipeline."""
    if not mongo or not groq:
        return jsonify({"error": "Backend services are not initialized."}), 500

    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided."}), 400

    try:
        print(f"User message: '{user_message}'")
        mongo_query = groq.generate_mongo_query(user_message, SCHEMA_INFO)

        # --- IMPORTANT CHANGE: Handle simple greetings and empty queries ---
        if not mongo_query:  # Check if the query is empty ({})
            print("Empty query generated. Responding directly.")
            if any(greeting in user_message.lower() for greeting in ["hi", "hello", "hey"]):
                return jsonify({"response": "Hello! I am an AI assistant for INGRES. How can I help you with the groundwater data?"})
            else:
                return jsonify({"response": "I'm sorry, I couldn't determine what to search for in the database. Could you please ask a more specific question about the data?"})

        print(f"Generated MongoDB Query: {json.dumps(mongo_query)}")
        query_results = mongo.execute_query(mongo_query)

        if query_results is None:
            print("Database query failed.")
            return jsonify({"error": "Failed to execute database query."}), 500

        print(f"Found {len(query_results)} results from database.")
        final_response = groq.generate_natural_language_response(user_message, query_results)

        return jsonify({"response": final_response})

    except Exception as e:
        print(f"An error occurred in the chat pipeline: {e}")
        return jsonify({"error": "An internal error occurred."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
