"""
test_agent.py - Tests para las funciones del agente
"""
from unittest.mock import patch, MagicMock

from agent import batch_chat


# ---- Tests para batch_chat ----

class TestBatchChat:
    """Tests para la función batch_chat."""

    @patch("agent.create_agent")
    def test_batch_chat_returns_results(self, mock_create_agent):
        mock_agent = MagicMock()
        mock_agent.invoke.side_effect = [
            {"output": "4"},
            {"output": "Hola, soy un agente"},
        ]
        mock_create_agent.return_value = mock_agent

        questions = ["¿Cuánto es 2+2?", "¿Quién eres?"]
        results = batch_chat(questions)

        assert len(results) == 2
        assert results[0]["question"] == "¿Cuánto es 2+2?"
        assert results[0]["answer"] == "4"
        assert results[1]["question"] == "¿Quién eres?"
        assert results[1]["answer"] == "Hola, soy un agente"

    @patch("agent.create_agent")
    def test_batch_chat_skips_empty_questions(self, mock_create_agent):
        mock_agent = MagicMock()
        mock_agent.invoke.return_value = {"output": "respuesta"}
        mock_create_agent.return_value = mock_agent

        questions = ["pregunta1", "", "  ", "pregunta2"]
        results = batch_chat(questions)

        assert len(results) == 2
        assert mock_agent.invoke.call_count == 2

    @patch("agent.create_agent")
    def test_batch_chat_handles_errors(self, mock_create_agent):
        mock_agent = MagicMock()
        mock_agent.invoke.side_effect = Exception("API error")
        mock_create_agent.return_value = mock_agent

        questions = ["pregunta con error"]
        results = batch_chat(questions)

        assert len(results) == 1
        assert "error" in results[0]
        assert results[0]["error"] == "API error"

    @patch("agent.create_agent")
    def test_batch_chat_empty_list(self, mock_create_agent):
        mock_create_agent.return_value = MagicMock()

        results = batch_chat([])

        assert results == []

    @patch("agent.create_agent")
    def test_batch_chat_preserves_conversation_context(self, mock_create_agent):
        """Verifica que se usa un solo agente para todas las preguntas (memoria compartida)."""
        mock_agent = MagicMock()
        mock_agent.invoke.return_value = {"output": "respuesta"}
        mock_create_agent.return_value = mock_agent

        questions = ["pregunta1", "pregunta2", "pregunta3"]
        batch_chat(questions)

        # create_agent se llama una sola vez para todas las preguntas
        mock_create_agent.assert_called_once()
        assert mock_agent.invoke.call_count == 3

    @patch("agent.create_agent")
    def test_batch_chat_output_no_interactive_prompt(self, mock_create_agent, capsys):
        """Verifica que batch_chat no usa el prompt interactivo 'Tú:'."""
        mock_agent = MagicMock()
        mock_agent.invoke.return_value = {"output": "respuesta"}
        mock_create_agent.return_value = mock_agent

        questions = ["¿Cuánto es 2+2?"]
        batch_chat(questions)

        captured = capsys.readouterr()
        assert "Tú:" not in captured.out
        assert "📝 ¿Cuánto es 2+2?" in captured.out
