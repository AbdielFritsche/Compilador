import ply.lex as lex
import ply.yacc as yacc

# Lexico

reserved = {
    'program' : 'PROGRAM',
    'var'     : 'VAR',
    'main'    : 'MAIN',
    'end'     : 'END',
    'int'     : 'INT',
    'float'   : 'FLOAT',
    'string'  : 'STRING_T',
    'bool'    : 'BOOL',
    'if'      : 'IF',
    'else'    : 'ELSE',
    'true'    : 'TRUE',   
    'false'   : 'FALSE',
}

tokens = list(reserved.values()) + [
    'ID', 'CONS_INT', 'CONS_FLOAT', 'CONS_STRING',
    'OPASIGNA',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'GT', 'LT', 'GTE', 'LTE', 'EQ', 'NEQ',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'SEMICOL', 'COLON', 'COMMA',
]

t_OPASIGNA = r'='
t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'
t_GTE      = r'>='
t_LTE      = r'<='
t_GT       = r'>'
t_LT       = r'<'
t_EQ       = r'=='
t_NEQ      = r'!='
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_LBRACE   = r'\{'
t_RBRACE   = r'\}'
t_SEMICOL  = r';'
t_COLON    = r':'
t_COMMA    = r','
t_ignore   = ' \t'

def t_CONS_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CONS_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CONS_STRING(t):
    r'\"[^\"]*\"'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    errors.append(
        "Error lexico: caracter ilegal '{}' en linea {}".format(
            t.value[0], t.lexer.lineno))
    t.lexer.skip(1)

lexer = lex.lex()

class Persistent:
    def __init__(self):
        self.stack_ops   = [('none', 'none')]
        self.stack_args  = [('none', 'none')]
        self.nquads      = 0
        self.count_temps = 0
        self.quad_list   = []

# Tabla de simbolos: names['main'] = { 'A': {'tipo':'int', 'has_value':False} }
names = {}
names['main'] = {}

# Cubo semantico: (tipo_izq, tipo_der, operador) -> tipo_resultado
cubo = {
    # --- asignacion ---
    ('int',    'int',    '=') : 'int',
    ('float',  'float',  '=') : 'float',
    ('float',  'int',    '=') : 'float',   
    ('string', 'string', '=') : 'string',
    ('bool',   'bool',   '=') : 'bool',
    # --- suma ---
    ('int',   'int',   '+') : 'int',
    ('float', 'float', '+') : 'float',
    ('int',   'float', '+') : 'float',
    ('float', 'int',   '+') : 'float',
    # --- resta ---
    ('int',   'int',   '-') : 'int',
    ('float', 'float', '-') : 'float',
    ('int',   'float', '-') : 'float',
    ('float', 'int',   '-') : 'float',
    # --- multiplicacion ---
    ('int',   'int',   '*') : 'int',
    ('float', 'float', '*') : 'float',
    ('int',   'float', '*') : 'float',
    ('float', 'int',   '*') : 'float',
    # --- division ---
    ('int',   'int',   '/') : 'float',
    ('float', 'float', '/') : 'float',
    ('int',   'float', '/') : 'float',
    ('float', 'int',   '/') : 'float',
    # --- igualdad booleana ---
    ('bool',  'bool',  '==') : 'bool',
    ('bool',  'bool',  '!=') : 'bool',
    # --- relacionales ---
    ('int',   'int',   '>')  : 'bool',
    ('float', 'float', '>')  : 'bool',
    ('int',   'float', '>')  : 'bool',
    ('float', 'int',   '>')  : 'bool',
    ('int',   'int',   '<')  : 'bool',
    ('float', 'float', '<')  : 'bool',
    ('int',   'float', '<')  : 'bool',
    ('float', 'int',   '<')  : 'bool',
    ('int',   'int',   '>=') : 'bool',
    ('float', 'float', '>=') : 'bool',
    ('int',   'float', '>=') : 'bool',
    ('float', 'int',   '>=') : 'bool',
    ('int',   'int',   '<=') : 'bool',
    ('float', 'float', '<=') : 'bool',
    ('int',   'float', '<=') : 'bool',
    ('float', 'int',   '<=') : 'bool',
    ('int',   'int',   '==') : 'bool',
    ('float', 'float', '==') : 'bool',
    ('int',   'float', '==') : 'bool',
    ('float', 'int',   '==') : 'bool',
    ('int',   'int',   '!=') : 'bool',
    ('float', 'float', '!=') : 'bool',
    ('int',   'float', '!=') : 'bool',
    ('float', 'int',   '!=') : 'bool',
}

ds         = Persistent()
errors     = []
jump_stack = []

class ParseAbort(Exception):
    pass

# Funciones para semantica

def semantica_trad_ops(op):
    """Pop dos operandos, consulta cubo, emite quad, push temporal."""
    if (len(ds.stack_args) < 2
            or ds.stack_args[-1][0] == 'none'
            or ds.stack_args[-2][0] == 'none'):
        errors.append(
            "Error semantico: operandos insuficientes para '{}'".format(op))
        ds.stack_args.append(('error', 'error'))
        return

    arg_R, tipo_R = ds.stack_args.pop()
    arg_L, tipo_L = ds.stack_args.pop()


    if tipo_L == 'error' or tipo_R == 'error':
        ds.stack_args.append(('error', 'error'))
        return

    key      = (tipo_L, tipo_R, op)
    tipo_res = cubo.get(key, None)

    if tipo_res is None:
        errors.append(
            "Error semantico: operacion '{}' no permitida entre tipos "
            "'{}' y '{}'".format(op, tipo_L, tipo_R))
        ds.stack_args.append(('error', 'error'))
        return

    ds.count_temps += 1
    temp = 't' + str(ds.count_temps)
    ds.stack_args.append((temp, tipo_res))
    ds.nquads += 1
    ds.quad_list.append([ds.nquads, op, arg_L, arg_R, temp, tipo_res])


def semantica_asigna(var_name, lineno):
    """Verifica tipo mediante el cubo y emite quad de asignacion.

    lineno: numero de linea del ID del lado izquierdo (de p.lineno(1)).
    """
    if not ds.stack_args or ds.stack_args[-1][0] == 'none':
        errors.append(
            "Error semantico [linea {}]: sin valor para asignar a "
            "'{}'".format(lineno, var_name))
        return

    val, tipo_val = ds.stack_args.pop()

    if tipo_val == 'error':
        return

    tipo_var     = None
    target_scope = None
    for scope_table in names.values():
        if var_name in scope_table:
            tipo_var     = scope_table[var_name]['tipo']
            target_scope = scope_table
            break

    if tipo_var is None:
        errors.append(
            "Error semantico [linea {}]: variable '{}' no fue declarada "
            "en la seccion var".format(lineno, var_name))
        return

    res_type = cubo.get((tipo_var, tipo_val, '='), None)
    if res_type is None:
        errors.append(
            "Error semantico [linea {}]: no se puede asignar tipo '{}' "
            "a la variable '{}' de tipo '{}'".format(
                lineno, tipo_val, var_name, tipo_var))
        return

    target_scope[var_name]['has_value'] = True
    ds.nquads += 1
    ds.quad_list.append([ds.nquads, '=', val, '_', var_name, tipo_var])


def emit_gotof(cond, tipo_cond, lineno):
    """Emite GOTOF con destino pendiente; guarda indice en jump_stack.

    Si la condicion ya es 'error' (viene de variable no declarada) no
    emitimos un segundo mensaje sobre 'debe ser bool' porque ya se
    reporto el error de origen.
    """
    if tipo_cond != 'bool' and tipo_cond != 'error':
        errors.append(
            "Error semantico [linea {}]: la condicion del 'if' debe "
            "producir un valor bool, se recibio '{}'".format(lineno, tipo_cond))
    ds.nquads += 1
    ds.quad_list.append([ds.nquads, 'GOTOF', cond, '_', '?', 'bool'])
    jump_stack.append(len(ds.quad_list) - 1)


def emit_goto():
    """Emite GOTO con destino pendiente; guarda indice en jump_stack."""
    ds.nquads += 1
    ds.quad_list.append([ds.nquads, 'GOTO', '_', '_', '?', ''])
    jump_stack.append(len(ds.quad_list) - 1)


def backpatch(idx, dest):
    """Rellena el destino del quad en posicion idx (0-based en quad_list)."""
    ds.quad_list[idx][4] = str(dest)


# Gramatica y reglas de produccion

def p_program(p):
    '''program : PROGRAM ID SEMICOL opt_vars MAIN LBRACE body RBRACE END'''

def p_opt_vars(p):
    '''opt_vars : VAR var_decl_list
               | empty'''

def p_var_decl_list(p):
    '''var_decl_list : var_decl var_decl_list
                     | var_decl'''

def p_var_decl(p):
    '''var_decl : id_list COLON tipo SEMICOL'''
    tipo = p[3]
    for nombre, lineno_id in p[1]:
        if nombre in names['main']:
            errors.append(
                "Error semantico [linea {}]: variable '{}' ya fue "
                "declarada anteriormente".format(lineno_id, nombre))
        else:
            names['main'][nombre] = {'tipo': tipo, 'has_value': False}

def p_id_list_multi(p):
    '''id_list : ID COMMA id_list'''
    p[0] = [(p[1], p.lineno(1))] + p[3]

def p_id_list_single(p):
    '''id_list : ID'''
    p[0] = [(p[1], p.lineno(1))]

def p_tipo(p):
    '''tipo : INT
            | FLOAT
            | STRING_T
            | BOOL'''
    p[0] = p[1]

def p_body(p):
    '''body : statement_list'''

def p_statement_list_multi(p):
    '''statement_list : statement statement_list'''

def p_statement_list_single(p):
    '''statement_list : statement'''

def p_statement_asigna(p):
    '''statement : asigna'''

def p_statement_condicional(p):
    '''statement : condicional'''

def p_asigna(p):
    '''asigna : ID OPASIGNA exp SEMICOL'''
    semantica_asigna(p[1], p.lineno(1))

def p_condicional(p):
    '''condicional : IF LPAREN exp RPAREN gotof_action LBRACE body RBRACE goto_action else_part SEMICOL'''

def p_gotof_action(p):
    '''gotof_action : empty'''
    if not ds.stack_args or ds.stack_args[-1][0] == 'none':
        errors.append(
            "Error semantico: condicion del 'if' no encontrada o invalida")
        cond, tipo = 'error', 'error'
    else:
        cond, tipo = ds.stack_args.pop()
    emit_gotof(cond, tipo, p.lineno(0))

def p_goto_action(p):
    '''goto_action : empty'''
    emit_goto()
    if len(jump_stack) < 2:
        return
    goto_idx  = jump_stack.pop()
    gotof_idx = jump_stack.pop()
    backpatch(gotof_idx, ds.nquads + 1)
    jump_stack.append(goto_idx)

def p_else_part_with_else(p):
    '''else_part : ELSE LBRACE body RBRACE'''
    if not jump_stack:
        return
    goto_idx = jump_stack.pop()
    backpatch(goto_idx, ds.nquads + 1)

def p_else_part_empty(p):
    '''else_part : empty'''
    if not jump_stack:
        return
    goto_idx = jump_stack.pop()
    backpatch(goto_idx, ds.nquads + 1)

def p_exp_relacional(p):
    '''exp : exp GT  exp_arit
           | exp LT  exp_arit
           | exp GTE exp_arit
           | exp LTE exp_arit
           | exp EQ  exp_arit
           | exp NEQ exp_arit'''
    semantica_trad_ops(p[2])

def p_exp_simple(p):
    '''exp : exp_arit'''

def p_exp_arit_plus(p):
    '''exp_arit : exp_arit PLUS term'''
    semantica_trad_ops('+')

def p_exp_arit_minus(p):
    '''exp_arit : exp_arit MINUS term'''
    semantica_trad_ops('-')

def p_exp_arit(p):
    '''exp_arit : term'''

def p_term_times(p):
    '''term : term TIMES factor'''
    semantica_trad_ops('*')

def p_term_divide(p):
    '''term : term DIVIDE factor'''
    semantica_trad_ops('/')

def p_term(p):
    '''term : factor'''

def p_factor_paren(p):
    '''factor : LPAREN exp RPAREN'''

def p_factor_id(p):
    '''factor : ID'''
    entry = None
    for scope_table in names.values():
        if p[1] in scope_table:
            entry = scope_table[p[1]]
            break
    if entry is None:
        errors.append(
            "Error semantico [linea {}]: variable '{}' no fue declarada "
            "en la seccion var".format(p.lineno(1), p[1]))
        ds.stack_args.append((p[1], 'error'))
    else:
        ds.stack_args.append((p[1], entry['tipo']))

def p_factor_cons_int(p):
    '''factor : CONS_INT'''
    ds.stack_args.append((p[1], 'int'))

def p_factor_cons_float(p):
    '''factor : CONS_FLOAT'''
    ds.stack_args.append((p[1], 'float'))

def p_factor_cons_string(p):
    '''factor : CONS_STRING'''
    ds.stack_args.append((p[1], 'string'))

def p_factor_cons_bool(p):
    '''factor : TRUE
              | FALSE'''
    ds.stack_args.append((p[1], 'bool'))

def p_empty(p):
    '''empty :'''

def p_error(t):
    if t is not None:
        errors.append(
            "Error sintactico [linea {}]: token inesperado '{}'".format(
                t.lineno, t.value))
    else:
        errors.append("Error sintactico: fin de archivo inesperado")
    raise ParseAbort()


# Parser construido
parser = yacc.yacc(debug=False, write_tables=False, errorlog=yacc.NullLogger())

input = open("input.txt").read()

try:
    parser.parse(input, lexer=lexer)
except ParseAbort:
    pass

if errors:
    print("Se encontraron errores. No se generan quadruplos.")
    print()
    for e in errors:
        print(e)
else:
    print("Quadruplos")
    print("{:<5} {:<8} {:<12} {:<12} {:<12} {:<8}".format(
        "No.", "Op", "Arg1", "Arg2", "Result", "Tipo"))
    print("-" * 60)
    for q in ds.quad_list:
        print("{:<5} {:<8} {:<12} {:<12} {:<12} {:<8}".format(
            q[0], str(q[1]), str(q[2]), str(q[3]), str(q[4]), str(q[5])))
    print()
    print("Tabla de Simbolos")
    print("{:<6} {:<15} {:<10}".format("Scope", "Nombre", "Tipo"))
    print("-" * 33)
    for scope, tabla in names.items():
        for nombre, info in tabla.items():
            print("{:<6} {:<15} {:<10}".format(scope, nombre, info['tipo']))