from fastapi import FastAPI
from pydantic import BaseModel

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from groq import Groq

from dotenv import load_dotenv

import os

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- FASTAPI ----------------
app = FastAPI()

# ---------------- EMBEDDINGS ----------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ---------------- VECTOR DB ----------------
db = FAISS.load_local(
    "ipc_vector_db",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

# ---------------- GROQ ----------------
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------- REQUEST MODEL ----------------
class AskRequest(BaseModel):
    question: str

# ---------------- /ASK ENDPOINT ----------------
@app.post("/ask")
def ask_question(request: AskRequest):

    docs = retriever.invoke(request.question)

    context = "\n\n".join(
        doc.page_content[:1000]
        for doc in docs
    )

    prompt = f"""
Answer ONLY using context.

CONTEXT:
{context}

QUESTION:
{request.question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=1000
    )

    answer = response.choices[0].message.content

    citations = []

    for doc in docs:

        citations.append({
            "source": doc.metadata.get("source"),
            "page": doc.metadata.get("page"),
            "snippet": doc.page_content[:300]
        })

    return {
        "question": request.question,
        "answer": answer,
        "citations": citations,
        "confidence_score": round(
            min(len(docs) / 5, 1.0) * 100,
            2
        )
    }