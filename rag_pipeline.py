from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables (expects OPENAI_API_KEY in .env).
load_dotenv()


# Initialize the sentence embedding model used for both documents and questions.
model = SentenceTransformer("all-MiniLM-L6-v2")

# Source text files to ingest into the retrieval index.
list_files = ['data/dengue.txt', 'data/leprosy.txt', 'data/rabies.txt']

# Read documents from text files and split each file into line-based chunks.
def load_documents():
    for file in list_files:
        with open(file, "r") as f:
            # Note: this currently keeps chunks from the last file read.
            docs = f.read().split("\n")
    return docs

# In-memory list of text chunks used for retrieval.
documents = load_documents()

# Convert all document chunks into dense vectors.
doc_embeddings = model.encode(documents)

# Build a FAISS L2 index for nearest-neighbor similarity search.
dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(doc_embeddings))

# Initialize OpenAI client with API key from environment.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Retrieve top-k relevant chunks for a question from the FAISS index.
def retrieve_context(question):
    # Embed question in the same vector space as documents.
    question_embedding = model.encode([question])
    # Search for the 2 closest chunks by L2 distance.
    D, I = index.search(np.array(question_embedding), k=2)
    # Join selected chunks into a single context block.
    context = "\n".join([documents[i] for i in I[0]])
    return context


# Generate a final answer using retrieved context and an LLM call.
def generate_answer(question):
    # Retrieve supporting text before generation.
    context = retrieve_context(question)
    # Build a simple prompt that constrains the model to the retrieved context.
    prompt = f"""
    Answer the question using the context below.
    Context:
    {context}
    Question:
    {question}
    """

    # Send prompt to chat completion endpoint.
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    # Return only the assistant's text output.
    return response.choices[0].message.content
