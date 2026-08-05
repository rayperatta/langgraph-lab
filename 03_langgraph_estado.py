"""LECCIÓN 03 — LangGraph: estado, nodos y edges

Conceptos:
  - El ESTADO es un dict tipado que fluye por el grafo
  - Cada NODO es una función: recibe estado -> devuelve CAMBIOS (merge)
  - Los EDGES conectan nodos; START/END son nodos virtuales
  - compile() -> invoke() ejecuta el grafo de punta a punta

Mentalidad: no "llamas funciones", defines una máquina de estados.

Ejecuta:  python 03_langgraph_estado.py
"""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# --- 1. El estado: contrato de datos del grafo ------------------------------
class Estado(TypedDict):
    nombre: str
    saludo: str
    gritos: int


# --- 2. Nodos: funciones puras estado -> cambios ----------------------------
def nodo_saludar(state: Estado) -> dict:
    print(f"   [nodo_saludar] recibí: {state}")
    return {"saludo": f"Hola, {state['nombre']}!"}


def nodo_gritar(state: Estado) -> dict:
    print(f"   [nodo_gritar] recibí saludo: {state['saludo']}")
    return {"saludo": state["saludo"].upper(), "gritos": state["gritos"] + 1}


# --- 3. Construir el grafo ---------------------------------------------------
builder = StateGraph(Estado)
builder.add_node("saludar", nodo_saludar)   # nombre, función
builder.add_node("gritar", nodo_gritar)

builder.add_edge(START, "saludar")          # entrada
builder.add_edge("saludar", "gritar")       # flujo lineal
builder.add_edge("gritar", END)             # salida

grafo = builder.compile()

# --- 4. Ejecutar -------------------------------------------------------------
print("▶ Ejecutando grafo lineal START -> saludar -> gritar -> END\n")
resultado = grafo.invoke({"nombre": "Ray", "saludo": "", "gritos": 0})
print("\n◀ Estado final:", resultado)

# --- 5. Ver el grafo (ASCII) -------------------------------------------------
print("\n🗺  Estructura:")
print(grafo.get_graph().draw_ascii())

# 🧠 EJERCICIO: añade un nodo "despedir" entre gritar y END que añada
# " ¡Adiós!" al saludo. Observa cómo solo devuelves el CAMPO que cambias.
