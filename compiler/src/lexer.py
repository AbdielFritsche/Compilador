import ply.lex as lex

# --- MAPEO DE PALABRAS RESERVADAS ---
reserved = {
    "program": "PROGRAM", "main": "MAIN", "var": "VAR", "end": "END",
    "int": "INT", "float": "FLOAT", "string": "STRING", "void": "VOID",
    "if": "IF", "else": "ELSE", "do": "DO", "while": "WHILE",
    "print": "PRINT", "class": "CLASS", "new": "NEW", "this": "THIS",
    "public": "PUBLIC", "private": "PRIVATE", "return": "RETURN"
}

# --- LISTA DE TOKENS ---
tokens = [
    'CTE_FLOAT', 'CTE_INT', 'CTE_STR', 'ID',
    'OP_EX_EQTH', 'OP_STRIC_NOTEQ',
    'OP_EQAS', 'OP_NOT_EQTH', 'OP_MIN_EQTH', 'OP_GRT_EQTH',
    'OP_AND', 'OP_OR', 'OP_DOBLE_NOT', 'OP_BIT_SHFL', 'OP_BIT_SHFR',
    'OP_ARROW', 'OP_INT_DIV', 'OP_SUM_ASSIGN', 'OP_SUB_ASSIGN',
    'OP_DIV_ASSIGN', 'OP_MUL_ASSIGN', 'OP_INC', 'OP_DEC',
    'OP_SUM', 'OP_SUB', 'OP_MUL', 'OP_DIV', 'OP_ASSIGN',
    'OP_MIN_TH', 'OP_GRT_TH', 'OP_NOT', 'OP_MOD',
    'OP_DOT', 'SEMICOLON', 'COLON', 'COMMA',
    'L_PAREN', 'R_PAREN', 'L_BRACE', 'R_BRACE', 'L_BRACKET', 'R_BRACKET'
] + list(reserved.values())

# --- REGLAS DE EXPRESIONES REGULARES ---

# Operadores de 3 caracteres
t_OP_EX_EQTH      = r'==='
t_OP_STRIC_NOTEQ  = r'!=='

# Operadores de 2 caracteres
t_OP_EQAS         = r'=='
t_OP_NOT_EQTH     = r'!='
t_OP_MIN_EQTH     = r'<='
t_OP_GRT_EQTH     = r'>='
t_OP_AND          = r'&&'
t_OP_OR           = r'\|\|'
t_OP_DOBLE_NOT    = r'!!'
t_OP_BIT_SHFL     = r'<<'
t_OP_BIT_SHFR     = r'>>'
t_OP_ARROW        = r'->'
t_OP_INT_DIV      = r'//'
t_OP_SUM_ASSIGN   = r'\+='
t_OP_SUB_ASSIGN   = r'-='
t_OP_DIV_ASSIGN   = r'/='
t_OP_MUL_ASSIGN   = r'\*='
t_OP_INC          = r'\+\+'
t_OP_DEC          = r'--'

# Operadores de 1 carácter
t_OP_SUM          = r'\+'
t_OP_SUB          = r'-'
t_OP_MUL          = r'\*'
t_OP_DIV          = r'/'
t_OP_ASSIGN       = r'='
t_OP_MIN_TH       = r'<'
t_OP_GRT_TH       = r'>'
t_OP_NOT          = r'!'
t_OP_MOD          = r'%'
t_OP_DOT          = r'\.'

# Delimitadores
t_SEMICOLON       = r';'
t_COLON           = r':'
t_COMMA           = r','
t_L_PAREN         = r'\('
t_R_PAREN         = r'\)'
t_L_BRACE         = r'\{'
t_R_BRACE         = r'\}'
t_L_BRACKET       = r'\['
t_R_BRACKET       = r'\]'


def t_CTE_FLOAT(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_CTE_INT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_CTE_STR(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1] 
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_comment(t):
    r'\#.*'
    pass # No devuelve token, solo salta el texto

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"*** Error Léxico en línea {t.lineno}: símbolo desconocido '{t.value[0]}' ***")
    t.lexer.skip(1)

# Constructor
lexer = lex.lex()