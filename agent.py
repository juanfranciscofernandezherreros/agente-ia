"""
agent.py - Tu primer agente de IA
"""
import argparse
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from tools import all_tools

load_dotenv()


def create_agent():
    """Crea y configura el agente"""

    # 1. Configurar el LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",  # Buena relación calidad/precio
        temperature=0,  # Respuestas consistentes
    )

    # 2. Definir el prompt del agente
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Eres un asistente inteligente con acceso a herramientas.

REGLAS:
- Siempre explica brevemente qué vas a hacer antes de usar una herramienta
- Si no necesitas herramientas, responde directamente
- Para cálculos, usa la calculadora
- Para información actual (precios, noticias, datos), busca en internet
- No repitas búsquedas web casi iguales para la misma pregunta
- Usa como máximo 2 búsquedas web por pregunta antes de responder
- Sé conciso pero útil

IMPORTANTE: Piensa paso a paso antes de actuar.""",
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # 3. Crear el agente
    agent = create_openai_tools_agent(llm, all_tools, prompt)

    # 4. Crear el executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=all_tools,
        verbose=True,  # Ver el razonamiento del agente
        handle_parsing_errors=True,
        max_iterations=3,  # Límite de pasos para evitar loops
        early_stopping_method="generate",
    )

    return agent_executor


def chat():
    """Loop de conversación con el agente"""
    print("🤖 Agente de IA iniciado. Escribe 'salir' para terminar.\n")
    print("Puedo buscar en internet, hacer cálculos y ejecutar código Python.\n")

    agent = create_agent()
    chat_history = []

    while True:
        user_input = input("Tú: ").strip()

        if user_input.lower() in ["salir", "exit", "quit"]:
            print("👋 ¡Hasta luego!")
            break

        if not user_input:
            continue

        try:
            response = agent.invoke({"input": user_input, "chat_history": chat_history})
            answer = response["output"]
            print(f"\n🤖 Agente: {answer}\n")
            chat_history.extend(
                [HumanMessage(content=user_input), AIMessage(content=answer)]
            )
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")


def batch_chat(questions):
    """Procesa una lista de preguntas de forma seguida sin interacción del usuario.

    Args:
        questions: Lista de preguntas a responder secuencialmente.

    Returns:
        Lista de diccionarios con las preguntas y sus respuestas.
    """
    agent = create_agent()
    chat_history = []
    results = []
    valid_questions = [q.strip() for q in questions if q.strip()]

    print("🤖 Procesando lista de preguntas...\n")

    for i, question in enumerate(valid_questions, 1):
        print(f"--- Pregunta {i}/{len(valid_questions)} ---")
        print(f"📝 {question}")

        try:
            response = agent.invoke({"input": question, "chat_history": chat_history})
            answer = response["output"]
            print(f"\n🤖 Agente: {answer}\n")
            results.append({"question": question, "answer": answer})
            chat_history.extend(
                [HumanMessage(content=question), AIMessage(content=answer)]
            )
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error: {error_msg}\n")
            results.append({"question": question, "error": error_msg})

    print("✅ Todas las preguntas han sido procesadas.")
    return results


DEFAULT_QUESTIONS = [
    "¿Qué fecha y hora es ahora mismo?",
    "¿Cuánto es 125 * 37 + 99?",
    "Busca en internet cuál es la última versión de Python",
    "Escribe un programa en Python que calcule los primeros 10 números de Fibonacci",
    "¿Cuál es la raíz cuadrada de 2025?",
]


def main(argv=None):
    """Punto de entrada principal del agente."""
    parser = argparse.ArgumentParser(description="Agente de IA con herramientas")
    parser.add_argument(
        "--questions",
        nargs="+",
        help="Preguntas a procesar secuencialmente",
    )
    args = parser.parse_args(argv)

    if args.questions:
        batch_chat(args.questions)
    else:
        chat()


if __name__ == "__main__":
    main()
