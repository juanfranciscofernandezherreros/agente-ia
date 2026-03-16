# Diagramas del Proyecto agente-ia

Diagramas de análisis generados con [Mermaid](https://mermaid.js.org/), que GitHub renderiza automáticamente.

---

## 1. Visión general del sistema

Contexto del sistema y actores que interactúan con el agente.

```mermaid
graph TB
    subgraph Usuario
        U1[👤 Usuario CLI]
        U2[🐳 Docker / Compose]
        U3[🐍 Código Python externo]
    end

    subgraph agente-ia
        E1[agent.py\nchat / batch_chat / main]
        E2[ask_agent.py\nmain]
        E3[tools.py\nherramientas]
    end

    subgraph Servicios externos
        S1[🤖 OpenAI API\ngpt-4o-mini]
        S2[🌐 DuckDuckGo\nbúsqueda web]
    end

    U1 -->|python agent.py| E1
    U1 -->|python ask_agent.py| E2
    U2 -->|docker run| E1
    U3 -->|from agent import batch_chat| E1
    E2 --> E1
    E1 --> E3
    E1 -->|LangChain / ChatOpenAI| S1
    E3 -->|DuckDuckGoSearchRun| S2
```

---

## 2. Dependencias entre módulos

Relaciones de importación entre los ficheros Python del proyecto.

```mermaid
graph LR
    subgraph Proyecto
        AG[agent.py]
        AS[ask_agent.py]
        TO[tools.py]
    end

    subgraph LangChain
        LC1[langchain_openai\nChatOpenAI]
        LC2[langchain_classic.agents\nAgentExecutor\ncreate_openai_tools_agent]
        LC3[langchain_core.prompts\nChatPromptTemplate\nMessagesPlaceholder]
        LC4[langchain_core.messages\nHumanMessage / AIMessage]
        LC5[langchain_core.tools\n@tool]
        LC6[langchain_community.tools\nDuckDuckGoSearchRun]
    end

    subgraph Stdlib
        PY1[math]
        PY2[datetime]
        PY3[argparse / os]
        PY4[python-dotenv]
        PY5[sys]
    end

    AS -->|from agent import batch_chat| AG
    AS --> PY5
    AG --> TO
    AG --> LC1
    AG --> LC2
    AG --> LC3
    AG --> LC4
    AG --> PY3
    AG --> PY4
    TO --> LC5
    TO --> LC6
    TO --> PY1
    TO --> PY2
```

---

## 3. Diagrama de secuencia — pregunta interactiva

Flujo completo desde que el usuario escribe una pregunta hasta que recibe la respuesta en modo interactivo (`python agent.py`).

```mermaid
sequenceDiagram
    actor Usuario
    participant Chat as chat() [agent.py]
    participant Executor as AgentExecutor [LangChain]
    participant LLM as ChatOpenAI [OpenAI API]
    participant Tool as Herramienta [tools.py]

    Usuario->>Chat: escribe pregunta
    Chat->>Executor: invoke({input, chat_history})
    Executor->>LLM: genera plan / razonamiento
    LLM-->>Executor: devuelve tool_call o texto final

    alt Se necesita herramienta
        Executor->>Tool: llama a la herramienta seleccionada
        Tool-->>Executor: devuelve resultado
        Executor->>LLM: añade resultado al contexto
        LLM-->>Executor: respuesta final
    end

    Executor-->>Chat: {"output": "respuesta"}
    Chat-->>Usuario: muestra 🤖 respuesta
    Chat->>Chat: actualiza chat_history
```

---

## 4. Diagrama de secuencia — modo batch

Flujo para `batch_chat()` con múltiples preguntas (usado por `--questions` y `ask_agent.py`).

```mermaid
sequenceDiagram
    actor Caller as Llamador\n(CLI / código)
    participant BC as batch_chat() [agent.py]
    participant Executor as AgentExecutor [LangChain]
    participant LLM as ChatOpenAI [OpenAI API]

    Caller->>BC: lista de preguntas
    BC->>BC: create_agent() → un solo agente

    loop Para cada pregunta
        BC->>Executor: invoke({input, chat_history})
        Executor->>LLM: procesa con historial acumulado
        LLM-->>Executor: respuesta
        Executor-->>BC: {"output": "..."}
        BC->>BC: acumula HumanMessage + AIMessage en chat_history
        BC->>BC: agrega {question, answer} a results
    end

    BC-->>Caller: lista de resultados
```

---

## 5. Diagrama de flujo — punto de entrada `main()`

Lógica de decisión al ejecutar `python agent.py`.

```mermaid
flowchart TD
    Start([Inicio: python agent.py]) --> Parse[Parsear args con argparse]
    Parse --> HasQ{"¿args.questions\nestá definido?"}

    HasQ -- Sí --> Batch[batch_chat(questions)]
    HasQ -- No --> Interactive[chat() modo interactivo]

    Batch --> Loop1[Procesa cada pregunta\ncon historial compartido]
    Loop1 --> Done1([Fin])

    Interactive --> Loop2[Espera input\ndel usuario]
    Loop2 --> EmptyQ{¿Input vacío?}
    EmptyQ -- Sí --> Loop2
    EmptyQ -- No --> Salir{"¿salir / exit / quit?"}
    Salir -- Sí --> Done2([Fin])
    Salir -- No --> Invoke[agent.invoke]
    Invoke --> Print[Muestra respuesta]
    Print --> Loop2
```

---

## 6. Componentes de las herramientas (`tools.py`)

Descripción de cada herramienta y sus dependencias.

```mermaid
graph TD
    subgraph tools.py
        AT[all_tools\nlista de herramientas]
        SW[search_web\nBúsqueda DuckDuckGo]
        CA[calculator\nEvaluación matemática]
        RP[run_python\nEjecución Python restringida]
        DT[get_current_datetime\nFecha y hora actual]
    end

    AT --> SW
    AT --> CA
    AT --> RP
    AT --> DT

    SW -->|DuckDuckGoSearchRun| DDG[🌐 DuckDuckGo]
    CA -->|math.sqrt / sin / cos / ...| MATH[stdlib: math]
    CA -->|eval con __builtins__ vacíos| EVAL[Evaluador seguro]
    RP -->|exec con __builtins__ restringidos| EXEC[Ejecutor seguro]
    DT -->|datetime.now| DATElib[stdlib: datetime]
```

---

## 7. Arquitectura de despliegue

Entornos de ejecución disponibles.

```mermaid
graph LR
    subgraph Local
        PY[Python 3.10+]
        ENV[.env\nOPENAI_API_KEY]
        PY -- lee --> ENV
    end

    subgraph Docker
        DC[docker-compose.yml]
        DF[Dockerfile\npython:3.12-slim]
        DC --> DF
        DF -- env_file --> ENV2[.env / variable de entorno]
    end

    subgraph Producción recomendada
        SB[Sandbox adicional\ncontenedor aislado +\nlímites de red/recursos]
    end

    Local -->|"python agent.py"| AGENT[agente-ia]
    Docker -->|"docker compose run"| AGENT
    SB --> AGENT
    AGENT -->|HTTPS| OAI[OpenAI API]
    AGENT -->|HTTPS| DDG2[DuckDuckGo]
```

---

## 8. Resumen de la estructura del proyecto

```mermaid
graph TD
    ROOT[agente-ia/]

    ROOT --> AG[agent.py\ncreate_agent · chat\nbatch_chat · main]
    ROOT --> AS[ask_agent.py\nmain]
    ROOT --> TO[tools.py\nsearch_web · calculator\nrun_python · get_current_datetime]
    ROOT --> REQ[requirements.txt]
    ROOT --> DF[Dockerfile]
    ROOT --> DC[docker-compose.yml]
    ROOT --> ENV[.env.example]
    ROOT --> TESTS[tests/]
    ROOT --> DOCS[docs/]

    TESTS --> T1[test_agent.py]
    TESTS --> T2[test_tools.py]
    TESTS --> T3[test_ask_agent.py]
    DOCS --> D1[diagrams.md]
```
