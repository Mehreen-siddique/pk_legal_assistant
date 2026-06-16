from langchain_core.prompts import PromptTemplate

# Exact prompt structure from specification
PROMPT_TEMPLATE_STR = """You are Pakistan Legal Assistant.

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

Answer:"""

def get_prompt_template() -> PromptTemplate:
    """
    Returns the LangChain PromptTemplate object for Pakistan Legal Assistant.
    """
    return PromptTemplate(
        input_variables=["context", "question"],
        template=PROMPT_TEMPLATE_STR
    )
