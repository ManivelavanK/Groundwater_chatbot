# services/groq_service.py

import os
from groq import Groq
from dotenv import load_dotenv
import json

class GroqService:
    def __init__(self):
        """
        Initializes the GroqService, loading the API key and setting up the client.
        """
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def generate_mongo_query(self, user_question, schema_info):
        """
        Generates a MongoDB query object from a natural language question.
        """
        system_prompt = f"""
        You are a precise MongoDB query assistant. Your task is to convert a natural language question into a valid MongoDB query filter object based on the provided schema.

        DATABASE SCHEMA:
        {schema_info}

        INSTRUCTIONS:
        1.  Your output MUST be a single, valid JSON object for a MongoDB `find()` query filter. Do NOT output any text or code before or after the JSON object.
        2.  For text/string fields like 'STATE' or 'DISTRICT', use the `$regex` operator with the `i` option for case-insensitive matching. Example: `{{"STATE": {{"$regex": "delhi", "$options": "i"}}}}`.
        3.  For numerical fields (like those ending in '_mm_Total' or '_ham_Total'), use comparison operators (`$gt`, `$gte`, `$lt`, `$lte`) for questions involving "more than", "less than", "at least", etc.
        4.  If a user asks for a list, create a filter for the parent category. Fields to display will be handled later.
        5.  If the question cannot be answered with a query, return an empty JSON object `{{}}`.
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ],
                model=self.model,
                temperature=0.0,
                max_tokens=512,
            )

            response_content = chat_completion.choices[0].message.content

            # Extract JSON if returned in a markdown block
            if "```json" in response_content:
                response_content = response_content.split("```json")[1].split("```")[0]

            query_object = json.loads(response_content)
            return query_object

        except json.JSONDecodeError:
            print("Error: Failed to decode LLM response into JSON.")
            return {}
        except Exception as e:
            print(f"An error occurred while generating MongoDB query: {e}")
            return {}

    def generate_natural_language_response(self, user_question, query_results):
        """
        Generates a natural language response based on the user's question and query results.
        """
        system_prompt = """
        You are an expert data analyst and a helpful virtual assistant. Your task is to answer a user's question based on the provided database results.

        INSTRUCTIONS:
        1. Carefully analyze the user's original question and the JSON data from the database.
        2. If the data is empty, politely inform the user that you couldn't find any information for their request.
        3. If the data contains results, synthesize the information into a clear and direct answer.
        4. For "highest" or "lowest" questions, identify the best record and state the district and value clearly.
        5. Do not just dump the raw JSON data. Explain the results conversationally.
        """

        results_str = json.dumps(query_results, indent=2, default=str)

        prompt_content = f"""
        User's Original Question: "{user_question}"

        Data from Database:
        {results_str}
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt_content}
                ],
                model=self.model,
                temperature=0.5,
                max_tokens=1024,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"An error occurred while generating natural language response: {e}")
            return "I'm sorry, but I encountered an error while processing your request."
