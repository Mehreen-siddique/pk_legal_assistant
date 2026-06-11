# pk_legal_assistant
---
title: Pakistan Legal Assistant
emoji: ⚖️
colorFrom: green
colorTo: blue
sdk: streamlit
sdk_version: 1.35.0
app_file: app.py
pinned: true
license: mit
short_description: Ask questions about Pakistani law in English or Roman Urdu
---

# ⚖️ Pakistan Legal Assistant

**Pakistan's first AI-powered legal assistant** — answers questions about Pakistani law
using RAG (Retrieval-Augmented Generation) on official legal documents.

## What it covers
- Constitution of Pakistan
- Pakistan Penal Code (PPC) — all 511 sections
- Code of Criminal Procedure (CrPC) — FIR filing, arrests, bail
- Code of Civil Procedure (CPC)
- Labour Laws (Industrial Relations Act 2012)
- Family Laws Ordinance 1961
- Punjab Rent Restriction Ordinance (tenant rights)

## How it works
1. Official Pakistani legal PDFs → text extraction (PyMuPDF)
2. Chunked & embedded using multilingual sentence-transformers
3. Stored in FAISS vector database
4. User question → retrieve top 5 relevant chunks → LLaMA 3 70B (via Groq)
5. Answer grounded in actual Pakistani law

## Built by
**Mehreen Siddique** — ML Engineer, Lahore, Pakistan
- HuggingFace: huggingface.co/Mehreen-siddique
- GitHub: github.com/Mehreen-siddique
