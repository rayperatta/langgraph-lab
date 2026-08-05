"""LECCIÓN 07 — Human-in-the-loop: pausar el grafo para aprobación humana

Conceptos:
  - interrupt() CONGELA el grafo en medio de un nodo y devuelve control al humano
  - El humano inspecciona el estado y reanuda con Command(resume=...)
  - Requiere checkpointer (el grafo se "suspende" guardando su estado)
  - Es el patrón de las apps serias: el agente propone, el humano aprueba

Flujo:  invoke -> nodo llega a interrupt() -> invoke devuelve __interrupt__
        -> tú envías Command(resume="aprobado") -> el nodo continúa

Ejecuta:  python 07_langgraph_humano.py
"""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command


class Estado(TypedDict):
    transferencia: str
    aprobada: bool
    log: str


def preparar(state: Estado) -> dict:
    return {"log": f"Preparada transferencia: {state['transferencia']}"}


def pedir_aprobacion(state: Estado) -> dict:
    # ⏸  AQUÍ el grafo se congela. El valor de interrupt() sale al exterior.
    decision = interrupt({
        "pregunta": f"¿Aprobar {state['transferencia']}?",
        "opciones": ["aprobar", "rechazar"],
    })
    # ▶  Cuando reanudes con Command(resume=X), `decision` = X y sigue aquí.
    return {"aprobada": decision == "aprobar", "log": f"Decisión humana: {decision}"}


def ejecutar(state: Estado) -> dict:
    if state["aprobada"]:
        return {"log": "✅ Transferencia ejecutada"}
    return {"log": "❌ Transferencia cancelada"}


builder = StateGraph(Estado)
builder.add_node("preparar", preparar)
builder.add_node("pedir_aprobacion", pedir_aprobacion)
builder.add_node("ejecutar", ejecutar)
builder.add_edge(START, "preparar")
builder.add_edge("preparar", "pedir_aprobacion")
builder.add_edge("pedir_aprobacion", "ejecutar")
builder.add_edge("ejecutar", END)

grafo = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "demo-hitl"}}

# --- 1. Primer invoke: corre hasta el interrupt ------------------------------
print("▶ Lanzando...")
r = grafo.invoke({"transferencia": "500€ a proveedor X", "aprobada": False, "log": ""}, config=config)
pausa = r["__interrupt__"][0].value
print("⏸  Grafo pausado. Pregunta al humano:", pausa["pregunta"])
print("   log hasta ahora:", r["log"])

# --- 2. El humano decide y el grafo CONTINÚA desde donde se quedó ------------
print("\n▶ Humano responde 'rechazar'...")
r = grafo.invoke(Command(resume="rechazar"), config=config)
print("   log final:", r["log"])

# 🧠 EJERCICIO: lanza otro thread_id y responde "aprobar". Luego combina esta
# lección con la 05: haz que el agente pida aprobación ANTES de ejecutar
# ciertas tools peligrosas (interrupt dentro del ToolNode o antes de él).
# Así nace un agente con "modo supervisado".
