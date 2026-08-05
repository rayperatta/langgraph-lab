"""LECCIÓN 05 — Agente ReAct: LLM + tools en un bucle de grafo

Conceptos:
  - ReAct = Reason + Act: el LLM piensa, pide una tool, se ejecuta, ve el
    resultado, y decide si pedir otra o responder. Es un BUCLE en el grafo.
  - MessagesState: estado estándar con `messages` (con reducer incluido)
  - ToolNode: nodo prefabricado que ejecuta los tool_calls por ti
  - El router `tools_condition`: envía a "tools" si hay tool_calls, si no a END

Este patrón es EL agente. Todo lo demás (memoria, humano, subgrafos) son extras.

Ejecuta:  python 05_langgraph_agente.py
(necesita un LLM real en .env — el fake no sabe pedir tools)
"""
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from utils.llm import get_llm, modo_actual

print(f"🔌 Modo LLM: {modo_actual()}\n")


@tool
def sumar(a: float, b: float) -> float:
    """Suma dos números."""
    return a + b


@tool
def multiplicar(a: float, b: float) -> float:
    """Multiplica dos números."""
    return a * b


tools = [sumar, multiplicar]
llm = get_llm().bind_tools(tools)


def nodo_llm(state: MessagesState) -> dict:
    """El LLM ve toda la conversación y decide: responder o pedir tool."""
    respuesta = llm.invoke(state["messages"])
    return {"messages": [respuesta]}  # MessagesState concatena solo


builder = StateGraph(MessagesState)
builder.add_node("llm", nodo_llm)
builder.add_node("tools", ToolNode(tools))     # ejecuta tool_calls automáticamente

builder.add_edge(START, "llm")
# Si el último mensaje tiene tool_calls -> "tools"; si no -> END
builder.add_conditional_edges("llm", tools_condition)
builder.add_edge("tools", "llm")               # tras la tool, el LLM ve el resultado

agente = builder.compile()

print("🗺 ", agente.get_graph().draw_ascii(), "\n")

if modo_actual().startswith("FAKE"):
    print("⚠️  Modo FAKE: configura .env con un LLM real para ver el bucle ReAct.")
    print("    Mientras tanto, observa el diagrama: llm ⇄ tools hasta terminar.\n")
else:
    r = agente.invoke({"messages": [("human", "Cuánto es (12 + 8) * 3? Piensa paso a paso.")]})
    print("▶ Traza completa del agente:")
    for m in r["messages"]:
        extra = f"  tool_calls={[c['name'] for c in m.tool_calls]}" if getattr(m, "tool_calls", None) else ""
        print(f"   [{m.type}]{extra} {m.content[:120]}")

# 🧠 EJERCICIO: añade la tool `clima` de la lección 02 y pregunta algo que
# requiera DOS tools seguidas ("suma 5+3 y dime el clima de Madrid").
# Cuenta cuántas vueltas da el bucle llm->tools->llm.
