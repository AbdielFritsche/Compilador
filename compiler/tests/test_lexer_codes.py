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
    
    lexer.input(code)
    
    print(f"{'TOKEN_ID':<15} | CONTENIDO")
    print("-" * 30)
    
    for tok in lexer:
        print(f"{tok.type:<15} | {str(tok.value)}")
        
        assert tok.type is not None