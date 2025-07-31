# KIIT Kquery

KIIT Kquery is a Retrieval-Augmented Generation (RAG) chatbot web application built with Flask and LangChain. It leverages Google Generative AI and a Chroma vector store to answer questions about KIIT University using both Wikipedia and PDF documents.

## Features

- Conversational chatbot interface for querying KIIT-related information
- Uses Google Gemini (Generative AI) for natural language responses
- Retrieves context from a vector database built from Wikipedia and PDF sources
- Simple web interface (Flask + HTML/JS)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd KIIT-Kquery
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the project root and add your Google Generative AI API key:

```
GOOGLE_API_KEY=your_google_api_key_here
```

### 4. Prepare the Vector Store

Before running the web app, ensure you have already created the Chroma vector store (`chroma_vector_store`) using your document ingestion script (e.g., `main.py`). This step loads Wikipedia and PDF data into the vector store.

### 5. Run the Web Application

```bash
python app.py
```

The app will be available at [http://localhost:5000](http://localhost:5000).

## Usage

- Open your browser and go to `http://localhost:5000`
- Type your question about KIIT University in the chat box
- The bot will respond using information from the ingested documents

## File Structure

- `app.py` - Flask web server and chatbot backend
- `main.py` - Script to ingest documents and build the vector store
- `main2.py` - CLI chatbot using the persisted vector store
- `templates/index.html` - Web UI (ensure this file exists)
- `chroma_vector_store/` - Directory containing the persisted vector database

## Requirements

- Python 3.8+
- Google Generative AI API access
- All Python dependencies in `requirements.txt`

## License

MIT License

---

**Note:**  
Make sure to run `main.py` at least once to create the vector store before starting the web app.
