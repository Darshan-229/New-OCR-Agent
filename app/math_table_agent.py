import re

def extract_math_expressions(text):
    """
    Extract potential math expressions using regex patterns.
    This is a basic version – can be improved with a proper math parser.
    """
    print("[INFO] Searching for math expressions...")
    
    math_patterns = [
        r'\d+\s*[\+\-\*/]\s*\d+',                # Basic arithmetic (e.g., 2 + 3)
        r'\d+\s*=\s*\d+',                        # Simple equations (e.g., 2 = 4)
        r'[\d\+\-\*/\^\(\)\s]+=[\d\s\+\-\*/\^]*' # Complex math (e.g., (2 + 3) * 4 = 20)
    ]
    
    found_expressions = []
    for pattern in math_patterns:
        found_expressions += re.findall(pattern, text)

    return list(set(found_expressions))  # Remove duplicates


def extract_tables(text):
    """
    Extract basic table-like text based on line and column structure.
    This doesn't parse real tables but finds rows with multiple spaces or tabs.
    """
    print("[INFO] Searching for table-like structures...")

    lines = text.split('\n')
    table_data = []

    for line in lines:
        if re.search(r'(\s{2,}|\t)', line):  # Look for multiple spaces or tabs
            table_data.append(line.strip())

    return table_data
