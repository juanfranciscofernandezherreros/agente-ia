"""
tools.py - Herramientas que el agente puede usar
"""
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
import math

# Herramienta 1: Búsqueda en internet
search = DuckDuckGoSearchRun()


@tool
def search_web(query: str) -> str:
    """
    Busca información en internet.
    Útil para obtener datos actuales, noticias, precios, etc.

    Args:
        query: La búsqueda a realizar
    """
    return search.run(query)


@tool
def calculator(expression: str) -> str:
    """
    Realiza cálculos matemáticos.
    Soporta: +, -, *, /, **, sqrt(), sin(), cos(), etc.

    Args:
        expression: La expresión matemática a evaluar (ej: "2 + 2", "sqrt(16)")
    """
    try:
        # Hacer disponibles funciones matemáticas
        allowed_names = {
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "pi": math.pi,
            "e": math.e,
            "abs": abs,
            "round": round,
        }
        # SEGURIDAD: eval() con builtins restringidos. No usar en producción
        # sin sandbox adicional (Docker, E2B, etc.)
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"Resultado: {result}"
    except Exception as e:
        return f"Error en el cálculo: {str(e)}"


@tool
def run_python(code: str) -> str:
    """
    Ejecuta código Python simple.
    Útil para procesamiento de datos, manipulación de strings, etc.
    ⚠️ Solo para código seguro y simple.

    Args:
        code: Código Python a ejecutar
    """
    try:
        # SEGURIDAD: exec() con builtins restringidos. No usar en producción
        # sin sandbox adicional (Docker, E2B, etc.)
        local_vars = {}
        exec(
            code,
            {
                "__builtins__": {
                    "print": print,
                    "len": len,
                    "range": range,
                    "str": str,
                    "int": int,
                    "float": float,
                    "list": list,
                    "dict": dict,
                }
            },
            local_vars,
        )

        # Capturar resultado si hay variable 'result'
        if "result" in local_vars:
            return f"Resultado: {local_vars['result']}"
        return "Código ejecutado correctamente"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def get_current_datetime() -> str:
    """
    Obtiene la fecha y hora actual.
    Útil para saber qué día es, calcular plazos, etc.
    """
    from datetime import datetime

    now = datetime.now()
    return f"Fecha y hora actual: {now.strftime('%d/%m/%Y %H:%M:%S')}"


# Lista de todas las herramientas
all_tools = [search_web, calculator, run_python, get_current_datetime]
