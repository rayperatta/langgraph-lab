"""LECCIÓN 06 — Memoria: checkpointers y threads

Conceptos:
  - Un CHECKPOINTER guarda el estado en cada paso del grafo
  - Cada ejecución se identifica por config={"configurable": {"thread_id": "..."}}
  - Mismo thread_id = el grafo RECUERDA el estado anterior (memoria)
  - thread_id distinto = conversación nueva e independiente
  - InMemorySaver para aprender; en producción: SqliteSaver / PostgresSaver

Esto es lo que hace que un agente "recuerde" entre mensajes.

Ejecuta:  python 06_langgraph_memoria.py
"""
from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver


class Estado(TypedDict):
    notas: Annotated[list[str], add]  # reducer: acumula entre pasos Y threads


def recordar(state: Estado) -> dict:
    n = len(state["notas"])
    return {"notas": [f"nota #{n + 1}: mensaje recibido"]}


builder = StateGraph(Estado)
builder.add_node("recordar", recordar)
builder.add_edge(START, "recordar")
builder.add_edge("recordar", END)

# Sin checkpointer: cada invoke empieza de cero. CON checkpointer: hay memoria.
checkpointer = InMemorySaver()
grafo = builder.compile(checkpointer=checkpointer)

ana = {"configurable": {"thread_id": "chat-ana"}}
luis = {"configurable": {"thread_id": "chat-luis"}}

print("▶ Thread 'ana' — 3 mensajes seguidos:")
for i in range(3):
    r = grafo.invoke({"notas": []}, config=ana)
    print(f"   mensaje {i + 1}: notas acumuladas = {len(r['notas'])}")

print("\n▶ Thread 'luis' — conversación INDEPENDIENTE:")
r = grafo.invoke({"notas": []}, config=luis)
print(f"   mensaje 1: notas acumuladas = {len(r['notas'])}  (empieza de 0)")

print("\n▶ Ana vuelve: su memoria sigue ahí")
r = grafo.invoke({"notas": []}, config=ana)
print(f"   notas acumuladas = {len(r['notas'])}")

# --- Inspeccionar el estado guardado ----------------------------------------
print("\n📦 Estado actual del thread 'ana' desde el checkpointer:")
estado = grafo.get_state(ana)
print("   values:", estado.values)
print("   next:", estado.next, " (qué nodo tocaría ejecutar)")

# 🧠 EJERCICIO: cambia InMemorySaver por SqliteSaver (langgraph-checkpoint-sqlite)
# con una ruta de archivo. Cierra y vuelve a ejecutar: la memoria SOBREVIVE
# al reinicio del proceso. Esa es la diferencia entre demo y producción.
