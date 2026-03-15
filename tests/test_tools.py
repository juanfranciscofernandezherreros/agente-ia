"""
test_tools.py - Tests para las herramientas del agente
"""
import math
import re

import pytest


# ---- Tests para calculator ----

class TestCalculator:
    """Tests para la herramienta calculator."""

    def _calculator(self, expression: str) -> str:
        """Lógica interna de calculator (sin decorador @tool)."""
        try:
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
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return f"Resultado: {result}"
        except Exception as e:
            return f"Error en el cálculo: {str(e)}"

    def test_addition(self):
        assert self._calculator("2 + 2") == "Resultado: 4"

    def test_multiplication(self):
        assert self._calculator("3 * 7") == "Resultado: 21"

    def test_division(self):
        assert self._calculator("10 / 4") == "Resultado: 2.5"

    def test_power(self):
        assert self._calculator("2 ** 10") == "Resultado: 1024"

    def test_sqrt(self):
        assert self._calculator("sqrt(16)") == "Resultado: 4.0"

    def test_pi(self):
        result = self._calculator("pi")
        assert "3.14159" in result

    def test_complex_expression(self):
        assert self._calculator("round(sqrt(2), 4)") == "Resultado: 1.4142"

    def test_invalid_expression(self):
        result = self._calculator("invalid_func()")
        assert "Error" in result

    def test_division_by_zero(self):
        result = self._calculator("1 / 0")
        assert "Error" in result

    def test_builtins_restricted(self):
        result = self._calculator("__import__('os').system('echo hacked')")
        assert "Error" in result


# ---- Tests para run_python ----

class TestRunPython:
    """Tests para la herramienta run_python."""

    def _run_python(self, code: str) -> str:
        """Lógica interna de run_python (sin decorador @tool)."""
        try:
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
            if "result" in local_vars:
                return f"Resultado: {local_vars['result']}"
            return "Código ejecutado correctamente"
        except Exception as e:
            return f"Error: {str(e)}"

    def test_simple_assignment(self):
        result = self._run_python("result = 42")
        assert result == "Resultado: 42"

    def test_no_result_variable(self):
        result = self._run_python("x = 10")
        assert result == "Código ejecutado correctamente"

    def test_fibonacci(self):
        code = """
def fibonacci(n):
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib[:n]

result = fibonacci(10)
"""
        result = self._run_python(code)
        assert result == "Resultado: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]"

    def test_string_manipulation(self):
        result = self._run_python("result = str(len('hello'))")
        assert result == "Resultado: 5"

    def test_syntax_error(self):
        result = self._run_python("def (invalid")
        assert "Error" in result

    def test_restricted_import(self):
        result = self._run_python("import os")
        assert "Error" in result

    def test_list_operations(self):
        result = self._run_python("result = list(range(5))")
        assert result == "Resultado: [0, 1, 2, 3, 4]"


# ---- Tests para get_current_datetime ----

class TestGetCurrentDatetime:
    """Tests para la herramienta get_current_datetime."""

    def _get_current_datetime(self) -> str:
        from datetime import datetime
        now = datetime.now()
        return f"Fecha y hora actual: {now.strftime('%d/%m/%Y %H:%M:%S')}"

    def test_returns_string(self):
        result = self._get_current_datetime()
        assert isinstance(result, str)

    def test_format(self):
        result = self._get_current_datetime()
        assert "Fecha y hora actual:" in result
        # Check date/time format dd/mm/YYYY HH:MM:SS
        pattern = r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}"
        assert re.search(pattern, result) is not None


# ---- Tests para all_tools list ----

class TestAllTools:
    """Tests para verificar que all_tools está configurado correctamente."""

    def test_all_tools_count(self):
        from tools import all_tools
        assert len(all_tools) == 4

    def test_all_tools_names(self):
        from tools import all_tools
        names = [t.name for t in all_tools]
        assert "search_web" in names
        assert "calculator" in names
        assert "run_python" in names
        assert "get_current_datetime" in names
