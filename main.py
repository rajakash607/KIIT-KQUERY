from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, WikipediaLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from chromadb import PersistentClient
# load environment variables
import os
from dotenv import load_dotenv
load_dotenv()

# Load document from wikipedia
wiki_loader = WikipediaLoader(query="KIIT",load_max_docs=3)
wiki_documents = wiki_loader.load()

# Load document from pdf
pdf_loader = PyPDFLoader("C:\\Users\\KIIT\\Desktop\\60projects\\KIIT Kquery\\B.Tech Project Area of Interest-2025 (1).pdf")
pdf_documents = pdf_loader.load()

# Add all documents
all_documents = pdf_documents + wiki_documents

# #Just to check the loaded documents
# for doc in all_documents:
#     print(doc)

# Split the documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
split_documents = text_splitter.split_documents(all_documents)

# Create embeddings and vector store
embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_store = Chroma.from_documents(documents=split_documents, embedding=embeddings)
# Create retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 3})
# Create the Google Generative AI chat model
llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-preview-05-20')
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)


persist_directory = "./chroma_vector_store"  # Directory to store the vector store
os.makedirs(persist_directory, exist_ok=True)  # Create directory if it doesn't exist
client = PersistentClient(path=persist_directory)

collection_name = "my_documents"
collection = client.get_or_create_collection(name=collection_name)
# # Example query
# query = "When was KIIT established?"
# response = qa.run(query)
# print(response)


# Chatbot loop for multiple queries
print("Welcome to KIIT Kquery! Type 'exit' to quit.")
while True:
    user_query = input("You: ")
    if user_query.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break
    response = qa.run(user_query)
    print("Bot:", response)

