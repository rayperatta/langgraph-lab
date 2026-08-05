"""LECCIÓN 01 — LangChain básico: LLM, PromptTemplate y chains (LCEL)

Conceptos:
  - ChatModel: la interfaz universal (invoke, batch, stream)
  - ChatPromptTemplate: plantillas con variables {así}
  - LCEL: el operador "|" encadena piezas -> prompt | llm | parser

Ejecuta:  python 01_langchain_basico.py
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.llm import get_llm, modo_actual

print(f"🔌 Modo LLM: {modo_actual()}\n")
llm = get_llm()

# --- 1. Invocación directa -------------------------------------------------
# Un ChatModel recibe mensajes y devuelve un AIMessage.
respuesta = llm.invoke("Explica en una frase qué es LangChain")
print("1) invoke directo:\n  ", respuesta.content, "\n")

# --- 2. PromptTemplate: separar la plantilla de los datos ------------------
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un profesor de programación conciso. Responde en español."),
    ("human", "Explícame {tema} como si tuviera {edad} años."),
])

# Puedes ver cómo queda el prompt ANTES de llamar al modelo (¡gratis!):
mensajes = prompt.invoke({"tema": "recursión", "edad": 12})
print("2) prompt renderizado:")
for m in mensajes.messages:
    print(f"   [{m.type}] {m.content}")
print()

# --- 3. LCEL: encadenar con "|" --------------------------------------------
# prompt | llm | parser  ==  pipeline: dict -> mensajes -> AIMessage -> str
chain = prompt | llm | StrOutputParser()
salida = chain.invoke({"tema": "qué es un grafo", "edad": 15})
print("3) chain LCEL:\n  ", salida, "\n")

# --- 4. Streaming: token a token -------------------------------------------
print("4) stream: ", end="", flush=True)
for chunk in chain.stream({"tema": "LangGraph", "edad": 20}):
    print(chunk, end="", flush=True)
print("\n")

# 🧠 EJERCICIO: añade una variable {nivel} al prompt ("básico/avanzado")
# y observa cómo cambia la salida. Luego prueba chain.batch([...]) con 3 dicts.
