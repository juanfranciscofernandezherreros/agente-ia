"""
test_agent.py - Tests para las funciones del agente
"""
from unittest.mock import patch, MagicMock

from langchain_core.messages import AIMessage, HumanMessage

from agent import batch_chat, create_agent, main, DEFAULT_QUESTIONS


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
    def test_batch_chat_passes_chat_history_between_questions(self, mock_create_agent):
        """Verifica que batch_chat envía el historial acumulado en cada invocación."""
        mock_agent = MagicMock()
        captured_histories = []

        def fake_invoke(payload):
            captured_histories.append(list(payload["chat_history"]))
            return {"output": "respuesta"}

        mock_agent.invoke.side_effect = fake_invoke
        mock_create_agent.return_value = mock_agent

        batch_chat(["pregunta1", "pregunta2"])

        assert len(captured_histories[0]) == 0
        assert len(captured_histories[1]) == 2
        assert isinstance(captured_histories[1][0], HumanMessage)
        assert isinstance(captured_histories[1][1], AIMessage)
        assert captured_histories[1][0].content == "pregunta1"
        assert captured_histories[1][1].content == "respuesta"

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


class TestDefaultQuestions:
    """Tests para las preguntas por defecto."""

    def test_default_questions_has_five(self):
        assert len(DEFAULT_QUESTIONS) == 5

    def test_default_questions_are_non_empty_strings(self):
        for q in DEFAULT_QUESTIONS:
            assert isinstance(q, str)
            assert q.strip() != ""

    @patch("agent.create_agent")
    def test_batch_chat_with_default_questions(self, mock_create_agent):
        """Verifica que batch_chat procesa las 5 preguntas por defecto."""
        mock_agent = MagicMock()
        mock_agent.invoke.return_value = {"output": "respuesta"}
        mock_create_agent.return_value = mock_agent

        results = batch_chat(DEFAULT_QUESTIONS)

        assert len(results) == 5
        assert mock_agent.invoke.call_count == 5


class TestCLIQuestionsFlag:
    """Tests para el argumento --questions de la línea de comandos."""

    @patch("agent.batch_chat")
    @patch("agent.chat")
    def test_questions_flag_calls_batch_chat(self, mock_chat, mock_batch_chat):
        """Verifica que --questions invoca batch_chat con las preguntas dadas."""
        main(["--questions", "¿Cuánto es 2+2?", "¿Qué día es hoy?"])

        mock_batch_chat.assert_called_once_with(
            ["¿Cuánto es 2+2?", "¿Qué día es hoy?"]
        )
        mock_chat.assert_not_called()

    @patch("agent.batch_chat")
    @patch("agent.chat")
    def test_no_questions_flag_calls_chat(self, mock_chat, mock_batch_chat):
        """Verifica que sin --questions se usa el modo interactivo."""
        main([])

        mock_chat.assert_called_once()
        mock_batch_chat.assert_not_called()


class TestAgentCreation:
    """Tests para la creación del agente."""

    @patch("agent.AgentExecutor")
    @patch("agent.create_openai_tools_agent")
    @patch("agent.ChatOpenAI")
    def test_create_agent_without_deprecated_memory(
        self, mock_chat_openai, mock_create_openai_tools_agent, mock_agent_executor
    ):
        mock_chat_openai.return_value = MagicMock()
        mock_create_openai_tools_agent.return_value = MagicMock()
        mock_agent_executor.return_value = MagicMock()

        create_agent()

        _, kwargs = mock_agent_executor.call_args
        assert "memory" not in kwargs
        assert kwargs["max_iterations"] == 3
        assert kwargs["early_stopping_method"] == "generate"
