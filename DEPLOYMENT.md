# Pakistan Legal Assistant - Deployment Instructions

This document outlines the steps to deploy the Pakistan Legal Assistant RAG application to production.

## Prerequisites

- **Python Version**: Python 3.11 is recommended.
- **Hardware Requirement**: For local deployment, at least 8GB RAM is required. For cloud hosting, ensure the environment has sufficient memory to run a 1.5B parameter language model (typically >4-6GB RAM; Hugging Face Spaces provides free 16GB CPU containers, which are perfect).

---

## Option 1: Deploying to Hugging Face Spaces (Recommended)

Hugging Face Spaces is the easiest platform for running applications with large models because of its integration with the Hugging Face Hub and generous free hardware limits (16GB RAM CPU Basic tier).

### Step 1: Create a Space
1. Log in to your [Hugging Face Account](https://huggingface.co/).
2. Click on **New Space**.
3. Set your **Space Name** (e.g., `pakistan-legal-assistant`).
4. Select **Streamlit** as the SDK.
5. Select the Space hardware: **CPU basic (free)** or **T4 small (GPU)** if you want faster generation.
6. Set the Space visibility to **Public** or **Private** as desired.

### Step 2: Upload Files
You can clone the Space repository using Git and push the project files, or upload them directly via the HF web interface. Upload the following files and folders:
- `app.py`
- `requirements.txt`
- `utils/` (entire directory containing `pdf_loader.py`, `text_cleaner.py`, `retriever.py`, `llm_loader.py`, `prompt.py`)
- `legal_faiss/` (containing `index.faiss` and `index.pkl` - see **Building Vector DB** below)

*Note: You do not need to upload the `data/` folder or the dummy PDF generator script to the Hugging Face space if the vector database `legal_faiss/` is already built and uploaded.*

### Step 3: HF Space Initialization
Once the files are pushed, Hugging Face will automatically:
1. Detect `requirements.txt` and install all libraries.
2. Read the `app.py` file and spin up the Streamlit server.
3. Automatically download the embedding model (`sentence-transformers/paraphrase-multilingual-mpnet-base-v2`) and the LLM model (`Qwen/Qwen2.5-1.5B-Instruct`) from the Hub on startup.

---

## Option 2: Deploying to Streamlit Community Cloud

Streamlit Community Cloud is free and syncs directly with a GitHub repository.

### Step 1: Push Project to GitHub
Create a new GitHub repository and push the following files:
- `app.py`
- `requirements.txt`
- `utils/` folder
- `legal_faiss/` folder

### Step 2: Connect to Streamlit Cloud
1. Sign in to [Streamlit Share](https://share.streamlit.io/).
2. Click **New app**.
3. Select your GitHub repository, branch, and entry point file (`app.py`).
4. Click **Deploy**.

> [!WARNING]
> Streamlit Community Cloud containers are limited to 1GB of RAM. The `Qwen2.5-1.5B-Instruct` model requires around ~3-4GB of memory in 32-bit/16-bit precision. Therefore, deploying on Streamlit Community Cloud might result in **Out Of Memory (OOM)** errors unless you switch the LLM component to call a cloud API (such as the Hugging Face Inference API or Qwen API) instead of loading the model locally. Hugging Face Spaces is highly recommended for running models locally.

---

## Local Setup & Building Vector Database Before Deployment

Before deploying, you must build the FAISS vector database:

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate Document Data**:
   If you do not have raw PDF files, run the dummy PDF generator to create them:
   ```bash
   python generate_dummy_pdfs.py
   ```

3. **Build the Vector Database**:
   Index the PDF documents in the `data/` folder and generate the FAISS files:
   ```bash
   python build_vector_db.py
   ```
   This will create a `legal_faiss/` directory containing `index.faiss` and `index.pkl`.

4. **Run the App Locally**:
   To test before deploying to production:
   ```bash
   streamlit run app.py
   ```
