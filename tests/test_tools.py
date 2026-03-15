"""
test_tools.py - Tests para las herramientas del agente
"""
import re

import pytest

from tools import calculator, run_python, get_current_datetime, all_tools


# ---- Tests para calculator ----

class TestCalculator:
    """Tests para la herramienta calculator."""

    def test_addition(self):
        assert calculator.invoke("2 + 2") == "Resultado: 4"

    def test_multiplication(self):
        assert calculator.invoke("3 * 7") == "Resultado: 21"

    def test_division(self):
        assert calculator.invoke("10 / 4") == "Resultado: 2.5"

    def test_power(self):
        assert calculator.invoke("2 ** 10") == "Resultado: 1024"

    def test_sqrt(self):
        assert calculator.invoke("sqrt(16)") == "Resultado: 4.0"

    def test_pi(self):
        result = calculator.invoke("pi")
        assert "3.14159" in result

    def test_complex_expression(self):
        assert calculator.invoke("round(sqrt(2), 4)") == "Resultado: 1.4142"

    def test_invalid_expression(self):
        result = calculator.invoke("invalid_func()")
        assert "Error" in result

    def test_division_by_zero(self):
        result = calculator.invoke("1 / 0")
        assert "Error" in result

    def test_builtins_restricted(self):
        result = calculator.invoke("__import__('os').system('echo hacked')")
        assert "Error" in result


# ---- Tests para run_python ----

class TestRunPython:
    """Tests para la herramienta run_python."""

    def test_simple_assignment(self):
        result = run_python.invoke("result = 42")
        assert result == "Resultado: 42"

    def test_no_result_variable(self):
        result = run_python.invoke("x = 10")
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
        result = run_python.invoke(code)
        assert result == "Resultado: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]"

    def test_string_manipulation(self):
        result = run_python.invoke("result = str(len('hello'))")
        assert result == "Resultado: 5"

    def test_syntax_error(self):
        result = run_python.invoke("def (invalid")
        assert "Error" in result

    def test_restricted_import(self):
        result = run_python.invoke("import os")
        assert "Error" in result

    def test_list_operations(self):
        result = run_python.invoke("result = list(range(5))")
        assert result == "Resultado: [0, 1, 2, 3, 4]"


# ---- Tests para get_current_datetime ----

class TestGetCurrentDatetime:
    """Tests para la herramienta get_current_datetime."""

    def test_returns_string(self):
        result = get_current_datetime.invoke({})
        assert isinstance(result, str)

    def test_format(self):
        result = get_current_datetime.invoke({})
        assert "Fecha y hora actual:" in result
        # Check date/time format dd/mm/YYYY HH:MM:SS
        pattern = r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}"
        assert re.search(pattern, result) is not None


# ---- Tests para all_tools list ----

class TestAllTools:
    """Tests para verificar que all_tools está configurado correctamente."""

    def test_all_tools_count(self):
        assert len(all_tools) == 4

    def test_all_tools_names(self):
        names = [t.name for t in all_tools]
        assert "search_web" in names
        assert "calculator" in names
        assert "run_python" in names
        assert "get_current_datetime" in names
