"""
ask_agent.py - Ejecuta preguntas en lote desde argumentos posicionales.
"""
import sys

from agent import batch_chat


def main(argv=None):
    """Procesa preguntas pasadas como argumentos sin interacción."""
    questions = argv if argv is not None else sys.argv[1:]

    if not questions:
        print(
            "Usa: python ask_agent.py 'pregunta1' 'pregunta2' ...",
            file=sys.stderr,
        )
        return 1

    batch_chat(questions)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
