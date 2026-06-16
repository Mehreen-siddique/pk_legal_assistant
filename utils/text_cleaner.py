import re

def clean_text(text: str) -> str:
    """
    Cleans raw text extracted from PDFs by removing duplicate whitespaces,
    rejoining lines broken by hyphens, removing consecutive blank lines, 
    and correcting spacing.
    
    Args:
        text (str): Raw input text.
        
    Returns:
        str: Cleaned text.
    """
    if not text:
        return ""
        
    # 1. Rejoin words hyphenated at line breaks (e.g. "con-\nstitution" -> "constitution")
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    
    # 2. Split into lines to clean individually
    lines = text.split("\n")
    cleaned_lines = []
    
    for line in lines:
        # Trim leading and trailing whitespace
        line = line.strip()
        
        # Remove repeated headers/footers or typical page numbers (e.g. "Page 1 of 10")
        if re.match(r'^(Page\s+\d+|[0-9]+)$', line, re.IGNORECASE):
            continue
            
        # Normalize multiple spaces within a single line to a single space
        line = re.sub(r'\s+', ' ', line)
        
        if line:
            cleaned_lines.append(line)
            
    # 3. Join lines back together with single newlines
    cleaned_text = "\n".join(cleaned_lines)
    
    # 4. Normalize any duplicate blank spaces or newlines
    cleaned_text = re.sub(r'\n+', '\n', cleaned_text)
    cleaned_text = re.sub(r'[ \t]+', ' ', cleaned_text)
    
    return cleaned_text.strip()
