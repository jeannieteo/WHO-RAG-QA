from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load documents
list_files = ['data/dengue.txt', 'data/leprosy.txt', 'data/rabies.txt']
def load_documents():
    for file in list_files:
        with open(file, "r") as f:
            docs = f.read().split("\n")
    return docs

documents = load_documents()

# Create embeddings
doc_embeddings = model.encode(documents)

# Create FAISS index
dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(doc_embeddings))

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def retrieve_context(question):

    question_embedding = model.encode([question])

    D, I = index.search(np.array(question_embedding), k=2)

    context = "\n".join([documents[i] for i in I[0]])

    return context


def generate_answer(question):

    context = retrieve_context(question)

    prompt = f"""
    Answer the question using the context below.

    Context:
    {context}

    Question:
    {question}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
