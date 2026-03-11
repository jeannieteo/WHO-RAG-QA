## Retrieval Augmented Generation (RAG):
AI assistant answers questions from healthcare documents (clinical guidelines, medical PDFs, etc.).

Example:
User question "What are the symptoms of diabetes?"
The system then searches medical documents and retrieves relevant text, Sends it to an LLM amd Returns a summarized answer
## Project structure:

User Question => 
**FastAPI endpoint** =>

**Document Retriever (FAISS)**  =>

Top relevant medical text  =>

**LLM (OpenAI / Llama / Bedrock)**  =>

Answer returned to user



| Component  | Tool                               | Description|
| ---------- | ---------------------------------- |---------------|
| LLM        | OpenAI / AWS Bedrock / HuggingFace ||
| Embeddings | sentence-transformers              |https://huggingface.co/sentence-transformers Sentence Transformers (a.k.a. SBERT) is the go-to Python module for accessing, using, and training state-of-the-art embedding and reranker models. |
| Vector DB  | FAISS                              |Faiss is open-source vector database for fast, and dense vector similarity search and for grouping. https://faiss.ai/|
| Backend    | FastAPI                            |FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints. https://fastapi.tiangolo.com/
| Language   | Python                             ||
