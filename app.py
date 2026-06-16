import os
import streamlit as st
import time

# Adjust page configuration first
st.set_page_config(
    page_title="Pakistan Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Elegant CSS for premium look and feel
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Inter:wght@300;400;600&display=swap');

/* Main App styling */
.stApp {
    background: linear-gradient(135deg, #06180e 0%, #030806 100%) !important;
    color: #e0e8e4 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #030b06 !important;
    border-right: 2px solid #c9a0dc; /* Fallback border or gold */
    border-right-color: #d4af37 !important; /* Gold border */
}

/* Titles and Headers */
.legal-title {
    font-family: 'Cinzel', serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: #d4af37;
    text-align: center;
    margin-bottom: 0.2rem;
    text-shadow: 0px 4px 10px rgba(212, 175, 55, 0.2);
}

.legal-subtitle {
    font-size: 1.1rem;
    color: #a3b899;
    text-align: center;
    margin-bottom: 2rem;
    font-weight: 300;
    letter-spacing: 1px;
}

/* Custom Answer Card */
.answer-card {
    background: rgba(11, 40, 24, 0.45);
    border: 1px solid #d4af37;
    border-radius: 12px;
    padding: 2rem;
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    transition: all 0.3s ease;
}

.answer-header {
    font-family: 'Cinzel', serif;
    font-size: 1.5rem;
    color: #d4af37;
    border-bottom: 1px solid rgba(212, 175, 55, 0.3);
    padding-bottom: 0.6rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* Interactive elements */
button[kind="secondary"] {
    background-color: rgba(212, 175, 55, 0.1) !important;
    color: #d4af37 !important;
    border: 1px solid rgba(212, 175, 55, 0.4) !important;
    transition: all 0.3s ease !important;
}

button[kind="secondary"]:hover {
    background-color: rgba(212, 175, 55, 0.25) !important;
    border-color: #d4af37 !important;
    transform: translateY(-2px);
}

button[kind="primary"] {
    background-color: #0b3c1b !important;
    color: #d4af37 !important;
    border: 1px solid #d4af37 !important;
    font-weight: bold !important;
    padding: 0.5rem 2rem !important;
    box-shadow: 0 4px 14px 0 rgba(11, 60, 27, 0.4) !important;
}

button[kind="primary"]:hover {
    background-color: #0d4f24 !important;
    box-shadow: 0 6px 20px 0 rgba(212, 175, 55, 0.2) !important;
    transform: translateY(-1px);
}

/* Info boxes and warnings */
.stAlert {
    background-color: rgba(11, 40, 24, 0.3) !important;
    border: 1px solid rgba(212, 175, 55, 0.2) !important;
    color: #e0e8e4 !important;
}

/* Custom styles for details/expanders */
.stExpander {
    background: rgba(5, 15, 10, 0.6) !important;
    border: 1px solid rgba(163, 184, 153, 0.2) !important;
    border-radius: 8px !important;
    margin-bottom: 0.5rem !important;
}

/* Footer styling */
.footer-text {
    text-align: center;
    font-size: 0.8rem;
    color: #6a7f72;
    margin-top: 3rem;
    border-top: 1px solid rgba(163, 184, 153, 0.1);
    padding-top: 1rem;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Try imports and handle missing modules or databases gracefully
try:
    from utils.retriever import retrieve_documents, DB_DIR
    from utils.llm_loader import generate_answer
    from utils.prompt import get_prompt_template
    IMPORTS_OK = True
except Exception as e:
    IMPORTS_OK = False
    IMPORT_ERROR = str(e)

# Sidebar setup
with st.sidebar:
    st.markdown("<h2 style='color: #d4af37; font-family: Cinzel;'>⚖️ Legal Assistant</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### Supported Laws")
    st.markdown("""
    - **Constitution of Pakistan**
    - **Pakistan Penal Code (PPC)**
    - **Code of Criminal Procedure (CrPC)**
    - **Code of Civil Procedure (CPC)**
    - **Family Laws Ordinance 1961**
    - **Industrial Relations Act 2012**
    - **Punjab Rent Restriction Ordinance**
    """)
    st.markdown("---")
    
    st.markdown("### About the System")
    st.markdown("""
    This system is an AI-powered legal assistant utilizing a **Retrieval-Augmented Generation (RAG)** pipeline.
    
    - **Database**: Local FAISS vector index
    - **Model**: Qwen2.5-1.5B-Instruct
    - **Embeddings**: paraphrase-multilingual-mpnet-base-v2
    """)
    st.markdown("---")
    
    st.markdown("### Disclaimer")
    st.caption("""
    *The assistant provides answers strictly grounded on the provided legal documents. It is for research and educational purposes only and does not constitute formal legal advice.*
    """)
    
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #6a7f72;'>Version 1.0.0 (Production)</p>", unsafe_allow_html=True)

# Main Application Area
st.markdown("<h1 class='legal-title'>⚖️ Pakistan Legal Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='legal-subtitle'>AI-Powered Retrieval-Augmented Legal Q&A System</p>", unsafe_allow_html=True)

# Initialize Session State for input value if it doesn't exist
if "user_query" not in st.session_state:
    st.session_state.user_query = ""

# Quick examples buttons
st.markdown("##### Quick Reference Examples:")
examples = [
    "What is FIR?",
    "What is Section 302 PPC?",
    "Can police arrest without warrant?",
    "Tenant rights in Punjab?"
]

cols = st.columns(len(examples))
for idx, ex in enumerate(examples):
    if cols[idx].button(ex, key=f"ex_btn_{idx}", use_container_width=True):
        st.session_state.user_query = ex
        st.rerun()

# Text Area Input
query_input = st.text_area(
    "Enter your legal question (English or Roman Urdu):",
    value=st.session_state.user_query,
    key="query_text_area",
    placeholder="Ask your legal question e.g. What is the punishment for murder under PPC?",
    height=120
)

# Keep the text synced
st.session_state.user_query = query_input

ask_button = st.button("Ask Legal Assistant", type="primary")

# Execute Search
if ask_button:
    # 1. Error Handling: Check empty query
    if not st.session_state.user_query.strip():
        st.warning("Please enter a legal question before submitting.")
    
    # 2. Error Handling: Check if imports and setup were successful
    elif not IMPORTS_OK:
        st.error("Error setting up application imports and utilities.")
        st.info(f"Detail: {IMPORT_ERROR}")
        
    else:
        # Check if database directory is built
        index_path = os.path.join(DB_DIR, "index.faiss")
        if not os.path.exists(index_path):
            st.error("FAISS database index not found. The vector database must be generated before querying.")
            st.info("Please run `python build_vector_db.py` to index the legal documents first.")
        else:
            try:
                # Progress sequence indicators
                status_box = st.status("Executing Search Pipeline...", expanded=True)
                
                with status_box:
                    st.write("🔍 Searching legal documents...")
                    time.sleep(0.5)
                    
                    st.write("📖 Retrieving relevant laws...")
                    # Retrieve the top 5 chunks
                    docs = retrieve_documents(st.session_state.user_query, k=5)
                    time.sleep(0.5)
                    
                    st.write("🧠 Generating answer using Qwen LLM...")
                    
                    # Construct context
                    context_chunks = []
                    for i, doc in enumerate(docs):
                        src = doc.metadata.get("source", "Unknown PDF")
                        title = doc.metadata.get("title", "Legal Document")
                        context_chunks.append(f"[{i+1}] Source: {src} ({title})\nContent: {doc.page_content}")
                    
                    context = "\n\n".join(context_chunks)
                    
                    # Construct template
                    prompt_template = get_prompt_template()
                    formatted_prompt = prompt_template.format(
                        context=context,
                        question=st.session_state.user_query
                    )
                    
                    # Generate response
                    answer = generate_answer(formatted_prompt)
                    
                    status_box.update(label="Query successfully processed!", state="complete", expanded=False)

                # Render Answer Box
                st.markdown(
                    f"""
                    <div class="answer-card">
                        <div class="answer-header">
                            <span>⚖️</span> Legal Assistant Grounded Response
                        </div>
                        <div style="font-size: 1.05rem; line-height: 1.6; color: #f0fdf4;">
                            {answer}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Render Sources
                st.markdown("### 📚 Retrieved Legal Reference Sources:")
                for idx, doc in enumerate(docs):
                    src = doc.metadata.get("source", "Unknown Document")
                    title = doc.metadata.get("title", "Legal Section")
                    chunk_id = doc.metadata.get("chunk_index", 0)
                    
                    with st.expander(f"Source {idx+1}: {title} ({src}) - Chunk {chunk_id}"):
                        st.markdown(f"**Document Content:**")
                        st.write(doc.page_content)
                        st.caption(f"Metadata: source={src} | chunk={chunk_id}")

            except FileNotFoundError as fnf:
                st.error("Vector database file not found. Make sure build_vector_db.py has run successfully.")
                st.exception(fnf)
            except RuntimeError as re_err:
                st.error("A model execution error occurred during processing.")
                st.exception(re_err)
            except Exception as e:
                st.error("An unexpected error occurred.")
                st.exception(e)

# Footer
st.markdown(
    """
    <div class="footer-text">
        Pakistan Legal Assistant &copy; 2026. Made for legal researchers, lawyers, and general public guidance.
    </div>
    """,
    unsafe_allow_html=True
)
