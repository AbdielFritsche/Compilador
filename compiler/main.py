from src import lexer

data = """
# Mi programa de prueba
program main {
    var x = 10.5;
    if (x === 10.5) {
        print("Hola Mundo");
    }
}
"""

lexer.input(data)

for tok in lexer:
    # tok.type es la etiqueta, tok.value es el lexema
    print(f"{str(tok.value):<15} {tok.type}")