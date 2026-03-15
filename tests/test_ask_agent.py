"""
test_ask_agent.py - Tests para el script de ejecución batch por argumentos.
"""
from unittest.mock import patch

from ask_agent import main


class TestAskAgentScript:
    @patch("ask_agent.batch_chat")
    def test_main_calls_batch_chat_with_positional_arguments(self, mock_batch_chat):
        exit_code = main(["¿Cuánto es 2+2?", "¿Qué día es hoy?"])

        assert exit_code == 0
        mock_batch_chat.assert_called_once_with(
            ["¿Cuánto es 2+2?", "¿Qué día es hoy?"]
        )

    @patch("ask_agent.batch_chat")
    def test_main_without_arguments_prints_usage(self, mock_batch_chat, capsys):
        exit_code = main([])

        captured = capsys.readouterr()
        assert exit_code == 1
        assert captured.err == "Usa: python ask_agent.py 'pregunta1' 'pregunta2' ...\n"
        mock_batch_chat.assert_not_called()
