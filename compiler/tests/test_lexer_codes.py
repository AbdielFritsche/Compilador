import glob
import pytest
import os
from src.lexer import lexer

INPUTS_DIR = os.path.join(os.path.dirname(__file__), "inputs")

txt_files = glob.glob(os.path.join(INPUTS_DIR, "*.txt"))

@pytest.mark.parametrize("file_path", txt_files)
def test_all_txt_files(file_path):
    """Carga y tokeniza automáticamente cualquier .txt en la carpeta."""
    
    filename = os.path.basename(file_path)
    print(f"\n\n--- Tokenizando archivo: {filename} ---")

    with open(file_path, "r") as f:
        code = f.read()

    lines = code.split('\n')

    lexer.lineno = 1 
    lexer.input(code)

    current_line = -1

    for tok in lexer:
        if tok.lineno != current_line:
            current_line = tok.lineno
            line_code = lines[current_line - 1].strip() if current_line <= len(lines) else ""
            print(f"\nLinea {current_line}:    {line_code}")
        
        print(f"{tok.type:<15} value: {str(tok.value):<10} lexpos: {tok.lexpos}")
        
        assert tok.type is not None