💬 AI-DRIVEN CHATBOT for INGRES (Virtual Assistant)

📌 PROJECT OVERVIEW

This project was developed for the Smart India Hackathon (SIH), based on problem statement PS25066.
The chatbot serves as a Virtual Assistant for INGRES, designed to answer natural language queries using a Retrieval-Augmented Generation (RAG) architecture.

It can intelligently route queries to the right MongoDB collection, fetch the required data, and provide human-readable answers.


🚀 FEATURES

Multi-Collection Querying → Supports multiple datasets (e.g., groundwater data, additional CSVs).

RAG-based Workflow → Combines structured database retrieval with natural language response generation.

Dynamic Query Routing → AI decides the most relevant collection before executing queries.

Natural Language Responses → Converts raw MongoDB query results into user-friendly answers.

Smart Efficiency Handling → Greets like “hi” or “hello” are handled directly without AI/database calls (saves API usage).

Simple Web Interface → HTML, CSS, JS frontend for smooth user interaction.


🏗️ ARCHITECTURE

The project follows a two-step AI pipeline:

NL2Query (Natural Language → MongoDB Query)

AI acts as a router, checks schemas, selects the right collection, and generates a MongoDB query.

QR2NL (Query Result → Natural Language)

Query is executed, results returned, and AI converts structured data into conversational text.


🛠️ TECH STACK

Backend: Python (Flask)

Database: MongoDB Community Server (local)

AI Model: Llama 3 (via Groq API → llama-3.3-70b-versatile)

Data Ingestion: pandas

Frontend: HTML, CSS, JavaScript

📂 FILE STRUCTURE

📦 project-root
 ┣ 📂 data
 ┃ ┣ ingres_data.csv        # Primary groundwater dataset
 ┃ ┣ file_1.csv             # Additional dataset 1
 ┃ ┗ file_2.csv             # Additional dataset 2
 ┣ 📂 services
 ┃ ┣ mongo_service.py       # MongoDB connection + queries
 ┃ ┗ groq_service.py        # AI routing + response generation
 ┣ app.py                   # Main Flask application
 ┣ ingest_data.py           # Script to load CSV → MongoDB collection
 ┣ index.html               # Chat frontend
 ┣ style.css                # Frontend styling
 ┣ script.js                # Frontend logic
 ┣ .env                     # API keys & configs (not pushed to GitHub)
 ┗ README.md                # Project documentation


⚙️ SETUP REPOSITORY

1️⃣ Clone the Repository
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

2️⃣ INSTALL DEPENDENCIES

Make sure you have Python 3.9+ and MongoDB installed locally.

pip install -r requirements.txt

3️⃣ CONFIGURE ENVIRONMENTAL VARIABLE

Create a .env file in the root directory:

GROQ_API_KEY=your_api_key_here
MONGO_URI=mongodb://localhost:27017

4️⃣ INGEST DATA

Load CSV files into MongoDB collections:

python ingest_data.py data/ingres_data.csv information
python ingest_data.py data/file_1.csv collection_1
python ingest_data.py data/file_2.csv collection_2

5️⃣ RUN FLASK APP

python app.py


Open your browser at: http://127.0.0.1:5000

🖥️ USAGE

Ask questions like:

“Show me groundwater levels in Tamil Nadu”

“What is the rainfall data in collection_1?”

Chatbot automatically:

Picks the right MongoDB collection.

Generates & executes the query.

Returns a conversational answer.


🛠️ TROUBLE SHOOTING JOURNEY (Highlights)

✅ Migrated from MongoDB Atlas → Local MongoDB (DNS issues solved).

✅ Cleaned CSV with complex headers for proper ingestion.

✅ Updated to latest Groq model (llama-3.3-70b-versatile) after deprecation.

✅ Added rate-limit handling with query limits & greeting bypass.


📜 LICENCE

This project is developed under SIH guidelines.
For educational & demonstration purposes.

👥 CONTRIBUTORS

NEURO CODERS
