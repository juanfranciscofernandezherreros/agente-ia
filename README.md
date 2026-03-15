# agente-ia

Tu primer agente de IA en 30 minutos. Un agente conversacional que puede:

- 🔍 Buscar información en internet
- 🔢 Hacer cálculos matemáticos
- 🐍 Ejecutar código Python
- 🧠 Decidir qué herramienta usar

## Estructura del Proyecto

```
agente-ia/
├── .env.example      # Plantilla de API keys
├── agent.py          # Código principal del agente
├── tools.py          # Herramientas custom
├── requirements.txt  # Dependencias
└── tests/
    ├── test_agent.py # Tests para el agente
    └── test_tools.py # Tests para herramientas
```

## Setup

```bash
# Clonar el repositorio
git clone https://github.com/juanfranciscofernandezherreros/agente-ia.git
cd agente-ia

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar API key
cp .env.example .env
# Editar .env con tu API key de OpenAI
```

## Uso

### Modo interactivo

```bash
python agent.py
```

#### Ejemplo de Conversación

```
🤖 Agente de IA iniciado. Escribe 'salir' para terminar.
Puedo buscar en internet, hacer cálculos y ejecutar código Python.

Tú: ¿Cuánto es la raíz cuadrada de 144?
🤖 Agente: La raíz cuadrada de 144 es **12.0**

Tú: Genera los primeros 10 números de Fibonacci
🤖 Agente: Los primeros 10 números de Fibonacci son:
**0, 1, 1, 2, 3, 5, 8, 13, 21, 34**
```

### Modo batch (lista de preguntas)

Pasa una lista de preguntas con `--questions` y el agente las responderá de forma seguida sin necesidad de interacción:

```bash
python agent.py --questions "¿Cuánto es 2+2?" "¿Qué día es hoy?" "¿Cuál es la raíz cuadrada de 144?"
```

También puedes usar el script `ask_agent.py` pasando las preguntas directamente como argumentos posicionales:

```bash
python ask_agent.py "¿Cuánto es 2+2?" "¿Qué día es hoy?" "¿Cuál es la raíz cuadrada de 144?"
```

#### Ejemplo de salida

```
🤖 Procesando lista de preguntas...

--- Pregunta 1/3 ---
Tú: ¿Cuánto es 2+2?
🤖 Agente: El resultado de 2+2 es **4**

--- Pregunta 2/3 ---
Tú: ¿Qué día es hoy?
🤖 Agente: Hoy es 15/03/2026

--- Pregunta 3/3 ---
Tú: ¿Cuál es la raíz cuadrada de 144?
🤖 Agente: La raíz cuadrada de 144 es **12.0**

✅ Todas las preguntas han sido procesadas.
```

También se puede usar `batch_chat()` de forma programática:

```python
from agent import batch_chat

preguntas = [
    "¿Cuánto es 2+2?",
    "¿Qué día es hoy?",
    "Genera los primeros 5 números de Fibonacci",
]
resultados = batch_chat(preguntas)
# resultados es una lista de {"question": ..., "answer": ...}
```

## Tests

```bash
pip install pytest
pytest tests/ -v
```

## Herramientas Disponibles

| Herramienta | Descripción |
|---|---|
| `search_web` | Busca información en internet usando DuckDuckGo |
| `calculator` | Realiza cálculos matemáticos (suma, resta, raíces, trigonometría) |
| `run_python` | Ejecuta código Python en un entorno restringido |
| `get_current_datetime` | Obtiene la fecha y hora actual |
