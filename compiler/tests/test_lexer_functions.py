import pytest 
from src.lexer import lexer

def get_tokens(code: str):
    """Funcion para obtener la lista de tipos de tokens"""
    lexer.input(code)
    return [tok.type for tok in lexer]

def test_reserved_words():
    """Verifica que las palabras reservadas se reconozcan correctamente"""
    code = "program main var if else while class return"
    expected_tokens_tokens = ['PROGRAM', 'MAIN', 'VAR', 'IF', 'ELSE', 'WHILE', 'CLASS', 'RETURN']
    assert get_tokens(code) == expected_tokens_tokens

def test_operators_priority():
    """Verifica que operadores largos tengan prioridad (=== vs ==)."""
    code = "=== == ="
    expected_tokens = ['OP_EX_EQTH', 'OP_EQAS', 'OP_ASSIGN']
    assert get_tokens(code) == expected_tokens

@pytest.mark.parametrize("code,expected_tokens_type", [
    ("123", "CTE_INT"),
    ("12.34", "CTE_FLOAT"),
    ('"Hola Mundo"', "CTE_STR"),
    ("mi_variable", "ID"),
])
def test_constants_and_ids(code, expected_tokens_type):
    """Prueba tipos de datos básicos."""
    tokens = get_tokens(code)
    assert tokens == [expected_tokens_type]

def test_complex_expression():
    """Prueba una línea de código completa."""
    code = "var x = 10.5 + (y * 2);"
    expected_tokens_tokens = [
        'VAR', 'ID', 'OP_ASSIGN', 'CTE_FLOAT', 'OP_SUM', 
        'L_PAREN', 'ID', 'OP_MUL', 'CTE_INT', 'R_PAREN', 'SEMICOLON'
    ]
    assert get_tokens(code) == expected_tokens_tokens

def test_comment_ignored():
    """Verifica que los comentarios no generen tokens."""
    code = "var x; # Esto es un comentario"
    expected_tokens = ['VAR', 'ID', 'SEMICOLON']
    assert get_tokens(code) == expected_tokens