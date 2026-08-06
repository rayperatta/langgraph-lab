# ⚡ Cheat Sheet — LangChain + LangGraph en 1 página

> Todo lo esencial. Léelo en 10 minutos y ya hablas el idioma.
> Lo de abajo es lo que de verdad se usa en el 90% de los proyectos.

## Los 2 mundos

| | LangChain | LangGraph |
|---|---|---|
| **Qué es** | Librería para hablar con LLMs | Framework para construir agentes |
| **Metáfora** | El walkie-talkie con el modelo | La máquina de estados que lo orquesta |
| **Pieza clave** | Chains (LCEL) | Grafos (estado + nodos + edges) |

## Los 9 conceptos que importan

**1. Chain (LCEL)** — encadenar piezas con el operador `|`
```python
chain = prompt | llm | StrOutputParser()
```
El output de cada pieza entra como input a la siguiente. Nada más.

**2. Prompt template** — plantilla con variables `{asi}` que se rellenan al invocar.

**3. Tool** — una función Python normal con decorador `@tool` y docstring.
El LLM *no la ejecuta*: solo **pide** que la ejecutes (devuelve `tool_calls`).

**4. `bind_tools()`** — le dices al modelo qué tools existen:
```python
llm_con_tools = llm.bind_tools([sumar, clima])
```

**5. Estado (`StateGraph` + `TypedDict`)** — un diccionario tipado que viaja
por el grafo. Cada nodo recibe el estado y devuelve solo lo que cambia.

**6. Nodos y edges** — un nodo = una función. Un edge = "después de A va B".
`START` y `END` son nodos virtuales. `compile()` + `invoke()` lo ejecuta.

**7. Router (`add_conditional_edges`)** — una función que mira el estado y
decide el siguiente nodo. **Esto convierte un pipeline en un agente.**
```python
builder.add_conditional_edges("clasificar", es_par, {"par": "par", "impar": "impar"})
```

**8. Agente ReAct** — el patrón estrella: bucle `llm ⇄ tools`
hasta que el modelo deja de pedir tools. Con piezas prefabricadas:
```python
builder = StateGraph(MessagesState)
builder.add_node("llm", nodo_llm)
builder.add_node("tools", ToolNode(tools))
builder.add_conditional_edges("llm", tools_condition)  # ¿pide tools? -> tools : END
```

**9. Memoria y human-in-the-loop** — saber que existen:
- **Checkpointer + `thread_id`** = el grafo recuerda entre mensajes (conversación).
- **`interrupt()`** = el grafo se pausa y espera aprobación humana, luego `Command(resume=...)` continúa.

## Vocabulario de entrevista (suena pro)

- **Agente**: LLM dentro de un bucle con tools que decide solo cuándo parar.
- **Tool calling**: el modelo devuelve JSON pidiendo ejecutar una función.
- **Grafo / nodo / edge**: función / conexión entre funciones.
- **Router**: lógica de decisión entre nodos (la "inteligencia" del flujo).
- **Reducer**: cómo se fusionan las actualizaciones de estado (ej. `Annotated[list, add]` acumula).
- **Checkpointing**: guardar el estado del grafo para reanudar o recordar.
- **Human-in-the-loop**: el agente pide permiso antes de acciones delicadas.
- **LCEL**: LangChain Expression Language, la sintaxis de pipes `|`.

## Regla mental

> Si es "llamar al LLM y formatear" → **LangChain**.
> Si es "decidir qué hacer después" → **LangGraph**.
