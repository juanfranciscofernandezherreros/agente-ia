"""
agent.py - Tu primer agente de IA
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

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

    # 4. Configurar memoria para conversación
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True
    )

    # 5. Crear el executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=all_tools,
        memory=memory,
        verbose=True,  # Ver el razonamiento del agente
        handle_parsing_errors=True,
        max_iterations=5,  # Límite de pasos para evitar loops
    )

    return agent_executor


def chat():
    """Loop de conversación con el agente"""
    print("🤖 Agente de IA iniciado. Escribe 'salir' para terminar.\n")
    print("Puedo buscar en internet, hacer cálculos y ejecutar código Python.\n")

    agent = create_agent()

    while True:
        user_input = input("Tú: ").strip()

        if user_input.lower() in ["salir", "exit", "quit"]:
            print("👋 ¡Hasta luego!")
            break

        if not user_input:
            continue

        try:
            response = agent.invoke({"input": user_input})
            print(f"\n🤖 Agente: {response['output']}\n")
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")


if __name__ == "__main__":
    chat()
