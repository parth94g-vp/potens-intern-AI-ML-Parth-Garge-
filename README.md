
# Legal Assistant — AI-Powered Legal RAG System


## Overview

Legal Assistant is an AI-powered Retrieval-Augmented Generation (RAG) system designed to answer legal questions using uploaded legal documents and policies. The system combines semantic search, vector databases, and Large Language Models (LLMs) to provide structured, citation-based legal responses while minimizing hallucinations.

The project focuses on:
        
- Indian legal compliance
- DPDP Act
- Motor Vehicle Rules
- IPC-related legal reasoning
- GDPR
- Privacy Policies
- Employment Policies

The system supports multilingual queries, citation-based answers, confidence scoring, and a modern Streamlit interface.


### Core Features
- Retrieval-Augmented Generation (RAG)
- Semantic document search using embeddings
- Citation-based answers
- Multilingual query support
- Confidence scoring
- Legal hallucination prevention
- Streamlit UI
- FastAPI /ask endpoint
- FAISS vector database
- Structured legal analysis
- Supported Legal Domains

The knowledge base currently contains:

- DPDP Act documents
- Motor Vehicle Rules
- GDPR documentation
- Employment Policies
- Privacy Policies
- IPC-related legal material

All documents were merged into a consolidated PDF (~123 pages) and indexed into the vector database.




## System architecture 

<img width="1024" height="1535" alt="Image" src="https://github.com/user-attachments/assets/eccd8b6f-47b5-4c9d-8651-e7d07d1b63ca" />

## Screenshots


## Tech Stack

### Frontend
- Streamlit
- Custom CSS
- Python

### Backend
- FastAPI
- LangChain

### AI / LLM
- Groq API
- Llama-3.3-70B-Versatile

### Vector Database
- FAISS

### Embedding Model
- sentence-transformers/all-MiniLM-L6-v2

### Document Processing
- PyPDFLoader
- RecursiveCharacterTextSplitter

### Multilingual Support
- langdetect
- deep-translator

### Environment & Utilities
- python-dotenv

### Deployment Ready
- Streamlit
- Uvicorn
## Project Structure 

    Leagal AI Assitant/
    │
    ├── app.py
    ├── api.py
    ├── Ingest.py
    ├── requirements.txt
    ├── README.md
    ├── .env
    ├── data/
    │     └── legal_documents.pdf
    ├── ipc_vector_db/
## Document Ingestion Pipeline


The system uses a Retrieval-Augmented Generation (RAG) architecture.

### Step 1 : Document Loading

Legal documents are loaded using:

**"PyPDFLoader"**

The documents include:

- DPDP Act
- GDPR
- Employment Policies
- Privacy Policies
- Motor Vehicle Rules

### Step 2 : Chunking Strategy

The documents are split using:

**"RecursiveCharacterTextSplitter"**

Configuration
- chunk_size = 1000
- chunk_overlap = 200


Why This Chunking Strategy?

Legal documents often contain:

- long sections
- contextual dependencies
- section references
- multi-paragraph clauses

Using, smaller chunks may lose legal context
very large chunks reduce retrieval precision

The selected configuration balances:

- semantic completeness
- retrieval accuracy
- embedding quality
- LLM context efficiency
- Chunk Overlap

An overlap of 200 characters ensures:

continuity between adjacent clauses
preservation of legal references
better retrieval consistency

### Embedding Model

The system uses:

**sentence-transformers/all-MiniLM-L6-v2**

Why This Model?

Because it is : 
- lightweight
- fast inference
- strong semantic similarity performance
- suitable for CPU environments
- works well for legal semantic retrieval
- Vector Database

The embeddings are stored in:

**FAISS (Facebook AI Similarity Search)** Vector Database

Why FAISS?

- fast similarity search
- lightweight
- easy local deployment
- efficient semantic retrieval
- ideal for assignment-scale RAG systems

### Retrieval Flow

When a user asks a question:

1. Query is embedded
2. FAISS retrieves top-k relevant chunks
3. Retrieved chunks are formatted into context
4. Context is passed to the LLM
5. LLM generates structured legal response
6. Citation System

### Hallucination Prevention

The prompt explicitly instructs the model to:

- answer ONLY from retrieved context
- avoid unsupported claims
- clearly mention insufficient information

Example:

**"The uploaded legal documents do not contain sufficient information."**

This prevents silent hallucinations.

### Multilingual Support

The system supports multilingual legal queries.

<img width="1536" height="1024" alt="Image" src="https://github.com/user-attachments/assets/8cf5df34-84d5-4865-9438-0abb0363ea37" />

### Confidence Score

The system generates a confidence score based on:

- retrieval completeness
- number of retrieved chunks
- retrieval quality

This provides users with transparency regarding answer reliability.

### Streamlit User Interface

The application includes:

- modern dark UI
- responsive layout
- feature cards
- chat interface
- citation expanders
- confidence scoring

## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd my-project
```

Create Virtual Environment

    python -m venv myenv


Activate:

Windows

    myenv\Scripts\activate


Install Requirements

    pip install -r requirements.txt

Configure Environment Variables

Create .env

    GROQ_API_KEY=your_api_key_here

Run Ingestion

    python Ingest.py

Run Streamlit App

    streamlit run app.py
## Usage/Examples

Example Queries
- DPDP Act

        Is consent required for employee data processing?
- GDPR

        What are the lawful bases for processing personal data?
- Motor Vehicle Rules

        What are the penalties for driving without insurance?

- Privacy Policy

        Can organizations share personal information with third parties?

