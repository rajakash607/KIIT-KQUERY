from flask import Flask, render_template, request, jsonify
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize the RAG system
persist_directory = "./chroma_vector_store"
collection_name = "my_documents"

# Load the persisted Chroma vector store
vector_store = Chroma(
    persist_directory=persist_directory,
    collection_name=collection_name,
    embedding_function=None  # Not needed for loading
)

# Create retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# Create the Google Generative AI chat model
llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-preview-05-20')
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    try:
        user_query = request.json.get('query', '')
        if not user_query.strip():
            return jsonify({'error': 'Please enter a valid query'}), 400
        
        # Get response from the QA system
        response = qa.invoke(user_query)
        
        # Extract the result text
        result_text = response.get('result', '') if isinstance(response, dict) else str(response)
        
        return jsonify({'response': result_text})
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)