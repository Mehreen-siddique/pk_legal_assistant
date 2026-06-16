
# Pakistan Legal Assistant - Complete Project Specification

## Project Overview

Build an AI-powered legal assistant for Pakistani law using Retrieval-Augmented Generation (RAG).

The assistant must answer legal questions based ONLY on retrieved legal documents and must not hallucinate laws.

Supported languages:

- English
- Roman Urdu

Target users:

- General public
- Law students
- Lawyers
- Researchers

---

# Project Name

Pakistan Legal Assistant

---

# Tech Stack

Frontend:
- Streamlit

Backend:
- Python

RAG Framework:
- LangChain

Embeddings:
- sentence-transformers/paraphrase-multilingual-mpnet-base-v2

Vector Database:
- FAISS

LLM:
- Qwen/Qwen2.5-1.5B-Instruct

NOTE:
Do NOT use Qwen 7B locally.
Use Qwen 1.5B for development.

PDF Processing:
- PyMuPDF (fitz)

Deployment:
- Streamlit Cloud
or
- HuggingFace Spaces

Python Version:
- Python 3.11

---

# Legal Documents

The system must support:

1. Constitution of Pakistan

2. Pakistan Penal Code (PPC)

3. Code of Criminal Procedure (CrPC)

4. Code of Civil Procedure (CPC)

5. Family Laws Ordinance 1961

6. Industrial Relations Act 2012

7. Punjab Rent Restriction Ordinance

Additional laws can be added later.

---

# Project Structure

project/

│

├── app.py

├── requirements.txt

├── build_vector_db.py

├── legal_faiss/

│   ├── index.faiss

│   └── index.pkl

│

├── data/

│   ├── constitution.pdf

│   ├── ppc.pdf

│   ├── crpc.pdf

│   ├── cpc.pdf

│   ├── family_laws.pdf

│   ├── labour_laws.pdf

│   └── rent_laws.pdf

│

├── utils/

│   ├── pdf_loader.py

│   ├── text_cleaner.py

│   ├── retriever.py

│   ├── llm_loader.py

│   └── prompt.py

│

└── DOCUMENT.md

---

# Functional Requirements

The system must:

1. Accept legal questions

2. Retrieve relevant legal sections

3. Generate grounded answers

4. Display legal sources

5. Display retrieved chunks

6. Prevent hallucinations

7. Support Roman Urdu questions

Example:

User:
"FIR kya hoti hai?"

System:
Retrieve relevant CrPC sections and explain.

---

# PDF Processing Pipeline

Create utility:

utils/pdf_loader.py

Responsibilities:

- Read PDF files
- Extract text using PyMuPDF
- Return clean text

Pseudo:

for each pdf:
    open pdf
    extract text
    return text

---

# Text Cleaning

Create utility:

utils/text_cleaner.py

Tasks:

- Remove extra spaces
- Remove broken lines
- Remove repeated headers
- Normalize whitespace

Function:

clean_text(text)

returns cleaned text

---

# Chunking Strategy

Use:

RecursiveCharacterTextSplitter

Parameters:

chunk_size = 1000

chunk_overlap = 200

Each chunk should preserve legal context.

---

# Embeddings

Use:

sentence-transformers/paraphrase-multilingual-mpnet-base-v2

Reason:

Supports:
- English
- Urdu
- Roman Urdu

---

# Vector Database

Use FAISS.

Create:

build_vector_db.py

Workflow:

1. Load all PDFs

2. Extract text

3. Clean text

4. Chunk text

5. Create embeddings

6. Store in FAISS

7. Save locally

Output:

legal_faiss/index.faiss

legal_faiss/index.pkl

---

# Retriever

File:

utils/retriever.py

Function:

retrieve_documents(query)

Process:

1. Load FAISS

2. Similarity search

3. Retrieve top 5 chunks

Return:

documents

---

# LLM Loader

File:

utils/llm_loader.py

Load:

Qwen/Qwen2.5-1.5B-Instruct

Use transformers pipeline.

Generation settings:

temperature = 0.2

max_new_tokens = 512

do_sample = True

top_p = 0.9

Cache model.

---

# Prompt Engineering

File:

utils/prompt.py

Prompt:

You are Pakistan Legal Assistant.

Rules:

1. Use ONLY provided legal context.

2. Never invent legal sections.

3. Cite legal provisions when available.

4. If answer is not found, respond:

"Information not found in legal documents."

5. Keep answers legally accurate.

6. Explain in simple language.

Context:
{context}

Question:
{question}

Answer:

---

# Answer Generation Flow

User Question

↓

Retrieve Top 5 Chunks

↓

Build Prompt

↓

Send To Qwen

↓

Generate Answer

↓

Display Sources

---

# Streamlit UI Requirements

Professional legal-themed UI.

Page title:

Pakistan Legal Assistant

Icon:

⚖️

Layout:

Wide

---

# Sidebar

Display:

Pakistan Legal Assistant

Supported Laws

About System

Version

---

# Main Page

Display:

Title

Description

Question Box

Search Button

---

# Input Area

Use:

st.text_area()

Placeholder:

Ask your legal question...

Examples:

What is FIR?

What is Section 302 PPC?

Can police arrest without warrant?

Tenant rights in Punjab?

---

# Search Button

Label:

Ask Legal Assistant

---

# Loading State

Show:

Searching legal documents...

Retrieving relevant laws...

Generating answer...

---

# Answer Section

Display:

Generated legal answer

Inside card/container

---

# Sources Section

Display:

Top retrieved chunks

Use expanders:

Source 1

Source 2

Source 3

Source 4

Source 5

---

# Error Handling

Handle:

Missing FAISS index

Missing PDF files

Model loading failure

Empty question

Embedding errors

Display friendly messages.

---

# Performance Requirements

Use caching:

@st.cache_resource

for:

Embedding model

Vector database

LLM

Avoid reloading resources.

---

# Security Rules

The assistant must NOT:

Invent laws

Give fake legal sections

Provide legal guarantees

Claim to be a lawyer

Answer outside legal context

---

# Expected Example

Question:

What are tenant rights in Pakistan?

Process:

Retrieve rent law chunks

Generate answer

Display:

Answer

Sources

---

# requirements.txt

streamlit

torch

transformers

accelerate

sentence-transformers

langchain

langchain-community

langchain-huggingface

faiss-cpu

pymupdf

pypdf

numpy

pandas

---

# Future Improvements

Chat history

Conversation memory

Citation highlighting

Section references

Urdu translation

Voice input

PDF upload

Case law database

Lawyer recommendation system

Fine-tuned legal model

Admin dashboard

Analytics

User feedback system

---

# Final Goal

Build a production-ready Pakistan Legal Assistant using:

FAISS + LangChain + Qwen + Streamlit

that answers legal questions strictly from Pakistani legal documents and provides source-backed responses.