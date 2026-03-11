from fastapi import FastAPI
from rag_pipeline import generate_answer

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Healthcare AI Assistant"}

@app.get("/ask")
def ask(question: str):

    answer = generate_answer(question)

    return {
        "question": question,
        "answer": answer
    }