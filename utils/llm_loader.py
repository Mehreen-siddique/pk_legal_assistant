import os
import torch
import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

@st.cache_resource
def get_qwen_pipeline():
    """
    Loads Qwen/Qwen2.5-1.5B-Instruct and wraps it in a transformers pipeline.
    Utilizes CUDA if available, otherwise runs on CPU with memory optimizations.
    Uses @st.cache_resource to prevent reloading the model on every streamlit rerun.
    """
    model_name = "Qwen/Qwen2.5-1.5B-Instruct"
    
    # Check GPU availability
    if torch.cuda.is_available():
        device_map = "auto"
        torch_dtype = torch.float16
        print("GPU detected. Loading Qwen on CUDA...")
    else:
        device_map = None
        torch_dtype = torch.float32
        print("No GPU detected. Loading Qwen on CPU...")

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        # Ensure pad token is set
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch_dtype,
            device_map=device_map,
            low_cpu_mem_usage=True
        )
        
        # If CPU, set device explicitly in pipeline; otherwise device_map handles it
        pipe_device = -1 if device_map is None else None
        
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=512,
            temperature=0.2,
            top_p=0.9,
            do_sample=True,
            device=pipe_device,
            pad_token_id=tokenizer.eos_token_id
        )
        return pipe
    except Exception as e:
        print(f"Failed to load model {model_name}: {str(e)}")
        raise RuntimeError(f"Model load error: {str(e)}")

def generate_answer(prompt: str) -> str:
    """
    Generates a response from the Qwen model given a formatted prompt.
    Splits the generated text to return only the model's new response.
    """
    pipe = get_qwen_pipeline()
    try:
        outputs = pipe(prompt, return_full_text=False)
        return outputs[0]["generated_text"].strip()
    except Exception as e:
        print(f"Error during generation: {str(e)}")
        raise RuntimeError(f"Text generation failed: {str(e)}")
