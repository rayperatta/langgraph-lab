"""LECCIÓN 04 — Edges condicionales: el grafo DECIDE por dónde ir

Conceptos:
  - add_conditional_edges(nodo, router): una función ROUTER mira el estado
    y devuelve el NOMBRE del siguiente nodo
  - Es la base de TODOS los agentes: "si el LLM pidió tool -> ejecutar tool;
    si no -> responder y terminar"
  - Reducers: anotar un campo con `Annotated[list, add]` hace que los nodos
    AÑADAN a la lista en vez de sobrescribirla (esencial para historiales)

Ejecuta:  python 04_langgraph_condicional.py
"""
from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END


class Estado(TypedDict):
    numero: int
    # Annotated[list, add] = cada nodo devuelve items y se CONCATENAN
    rastro: Annotated[list[str], add]


def clasificar(state: Estado) -> dict:
    return {"rastro": [f"clasifiqué {state['numero']}"]}


def es_par(state: Estado) -> str:
    """ROUTER: devuelve el nombre del siguiente nodo (o END)."""
    return "par" if state["numero"] % 2 == 0 else "impar"


def nodo_par(state: Estado) -> dict:
    return {"rastro": ["era par -> divido entre 2"], "numero": state["numero"] // 2}


def nodo_impar(state: Estado) -> dict:
    return {"rastro": ["era impar -> multiplico por 3 y sumo 1"], "numero": state["numero"] * 3 + 1}


builder = StateGraph(Estado)
builder.add_node("clasificar", clasificar)
builder.add_node("par", nodo_par)
builder.add_node("impar", nodo_impar)

builder.add_edge(START, "clasificar")
# La magia: después de "clasificar", la función es_par decide el camino
builder.add_conditional_edges("clasificar", es_par, {"par": "par", "impar": "impar"})
builder.add_edge("par", END)
builder.add_edge("impar", END)

grafo = builder.compile()

for n in (10, 7):
    print(f"▶ numero={n}")
    r = grafo.invoke({"numero": n, "rastro": []})
    print("   rastro:", " | ".join(r["rastro"]), "-> resultado:", r["numero"], "\n")

print("🗺 ", grafo.get_graph().draw_ascii())

# 🧠 EJERCICIO: convierte esto en la conjetura de Collatz — haz que "par" e
# "impar" vuelvan a "clasificar" hasta que numero == 1 (router -> END si es 1).
# Ojo: pon un límite de iteraciones para no hacer un bucle infinito.
