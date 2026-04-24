# 🚀 Construcción de Compilador - Analizador Léxico (Fase 1)

Este proyecto implementa la primera fase del front-end de un compilador: el **Analizador Léxico (Lexer)**. Está desarrollado en Python utilizando la librería **PLY (Python Lex-Yacc)** y es capaz de tokenizar código fuente de un lenguaje con soporte para programación orientada a objetos (POO), múltiples tipos de datos y operadores complejos.

---

## 📁 Estructura del Proyecto

El proyecto sigue una arquitectura modular para separar la lógica del compilador de las pruebas:

```text
Compilador/
├── src/
│   ├── __init__.py
│   └── lexer.py                 # Definición de expresiones regulares y tokens
├── tests/
│   ├── inputs/                  # Archivos .txt con código fuente de prueba
│   ├── test_lexer_codes.py      # Archivo que lee y tokeniza dinámicamente los .txt
│   └── test_lexer_functions.py  # Pruebas unitarias estrictas de tokens y prioridades
├── main.py                      # Punto de entrada para pruebas rápidas
└── requirements.txt             # Dependencias del entorno
```

---

## 🛠️ Requisitos Previos

- Python 3.8+
- Se recomienda encarecidamente utilizar un entorno virtual (`.venv`).

---

## ⚙️ Instalación y Configuración

### 1. Crear y activar el entorno virtual

Abre tu terminal (PowerShell) en la raíz del proyecto y ejecuta:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

Con el entorno virtual activado `(.venv)`, instala PLY y Pytest:

```powershell
python -m pip install ply pytest
```

---

## ▶️ Uso y Ejecución

### Ejecución rápida

Para probar el lexer con el bloque de código configurado por defecto, ejecuta el archivo principal:

```powershell
python main.py
```

**Salida esperada:** una tabla en la consola mostrando cada valor detectado junto a su etiqueta de token correspondiente (ej. `VAR`, `ID`, `CTE_INT`).

---

## 🧪 Pruebas Automatizadas (Testing)

El proyecto cuenta con un entorno de pruebas robusto diseñado con `pytest`, dividido en:

- `test_lexer_codes.py` — pruebas sobre archivos de código fuente externos.
- `test_lexer_functions.py` — pruebas unitarias de lógica, tokens y prioridades.

Para ejecutar todas las pruebas con reporte detallado en tiempo real, colócate en la raíz del proyecto y ejecuta:

```powershell
python -m pytest -sv
```

**Descripción de las banderas:**

| Bandera | Nombre | Efecto |
|--------|--------|--------|
| `-s` | Capture Off | Muestra todos los `print()` definidos en el código (ideal para ver tablas de tokens) |
| `-v` | Verbose | Muestra el nombre de cada prueba y su estado (`PASSED` / `FAILED`) |

### Probar tus propios scripts

Para probar nuevos bloques de código de forma escalable:

1. Crea un archivo de texto (ej. `mi_algoritmo.txt`) con tu código fuente.
2. Guárdalo dentro de la carpeta `tests/inputs/`.
3. Ejecuta `python -m pytest -sv`.

El script `test_lexer_codes.py` detectará tu archivo automáticamente, lo leerá, lo pasará por el lexer y mostrará el flujo de tokens en la consola.

---

## 📚 Características del Lenguaje Soportadas

El Lexer está configurado para reconocer los siguientes elementos:

| Categoría | Descripción |
|-----------|-------------|
| **Palabras reservadas** | `class`, `public`, `private`, `new`, `this`, `if`, `while`, `program`, `main`, entre otras |
| **Tipos de datos** | Enteros (`CTE_INT`), Flotantes (`CTE_FLOAT`) y Cadenas de texto (`CTE_STR`) |
| **Operadores complejos** | Prioridad automática para operadores de 3 caracteres (`===`), 2 caracteres (`++`, `+=`, `&&`, `<<`) y 1 carácter |
| **Manejo de errores** | Omisión de comentarios (`#`) y detección de caracteres ilegales con indicación del número de línea |